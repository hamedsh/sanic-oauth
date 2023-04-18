from aiohttp import ClientSession
from aiohttp.web import HTTPBadRequest
import pytest

from sanic_oauth.providers import TwitterClient, GithubClient


@pytest.mark.asyncio
@pytest.mark.skip
async def test_oauth1():
    async with ClientSession() as session:
        twitter = TwitterClient(
            session,
            consumer_key='oUXo1M7q1rlsPXm4ER3dWnMt8',
            consumer_secret='YWzEvXZJO9PI6f9w2FtwUJenMvy9SPLrHOvnNkVkc5LdYjKKup',
        )
        assert twitter

        rtoken, rsecret, _ = await twitter.get_request_token(oauth_callback='http://fuf.me:5000/twitter')
        assert rtoken
        assert rsecret
        assert twitter.oauth_token == rtoken
        assert twitter.oauth_token_secret == rsecret

        url = twitter.get_authorize_url()
        assert url == 'https://api.twitter.com/oauth/authorize?oauth_token=%s' % rtoken

        with pytest.raises(HTTPBadRequest):
            await twitter.get_access_token('wrong', rtoken)


@pytest.mark.asyncio
async def test_oauth2():
    async with ClientSession() as session:
        github = GithubClient(
            session,
            client_id='b6281b6fe88fa4c313e6',
            client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
        )
        assert github

        assert github.get_authorize_url()
        with pytest.raises(HTTPBadRequest):
            await github.get_access_token('000')
