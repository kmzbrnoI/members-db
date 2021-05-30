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

        return {'theme': self.theme, 'user': 'user', 'cities': cities}

    async def auth_login(self, request):
        uri = request.app['aiogoogle'].oauth2.authorization_url(
            client_creds={
                'client_id': request.app['cfg']['google-auth']['client_id'],
                'client_secret':  request.app['cfg']['google-auth']['client_secret'],
                'scopes': [],
                'redirect_uri': 'http://celestian.cz:8080/auth/callback'
            },
        )
        return web.HTTPTemporaryRedirect(location=uri)

    @aiohttp_jinja2.template('user_add.html')
    async def user_add(self, request):
        return {'theme': self.theme}

    @aiohttp_jinja2.template('user_check.html')
    async def user_check(self, request):

        data = await request.post()
        login = data['user_email']
        logging.info(login)
        return {'theme': self.theme}
