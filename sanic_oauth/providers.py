from .core import OAuth2Client, UserInfo

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Development"


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
    user_info_url = 'https://www.googleapis.com/plus/v1/people/me'

    @classmethod
    async def user_parse(cls, data) -> UserInfo:
        """Parse information from provider."""
        email = next(filter(lambda x: x['type'] == 'account', data.get('emails', [])), {'value': ''})
        return UserInfo(
            id=data.get('sub') or data.get('id'),
            email=email['value'],
            username=data.get('nickname'),
            first_name=data.get('name', {}).get('givenName'),
            last_name=data.get('name', {}).get('familyName'),
            locale=data.get('language'),
            link=data.get('url'),
            picture=data.get('image', {}).get('url')
        )
