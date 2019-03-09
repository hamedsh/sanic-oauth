import aiohttp
from sanic import Sanic
from sanic.request import Request
from sanic.response import text, HTTPResponse
from sanic_session import InMemorySessionInterface
from sanic_oauth.blueprint import oauth_blueprint, login_required

app = Sanic('example-oauth')
app.blueprint(oauth_blueprint)
app.session_interface = InMemorySessionInterface()
app.config.OAUTH_PROVIDER = 'sanic_oauth.providers.DiscordClient'
app.config.OAUTH_REDIRECT_URI = 'http://127.0.0.1:8888/oauth'
app.config.OAUTH_SCOPE = 'email'
app.config.OAUTH_CLIENT_ID = 'insert-you-credentials'
app.config.OAUTH_CLIENT_SECRET = 'insert-you-credentials'


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
@login_required
async def index(_request: Request, user) -> HTTPResponse:
    return text("Hello world")


if __name__ == '__main__':
    app.run(port=8888)