import importlib
import logging
from functools import partial
import re

from sanic import Blueprint, Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, redirect

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.2.1"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

_log = logging.getLogger(__name__)

oauth_blueprint = Blueprint('OAuth Configuration')  # pylint: disable=invalid-name


class OAuthConfigurationException(Exception):
    pass


async def oauth(request: Request) -> HTTPResponse:
    client = request.app.oauth_factory()
    if 'code' not in request.args:
        return redirect(client.get_authorize_url(
            scope=request.app.config.OAUTH_SCOPE,
            redirect_uri=request.app.config.OAUTH_REDIRECT_URI
        ))
    token, _data = await client.get_access_token(
        request.args.get('code'),
        redirect_uri=request.app.config.OAUTH_REDIRECT_URI
    )
    request['session']['token'] = token
    return redirect('/')


def login_required(async_handler=None, add_user_info=True, email_regex=None):
    """
    auth decorator
    call function(request, user: <sanic_oauth UserInfo object>)
    """

    if async_handler is None:
        return partial(login_required, add_user_info=add_user_info, email_regex=email_regex)

    if email_regex is not None:
        email_regex = re.compile(email_regex)

    async def wrapped(request, **kwargs):

        if 'token' not in request['session']:
            return redirect(request.app.config.OAUTH_ENDPOINT_PATH)

        client = request.app.oauth_factory(access_token=request['session']['token'])

        try:
            user, _info = await client.user_info()
        except KeyError as exc:
            _log.exception(exc)
            return redirect(request.app.config.OAUTH_ENDPOINT_PATH)

        local_email_regex = email_regex or request.app.config.OAUTH_EMAIL_REGEX

        if local_email_regex and user.email:
            if not local_email_regex.match(user.email):
                return redirect(request.app.config.OAUTH_ENDPOINT_PATH)

        if add_user_info:
            return await async_handler(request, user, **kwargs)
        return await async_handler(request, **kwargs)

    return wrapped


@oauth_blueprint.listener('after_server_start')
async def configuration_check(sanic_app: Sanic, _loop) -> None:
    if not hasattr(sanic_app, 'async_session'):
        raise OAuthConfigurationException("You should configure async_session with aiohttp.ClientSession")
    if not hasattr(sanic_app, 'session_interface'):
        raise OAuthConfigurationException("You should configure session_interface from sanic-session")


@oauth_blueprint.listener('before_server_start')
async def create_oauth_factory(sanic_app: Sanic, _loop) -> None:
    from .core import Client

    provider_class_link: str = sanic_app.config.pop('OAUTH_PROVIDER', None)
    oauth_redirect_uri: str = sanic_app.config.pop('OAUTH_REDIRECT_URI', None)
    oauth_scope: str = sanic_app.config.pop('OAUTH_SCOPE', None)
    oauth_endpoint_path: str = sanic_app.config.pop('OAUTH_ENDPOINT_PATH', '/oauth')
    oauth_email_regex: str = sanic_app.config.pop('OAUTH_EMAIL_REGEX', None)
    if provider_class_link is None:
        raise OAuthConfigurationException("You should setup OAUTH_PROVIDER setting for app")
    if oauth_redirect_uri is None:
        raise OAuthConfigurationException("You should setup OAUTH_REDIRECT_URI setting for app")
    if oauth_scope is None:
        raise OAuthConfigurationException("You should setup OAUTH_SCOPE setting for app")
    provider_module_path, provider_class_name = provider_class_link.rsplit('.', 1)
    module_object = importlib.import_module(provider_module_path)
    if module_object is None:
        raise OAuthConfigurationException(f"Cannot find module {provider_module_path} to import OAuth provider")
    provider_class = getattr(module_object, provider_class_name, None)
    if provider_class is None:
        raise OAuthConfigurationException(f"Cannot find class {provider_class_name} in module {provider_module_path}")
    if not issubclass(provider_class, Client):
        raise OAuthConfigurationException(f"Class must be a child of sanic_oauth.core.Client class")
    client_setting = {
        config_key[6:].lower(): sanic_app.config.get(config_key)
        for config_key in sanic_app.config.keys() if config_key.startswith('OAUTH')
    }

    def oauth_factory(access_token: str = None) -> Client:
        result = provider_class(
            sanic_app.async_session,
            access_token=access_token,
            **client_setting
        )
        return result

    sanic_app.oauth_factory = oauth_factory
    sanic_app.config.OAUTH_REDIRECT_URI = oauth_redirect_uri
    sanic_app.config.OAUTH_SCOPE = oauth_scope
    sanic_app.config.OAUTH_ENDPOINT_PATH = oauth_endpoint_path

    if oauth_email_regex:
        sanic_app.config.OAUTH_EMAIL_REGEX = re.compile(oauth_email_regex)

    sanic_app.add_route(oauth, oauth_endpoint_path)
