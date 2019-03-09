from typing import Dict, Tuple

from aiohttp import ClientResponse, BasicAuth

from .core import OAuth2Client, UserInfo, OAuth1Client

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.4.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"


class GoogleClient(OAuth2Client):

    """Support Google.
    * Dashboard: https://console.developers.google.com/project
    * Docs: https://developers.google.com/accounts/docs/OAuth2
    * API reference: https://developers.google.com/gdata/docs/directory
    * API explorer: https://developers.google.com/oauthplayground/
    """

    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    authorize_url = 'https://accounts.google.com/o/oauth2/auth'
    base_url = 'https://www.googleapis.com/plus/v1/'
    name = 'google'
    user_info_url = 'https://www.googleapis.com/userinfo/v2/me'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from provider."""
        return UserInfo(
            id=data.get('sub', data.get('id')),
            email=data.get('email'),
            verified_email=data.get('verified_email'),
            first_name=data.get('given_name'),
            last_name=data.get('family_name'),
            picture=data.get('picture'),
        )


class GitlabClient(OAuth2Client):

    """Support Gitlab
    * Dashboard: https://gitlab.com/profile/applications
    * Docs: https://docs.gitlab.com/ce/api/oauth2.html
    * API reference: https://docs.gitlab.com/ee/api/README.html
    """

    access_token_url = 'https://gitlab.com/oauth/token'
    authorize_url = 'https://gitlab.com/oauth/authorize'
    base_url = 'https://gitlab.com/api/v4'
    name = 'gitlab'
    user_info_url = 'https://gitlab.com/api/v4/user'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        return UserInfo(
            id=data.get('id'),
            email=data.get('email'),
            picture=data.get('avatar_url'),
            username=data.get('username'),
            link=data.get('web_url')
        )


class BitbucketClient(OAuth1Client):

    """Support Bitbucket.
    * Dashboard: https://bitbucket.org/account/user/peterhudec/api
    * Docs: https://confluence.atlassian.com/display/BITBUCKET/oauth+Endpoint
    * API refer: https://confluence.atlassian.com/display/BITBUCKET/Using+the+Bitbucket+REST+APIs
    """

    access_token_url = 'https://bitbucket.org/!api/1.0/oauth/access_token'
    authorize_url = 'https://bitbucket.org/!api/1.0/oauth/authenticate'
    base_url = 'https://api.bitbucket.org/1.0/'
    name = 'bitbucket'
    request_token_url = 'https://bitbucket.org/!api/1.0/oauth/request_token'
    user_info_url = 'https://api.bitbucket.org/1.0/user'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        user_ = data.get('user')
        return UserInfo(
            id=user_.get('username'),
            username=user_.get('username'),
            first_name=user_.get('first_name'),
            last_name=user_.get('last_name'),
            picture=user_.get('avatar'),
            link=user_.get('resource_url')
        )


class Bitbucket2Client(OAuth2Client):

    """Support Bitbucket API 2.0.
    * Dashboard: https://bitbucket.org/account/user/peterhudec/api
    * Docs:https://confluence.atlassian.com/display/BITBUCKET/OAuth+on+Bitbucket+Cloud
    * API refer: https://confluence.atlassian.com/display/BITBUCKET/Using+the+Bitbucket+REST+APIs
    """

    access_token_url = 'https://bitbucket.org/site/oauth2/access_token'
    authorize_url = 'https://bitbucket.org/site/oauth2/authorize'
    base_url = 'https://api.bitbucket.org/2.0/'
    name = 'bitbucket'
    user_info_url = 'https://api.bitbucket.org/2.0/user'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        links = data.get('links', {})
        return UserInfo(
            id=data.get('uuid'),
            username=data.get('username'),
            last_name=data.get('display_name'),
            picture=links.get('avatar', {}).get('href'),
            link=links.get('html', {}).get('href')
        )

    async def request(
            self, method: str, url: str,
            params: Dict[str, str] = None, headers: Dict[str, str] = None, **aio_kwargs) -> ClientResponse:
        """Request OAuth2 resource."""
        url = self._get_url(url)
        if self.access_token:
            headers = headers or {'Accept': 'application/json'}
            headers['Authorization'] = "Bearer {}".format(self.access_token)
            auth = None
        else:
            auth = BasicAuth(self.client_id, self.client_secret)
            headers = headers or {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            }
        return await self.aiohttp_session.request(
            method, url, params=params, headers=headers, auth=auth, **aio_kwargs
        )


class Flickr(OAuth1Client):

    """Support Flickr.
    * Dashboard: https://www.flickr.com/services/apps/
    * Docs: https://www.flickr.com/services/api/auth.oauth.html
    * API reference: https://www.flickr.com/services/api/
    """

    access_token_url = 'http://www.flickr.com/services/oauth/request_token'
    authorize_url = 'http://www.flickr.com/services/oauth/authorize'
    base_url = 'https://api.flickr.com/'
    name = 'flickr'
    request_token_url = 'http://www.flickr.com/services/oauth/request_token'
    user_info_url = 'http://api.flickr.com/services/rest?method=flickr.test.login&format=json&nojsoncallback=1'  # noqa

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        user_ = data.get('user', {})
        first_name, _, last_name = data.get('fullname', {}).get('_content', '').partition(' ')
        return UserInfo(
            id=data.get('user_nsid') or user_.get('id'),
            username=user_.get('username', {}).get('_content'),
            first_name=first_name,
            last_name=last_name
        )


class Meetup(OAuth1Client):

    """Support Meetup.
    * Dashboard: http://www.meetup.com/meetup_api/oauth_consumers/
    * Docs: http://www.meetup.com/meetup_api/auth/#oauth
    * API: http://www.meetup.com/meetup_api/docs/
    """

    access_token_url = 'https://api.meetup.com/oauth/access/'
    authorize_url = 'http://www.meetup.com/authorize/'
    base_url = 'https://api.meetup.com/2/'
    name = 'meetup'
    request_token_url = 'https://api.meetup.com/oauth/request/'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        return UserInfo(
            id=data.get('id') or data.get('member_id'),
            locale=data.get('lang'),
            picture=data.get('photo', {}).get('photo_link')
        )


class Plurk(OAuth1Client):

    """Support Plurk.
    * Dashboard: http://www.plurk.com/PlurkApp/
    * API: http://www.plurk.com/API
    * API explorer: http://www.plurk.com/OAuth/test/
    """

    access_token_url = 'http://www.plurk.com/OAuth/access_token'
    authorize_url = 'http://www.plurk.com/OAuth/authorize'
    base_url = 'http://www.plurk.com/APP/'
    name = 'plurk'
    request_token_url = 'http://www.plurk.com/OAuth/request_token'
    user_info_url = 'http://www.plurk.com/APP/Profile/getOwnProfile'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        _user = data.get('user_info', {})
        _id = _user.get('id') or _user.get('uid')
        first_name, _, last_name = _user.get('full_name', '').partition(' ')
        city, country = map(lambda s: s.strip(), _user.get('location', ',').split(','))
        return UserInfo(
            id=_id,
            locale=_user.get('default_lang'),
            username=_user.get('display_name'),
            first_name=first_name,
            last_name=last_name,
            picture='http://avatars.plurk.com/{0}-big2.jpg'.format(_id),
            city=city,
            country=country
        )


class TwitterClient(OAuth1Client):

    """Support Twitter.
    * Dashboard: https://dev.twitter.com/apps
    * Docs: https://dev.twitter.com/docs
    * API reference: https://dev.twitter.com/docs/api
    """

    access_token_url = 'https://api.twitter.com/oauth/access_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'
    base_url = 'https://api.twitter.com/1.1/'
    name = 'twitter'
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    user_info_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        first_name, _, last_name = data['name'].partition(' ')
        city, _, country = map(lambda s: s.strip(), data.get('location', '').partition(','))
        return UserInfo(
            id=data.get('id') or data.get('user_id'),
            first_name=first_name,
            last_name=last_name,
            picture=data.get('profile_image_url'),
            locale=data.get('lang'),
            link=data.get('url'),
            username=data.get('screen_name'),
            city=city,
            country=country
        )


class TumblrClient(OAuth1Client):

    """Support Tumblr.
    * Dashboard: http://www.tumblr.com/oauth/apps
    * Docs: http://www.tumblr.com/docs/en/api/v2#auth
    * API reference: http://www.tumblr.com/docs/en/api/v2
    """

    access_token_url = 'http://www.tumblr.com/oauth/access_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    base_url = 'https://api.tumblr.com/v2/'
    name = 'tumblr'
    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    user_info_url = 'http://api.tumblr.com/v2/user/info'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        _user = data.get('response', {}).get('user', {})
        return UserInfo(
            id=_user.get('name'),
            username=_user.get('name'),
            link=_user.get('blogs', [{}])[0].get('url')
        )


class VimeoClient(OAuth1Client):

    """Support Vimeo."""

    access_token_url = 'https://vimeo.com/oauth/access_token'
    authorize_url = 'https://vimeo.com/oauth/authorize'
    base_url = 'https://vimeo.com/api/rest/v2/'
    name = 'vimeo'
    request_token_url = 'https://vimeo.com/oauth/request_token'
    user_info_url = 'http://vimeo.com/api/rest/v2?format=json&method=vimeo.oauth.checkAccessToken'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        _user = data.get('oauth', {}).get('user', {})
        first_name, _, last_name = _user.get('display_name').partition(' ')
        return UserInfo(
            id=_user.get('id'),
            username=_user.get('username'),
            first_name=first_name,
            last_name=last_name
        )


class YahooClient(OAuth1Client):

    """Support Yahoo.
    * Dashboard: https://developer.vimeo.com/apps
    * Docs: https://developer.vimeo.com/apis/advanced#oauth-endpoints
    * API reference: https://developer.vimeo.com/apis
    """

    access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
    authorize_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'
    base_url = 'https://query.yahooapis.com/v1/'
    name = 'yahoo'
    request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
    user_info_url = ('https://query.yahooapis.com/v1/yql?q=select%20*%20from%20'
                     'social.profile%20where%20guid%3Dme%3B&format=json')

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        _user = data.get('query', {}).get('results', {}).get('profile', {})
        city, country = map(lambda s: s.strip(), _user.get('location', ',').split(','))
        emails = _user.get('emails')
        main_email = ''
        if isinstance(emails, list):
            for email in emails:
                if 'primary' in list(email.keys()):
                    main_email = email.get('handle')
        elif isinstance(emails, dict):
            main_email = emails.get('handle')
        return UserInfo(
            id=_user.get('guid'),
            username=_user.get('username'),
            link=_user.get('profileUrl'),
            picture=_user.get('image', {}).get('imageUrl'),
            city=city,
            country=country,
            email=main_email
        )


class AmazonClient(OAuth2Client):

    """Support Amazon.
    * Dashboard: https://developer.amazon.com/lwa/sp/overview.html
    * Docs: https://developer.amazon.com/public/apis/engage/login-with-amazon/docs/conceptual_overview.html # noqa
    * API reference: https://developer.amazon.com/public/apis
    """

    access_token_url = 'https://api.amazon.com/auth/o2/token'
    authorize_url = 'https://www.amazon.com/ap/oa'
    base_url = 'https://api.amazon.com/'
    name = 'amazon'
    user_info_url = 'https://api.amazon.com/user/profile'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from provider."""
        return UserInfo(
            id=data.get('user_id')
        )


