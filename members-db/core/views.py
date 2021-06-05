import logging

from urllib import parse
from aiohttp_session import new_session, get_session
from aiohttp import web, FormData
import aiohttp_jinja2

from db.token import create_nonce_token, create_state_token, is_token_valid
from db.allowed_account import is_account_allowed
from db.user import add_user_info


class SiteHandler:

    def __init__(self):
        self.errors = {
            'login_timeout': {
                'head': 'Přihlášení selhalo!',
                'body': 'Vypršela platnost spojení.',
            },
            'login_authorization': {
                'head': 'Přihlášení selhalo!',
                'body': 'Chyba autorizace.',
            },
            'login_not_allowed': {
                'head': 'Přihlášení selhalo!',
                'body': 'Zřejmě nejste členem klubu.'
            },
        }
        pass

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):

        if request.query.get('error'):
            return {'error': self.errors[request.query.get('error')]}

        return {}

    async def auth_login(self, request):

        user_session = await new_session(request)
        state_token = await create_state_token(request.app['db_session'])
        nonce_token = await create_nonce_token(request.app['db_session'])
        user_session['nonce'] = nonce_token

        uri = request.app['aiogoogle'].openid_connect.authorization_url(
            include_granted_scopes=True,
            state=state_token,
            nonce=nonce_token
        )
        return web.HTTPTemporaryRedirect(location=uri)

    async def auth_callback(self, request):

        user_session = await get_session(request)

        valid_state = await is_token_valid(request.app['db_session'], request.query.get('state'), 'state')
        valid_nonce = await is_token_valid(request.app['db_session'], user_session['nonce'], 'nonce')

        if not valid_state or not valid_nonce:
            logging.warning('OAuth2: Timeout on tokens.')
            return web.HTTPTemporaryRedirect(
                location='/?' + parse.urlencode({'error': 'login_timeout'}))

        elif not request.query.get('code'):
            loggin.warning('OAuth2: Authorization failed.')
            return web.HTTPTemporaryRedirect(
                location='/?' + parse.urlencode({'error': 'login_authorization'}))

        full_user_creds = await request.app['aiogoogle'].openid_connect.build_user_creds(
            grant=request.query.get('code'),
            nonce=user_session['nonce'],
            verify=True
        )
        # TODO
        logging.info(full_user_creds)

        google_granted_email = full_user_creds['id_token']['email']
        if not await is_account_allowed(request.app['db_session'], google_granted_email):
            logging.warning('OAuth2: Not allowed user [%s]', google_granted_email)
            return web.HTTPTemporaryRedirect(
                location='/?' + parse.urlencode({'error': 'login_not_allowed'}))

        await add_user_info(
            request.app['db_session'],
            full_user_creds['id_token']['email'],
            full_user_creds['id_token']['name'],
            full_user_creds['id_token']['given_name'],
            full_user_creds['id_token']['family_name'],
            full_user_creds['id_token']['picture']
        )

        return web.HTTPTemporaryRedirect(location='/')
