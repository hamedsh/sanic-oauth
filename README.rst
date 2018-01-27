Sanic OAuth
-----------


Simple OAuth library to work with sanic. Basically, just rewrited version of aioauth_client_ with async/await syntax and some optimization. Can be used only with python 3.5/3.6


.. _aioauth_client: https://github.com/klen/aioauth-client

Requirements
============

* python >= 3.6


Installation
============

Just install via pip:

.. code:: 

    pip install sanic_oauth


Usage
=====

.. code:: python

    # OAuth1
    import aiohttp
    from sanic_oauth import TwitterClient

    session = aiohttp.ClientSession()
    twitter = TwitterClient(
        session
        consumer_key='J8MoJG4bQ9gcmGh8H7XhMg',
        consumer_secret='7WAscbSy65GmiVOvMU5EBYn5z80fhQkcFWSLMJJu4',
    )

    request_token, request_token_secret, _ = await twitter.get_request_token()

    authorize_url = twitter.get_authorize_url(request_token)
    print("Open",authorize_url,"in a browser")
    # ...
    # Reload client to authorize_url and get oauth_verifier
    # ...
    print("PIN code:")
    oauth_verifier = input()
    oauth_token, oauth_token_secret, _ = await twitter.get_access_token(oauth_verifier)

    # Save the tokens for later use

    # ...

    twitter = TwitterClient(
        session,
        consumer_key='J8MoJG4bQ9gcmGh8H7XhMg',
        consumer_secret='7WAscbSy65GmiVOvMU5EBYn5z80fhQkcFWSLMJJu4',
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
    )

    timeline = await twitter.request('GET', 'statuses/home_timeline.json')
    content = await timeline.read()
    print(content)
    session.close()


.. code:: python
    
    # OAuth2
    import aiohttp
    from aioauth_client import GithubClient

    session = aiohttp.ClientSession()
    github = GithubClient(
        session,
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
    )

    authorize_url = github.get_authorize_url(scope="user:email")

    # ...
    # Reload client to authorize_url and get code
    # ...

    otoken, _ = await github.get_access_token(code)

    # Save the token for later use

    # ...

    github = GithubClient(
        session,
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
        access_token=otoken,
    )

    response = await github.request('GET', 'user')
    user_info = await response.json()
    session.close()



Example
=======