class EventbriteClient(OAuth2Client):

    """Support Eventbrite.
    * Dashboard: http://www.eventbrite.com/myaccount/apps/
    * Docs: https://developer.eventbrite.com/docs/auth/
    * API: http://developer.eventbrite.com/docs/
    """

    access_token_url = 'https://www.eventbrite.com/oauth/token'
    authorize_url = 'https://www.eventbrite.com/oauth/authorize'
    base_url = 'https://www.eventbriteapi.com/v3/'
    name = 'eventbrite'
    user_info_url = 'https://www.eventbriteapi.com/v3/users/me'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from provider."""
        for email in data.get('emails', []):
            if email.get('primary'):
                return UserInfo(
                    id=email.get('email'),
                    email=email.get('email')
                )
        return UserInfo()


class FacebookClient(OAuth2Client):

    """Support Facebook.
    * Dashboard: https://developers.facebook.com/apps
    * Docs: http://developers.facebook.com/docs/howtos/login/server-side-login/
    * API reference: http://developers.facebook.com/docs/reference/api/
    * API explorer: http://developers.facebook.com/tools/explorer
    """

    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    authorize_url = 'https://www.facebook.com/dialog/oauth'
    base_url = 'https://graph.facebook.com/v2.4'
    name = 'facebook'
    user_info_url = 'https://graph.facebook.com/me'

    async def user_info(self, **kwargs) -> Tuple[UserInfo, Dict]:
        """Facebook required fields-param."""
        params = kwargs.get('params', {})
        params['fields'] = 'id,email,first_name,last_name,name,link,locale,gender,location'
        return await super(FacebookClient, self).user_info(params=params, **kwargs)

    @staticmethod
    def user_parse(data):
        """Parse information from provider."""
        id_ = data.get('id')
        location = data.get('location', {}).get('name')
        city, country = '', ''
        if location:
            split_location = location.split(', ')
            city = split_location[0].strip()
            if len(split_location) > 1:
                country = split_location[1].strip()
        return UserInfo(
            id=id_,
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('name'),
            picture='http://graph.facebook.com/{0}/picture?type=large'.format(id_),
            link=data.get('link'),
            locale=data.get('locale'),
            gender=data.get('gender'),
            city=city,
            country=country
        )


class FoursquareClient(OAuth2Client):

    """Support Foursquare.
    * Dashboard: https://foursquare.com/developers/apps
    * Docs: https://developer.foursquare.com/overview/auth.html
    * API reference: https://developer.foursquare.com/docs/
    """

    access_token_url = 'https://foursquare.com/oauth2/access_token'
    authorize_url = 'https://foursquare.com/oauth2/authenticate'
    base_url = 'https://api.foursquare.com/v2/'
    name = 'foursquare'
    user_info_url = 'https://api.foursquare.com/v2/users/self'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        user = data.get('response', {}).get('user', {})
        city, country = user.get('homeCity', ', ').split(', ')
        return UserInfo(
            id=user.get('id'),
            email=user.get('contact', {}).get('email'),
            first_name=user.get('firstName'),
            last_name=user.get('lastName'),
            city=city,
            country=country
        )


class GithubClient(OAuth2Client):

    """Support Github.
    * Dashboard: https://github.com/settings/applications/
    * Docs: http://developer.github.com/v3/#authentication
    * API reference: http://developer.github.com/v3/
    """

    access_token_url = 'https://github.com/login/oauth/access_token'
    authorize_url = 'https://github.com/login/oauth/authorize'
    base_url = 'https://api.github.com'
    name = 'github'
    user_info_url = 'https://api.github.com/user'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from provider."""
        first_name, _, last_name = (data.get('name') or '').partition(' ')
        location = data.get('location', '')
        city, country = '', ''
        if location:
            split_location = location.split(',')
            country = split_location[0].strip()
            if len(split_location) > 1:
                city = split_location[1].strip()
        return UserInfo(
            id=data.get('id'),
            email=data.get('email'),
            first_name=first_name,
            last_name=last_name,
            username=data.get('login'),
            picture=data.get('avatar_url'),
            link=data.get('html_url'),
            city=city,
            country=country
        )


