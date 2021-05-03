import logging

from aiohttp import web, FormData
import aiohttp_jinja2

from db.user import create_user

class SiteHandler:

    def __init__(self):
        pass

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {}
