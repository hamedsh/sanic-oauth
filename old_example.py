import aiohttp
from sanic import Sanic
from sanic.response import redirect, text

from sanic_oauth.providers import UserInfo, GoogleClient
from sanic_session import InMemorySessionInterface
from sanic.log import error_logger

app = Sanic('sanic_ouath_example')

session_interface = InMemorySessionInterface()


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    await session_interface.open(request)


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    await session_interface.save(request, response)


@app.listener('before_server_start')
async def init_aiohttp_session(sanic_app, _loop) -> None:
    sanic_app.async_session = aiohttp.ClientSession()


@app.listener('after_server_stop')
async def close_aiohttp_session(sanic_app, _loop) -> None:
    await sanic_app.async_session.close()


class cfg:
    oauth_redirect_path = '/oauth'  # path of oauth callback in your app
    redirect_uri = 'http://127.0.0.1:8000/oauth'  # define it in google api console

    # client id and secret from google api console
    client_id = "441279057414586368"
    client_secret = "Cqivczm6hfUlVzRBm86L1s-sITrsSjs1"

    # secret_key for session encryption
    # key must be 32 url-safe base64-encoded bytes
    secret_key = b'abcdefghijklmnopqrstuvwxyz123456'


async def oauth(request):
    client = GoogleClient(
        request.app.async_session,
        client_id=cfg.client_id,
        client_secret=cfg.client_secret
    )
    if 'code' not in request.args:
        return redirect(client.get_authorize_url(
            scope='email profile',
            redirect_uri=cfg.redirect_uri
        ))
    token, data = await client.get_access_token(
        request.args.get('code'),
        redirect_uri=cfg.redirect_uri
    )
    request['session']['token'] = token
    return redirect('/')


def login_required(fn):
    """auth decorator
    call function(request, user: <aioauth_client User object>)
    """

    async def wrapped(request, **kwargs):

        if 'token' not in request['session']:
            return redirect(cfg.oauth_redirect_path)

        client = GoogleClient(
            request.app.async_session,
            client_id=cfg.client_id,
            client_secret=cfg.client_secret,
            access_token=request['session']['token']
        )

        try:
            user, info = await client.user_info()
        except Exception as exc:
            error_logger.exception(exc)
            return redirect(cfg.oauth_redirect_path)

        return await fn(request, user, **kwargs)

    return wrapped


@app.route('/')
@login_required
async def index(request, user: UserInfo):
    return text(user.email)

app.add_route(oauth, cfg.oauth_redirect_path)


if __name__ == '__main__':
    app.run(port=8000)