class VKClient(OAuth2Client):

    """Support vk.com.
    * Dashboard: http://vk.com/editapp?id={consumer_key}
    * Docs: http://vk.com/developers.php?oid=-17680044&p=Authorizing_Sites
    * API reference: http://vk.com/developers.php?oid=-17680044&p=API_Method_Description
    """

    authorize_url = 'http://api.vk.com/oauth/authorize'
    access_token_url = 'https://api.vk.com/oauth/access_token'
    user_info_url = 'https://api.vk.com/method/getProfiles?fields=uid,first_name,last_name,nickname,sex,bdate,city,country,timezone,photo_big'  # noqa
    name = 'vk'
    base_url = 'https://api.vk.com'

    def __init__(self, *args, **kwargs):
        """Set default scope."""
        super(VKClient, self).__init__(*args, **kwargs)
        self.params.setdefault('scope', 'offline')

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from provider."""
        resp = data.get('response', [{}])[0]
        return UserInfo(
            id=resp.get('uid'),
            first_name=resp.get('first_name'),
            last_name=resp.get('last_name'),
            username=resp.get('nickname'),
            city=resp.get('city'),
            country=resp.get('country'),
            picture=resp.get('photo_big')
        )


class OdnoklassnikiClient(OAuth2Client):

    """Support ok.ru.
    * Dashboard: http://ok.ru/dk?st.cmd=appsInfoMyDevList
    * Docs: https://apiok.ru/wiki/display/api/Authorization+OAuth+2.0
    * API reference: https://apiok.ru/wiki/pages/viewpage.action?pageId=49381398
    """

    authorize_url = 'https://connect.ok.ru/oauth/authorize'
    access_token_url = 'https://api.odnoklassniki.ru/oauth/token.do'
    user_info_url = 'http://api.ok.ru/api/users/getCurrentUser?fields=uid,first_name,last_name,gender,city,country,pic128max'  # noqa
    name = 'odnoklassniki'
    base_url = 'https://api.ok.ru'

    def __init__(self, *args, **kwargs):
        """Set default scope."""
        super().__init__(*args, **kwargs)
        self.params.setdefault('scope', 'offline')

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from provider."""
        resp = data.get('response', [{}])[0]
        location = resp.get('location', {})
        return UserInfo(
            id=resp.get('uid'),
            first_name=resp.get('first_name'),
            last_name=resp.get('last_name'),
            city=location.get('city'),
            country=location.get('country'),
            picture=resp.get('pic128max')
        )


