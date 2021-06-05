import logging

from aiohttp import web, FormData
import aiohttp_jinja2

from db.user import create_user

class SiteHandler:

    def __init__(self):
        self.theme = {
            'background': 'railway-station-4305749_1920.jpg',
        }

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        cities = [
            {'name': 'Brno', 'size': 350000},
            {'name': 'Hrušovany', 'size': 5000},
            {'name': 'Olomouc', 'size': 200000},
            {'name': 'Lipník', 'size': 15000},
            {'name': 'Přerov', 'size': 50000},
        ]

        await create_user(request.app['db_session'], 'Petr');

        return {'theme': self.theme, 'user': 'user', 'cities': cities, 'a_data': 'nothing'}

    async def auth_login(self, request):
        uri = request.app['aiogoogle'].openid_connect.authorization_url(
            include_granted_scopes=True,
            client_creds={
                'client_id': request.app['cfg']['google-auth']['client_id'],
                'client_secret':  request.app['cfg']['google-auth']['client_secret'],
                'scopes': [
                    'https://www.googleapis.com/auth/userinfo.profile',
                    'https://www.googleapis.com/auth/userinfo.email',
                    'openid'
                ],
                'redirect_uri': 'http://celestian.cz:8080/auth/callback'
            },
            nonce='haha_nonce'
        )
        return web.HTTPTemporaryRedirect(location=uri)

    @aiohttp_jinja2.template('index.html')
    async def auth_callback(self, request):
        # Here we request the access and refresh token
        if request.query.get('code'):
            full_user_creds = await request.app['aiogoogle'].openid_connect.build_user_creds(
                grant=request.query.get('code'),
                client_creds={
                    'client_id': request.app['cfg']['google-auth']['client_id'],
                    'client_secret':  request.app['cfg']['google-auth']['client_secret'],
                    'scopes': [
                        'https://www.googleapis.com/auth/userinfo.profile',
                        'https://www.googleapis.com/auth/userinfo.email',
                        'openid'
                    ],
                    'redirect_uri': 'http://celestian.cz:8080/auth/callback'
                },
                nonce='haha_nonce',
                verify=True
            )
            # Here, you should store full_user_creds in a db. Especially the refresh token and access token.
            logging.info(full_user_creds)

            # A dict having claims of the user e.g. the sub claim and iat claim.
            # Check https://developers.google.com/identity/protocols/oauth2/openid-connect#an-id-tokens-payload for more info
            full_user_info = await request.app['aiogoogle'].openid_connect.get_user_info(full_user_creds)
            logging.info(full_user_info)

            return {'theme': self.theme}

        else:
            # Should either receive a code or an error
            return {'theme': self.theme}

    @aiohttp_jinja2.template('user_add.html')
    async def user_add(self, request):
        return {'theme': self.theme}

    @aiohttp_jinja2.template('user_check.html')
    async def user_check(self, request):

        data = await request.post()
        login = data['user_email']
        logging.info(login)
        return {'theme': self.theme}
