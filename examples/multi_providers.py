import aiohttp
from collections import defaultdict
from sanic import Sanic
from sanic.request import Request
from sanic.response import text, HTTPResponse, html
from sanic_session import InMemorySessionInterface
from sanic_oauth.blueprint import oauth_blueprint, login_required

app = Sanic('example-oauth')
app.blueprint(oauth_blueprint)
app.session_interface = InMemorySessionInterface()

app.config.OAUTH_REDIRECT_URI = 'http://127.0.0.1:8888/oauth'
app.config.OAUTH_SCOPE = 'email'
app.config.OAUTH_PROVIDERS = defaultdict(dict)
DISCORD_PROVIDER = app.config.OAUTH_PROVIDERS['discord']
DISCORD_PROVIDER['PROVIDER_CLASS'] = 'sanic_oauth.providers.DiscordClient'
DISCORD_PROVIDER['SCOPE'] = "identify email"
DISCORD_PROVIDER['CLIENT_ID'] = 'insert-you-credentials'
DISCORD_PROVIDER['CLIENT_SECRET'] = 'insert-you-credentials'
GITLAB_PROVIDER = app.config.OAUTH_PROVIDERS['gitlab']
GITLAB_PROVIDER['PROVIDER_CLASS'] = 'sanic_oauth.providers.GitlabClient'
GITLAB_PROVIDER['SCOPE'] = "read_user"
GITLAB_PROVIDER['CLIENT_ID'] = 'insert-you-credentials'
GITLAB_PROVIDER['CLIENT_SECRET'] = 'insert-you-credentials'
app.config.OAUTH_PROVIDERS['default'] = DISCORD_PROVIDER

@app.listener('before_server_start')
async def init_aiohttp_session(sanic_app, _loop) -> None:
    sanic_app.async_session = aiohttp.ClientSession()


@app.listener('after_server_stop')
async def close_aiohttp_session(sanic_app, _loop) -> None:
    await sanic_app.async_session.close()


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    await request.app.session_interface.open(request)


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    await request.app.session_interface.save(request, response)


@app.route('/')
async def main_page(_request) -> HTTPResponse:
    return html(
        """
        <a href="/login">Simple login</a></br>
        <a href="/login/gitlab">Gitlab login</a></br>
        <a href="/login/discord">Discord login</a></br>
        """
    )

@app.route('/login')
@login_required
async def index(_request: Request, user) -> HTTPResponse:
    return text("Hello world")

@app.route('/login/discord')
@login_required(provider='discord')
async def index(_request: Request, user) -> HTTPResponse:
    return text("Hello world")

@app.route('/login/gitlab')
@login_required(provider='gitlab')
async def index(_request: Request, user) -> HTTPResponse:
    return text("Hello world")

if __name__ == '__main__':
    app.run(port=8888)