class YandexClient(OAuth2Client):

    """Support Yandex.
    * Dashboard: https://oauth.yandex.com/client/my
    * Docs: http://api.yandex.com/oauth/doc/dg/reference/obtain-access-token.xml
    """

    access_token_url = 'https://oauth.yandex.com/token'
    access_token_key = 'oauth_token'
    authorize_url = 'https://oauth.yandex.com/authorize'
    base_url = 'https://login.yandex.ru/info'
    name = 'yandex'
    user_info_url = 'https://login.yandex.ru/info'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from provider."""
        return UserInfo(
            id=data.get('id'),
            username=data.get('login'),
            email=data.get('default_email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            picture=f"https://avatars.yandex.net/get-yapic/{data.get('default_avatar_id', 0)}/islands-200"
        )


class LinkedinClient(OAuth2Client):

    """Support linkedin.com.
    * Dashboard: https://www.linkedin.com/developer/apps
    * Docs: https://developer.linkedin.com/docs/oauth2
    * API reference: https://developer.linkedin.com/docs/rest-api
    """

    name = 'linkedin'
    access_token_key = 'oauth2_access_token'
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    authorize_url = 'https://www.linkedin.com/oauth/v2/authorization'
    user_info_url = (
        'https://api.linkedin.com/v1/people/~:('
        'id,email-address,first-name,last-name,formatted-name,picture-url,'
        'public-profile-url,location)?format=json'
    )

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse user data."""
        return UserInfo(
            id=data.get('id'),
            email=data.get('emailAddress'),
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            username=data.get('formattedName'),
            picture=data.get('pictureUrl'),
            link=data.get('publicProfileUrl'),
            country=data.get('location', {}).get('name')
        )


class PinterestClient(OAuth2Client):

    """Support pinterest.com.
    * Dashboard: https://developers.pinterest.com/apps/
    * Docs: https://developers.pinterest.com/docs/api/overview/
    """

    name = 'pinterest'
    access_token_url = 'https://api.pinterest.com/v1/oauth/token'
    authorize_url = 'https://api.pinterest.com/oauth/'
    user_info_url = 'https://api.pinterest.com/v1/me/'

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse user data."""
        data = data.get('data', {})
        return UserInfo(
            id=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            link=data.get('url')
        )


class DiscordClient(OAuth2Client):
    """Support Discord.
    * Dashboard: https://discordapp.com/developers/applications/me
    * Docs: https://discordapp.com/developers/docs/intro
    * API reference: https://discordapp.com/developers/docs/reference
    """

    name = 'discord'
    access_token_url = 'https://discordapp.com/api/oauth2/token'
    authorize_url = 'https://discordapp.com/api/oauth2/authorize'
    base_url = 'https://discordapp.com/api/'
    user_info_url = 'https://discordapp.com/api/users/@me'

    def __init__(self, *args, **kwargs):
        """Set default scope."""
        super(DiscordClient, self).__init__(*args, **kwargs)
        self.params.setdefault('scope', 'email')

    async def request(
            self, method: str, url: str,
            params: Dict[str, str] = None, headers: Dict[str, str] = None, **aio_kwargs) -> ClientResponse:
        """Request OAuth2 resource."""
        if self.access_token:
            headers = headers or {}
            headers['Authorization'] = "Bearer {}".format(self.access_token)
        return await self.aiohttp_session.request(
            method, url, params=params, headers=headers, **aio_kwargs
        )

    @classmethod
    def user_parse(cls, data) -> UserInfo:
        """Parse information from the provider."""
        return UserInfo(
            id=data.get('id'),
            username=data.get('username'),
            discriminator=data.get('discriminator'),
            avatar=data.get('avatar'),
            verified=data.get('verified'),
            email=data.get('email')
        )
