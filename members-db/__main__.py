"""members-db

Usage:
  members-db init_db [--cfg=<config_file>]
  members-db run [--cfg=<config_file>]
  members-db (-h | --help)
  members-db --version

Options:
  --cfg=<config_file>   Configuration file [default: ./members-db.cfg].
  -h --help             Show this screen.
  --version             Show version.
"""

import os
import asyncio
from docopt import docopt
import logging
import configparser

from aiohttp import web
import jinja2
import aiohttp_jinja2
from aiogoogle import Aiogoogle

from db.tables import init_db, db_engine_ctx
from core.routes import setup_routes
from core.views import SiteHandler


STATIC_ROOT = os.path.abspath('./members-db/static')
TEMPLATES_ROOT = os.path.abspath('./members-db/templates')


async def init_app(config):

    app = web.Application()
    app['cfg'] = config

    loader = jinja2.FileSystemLoader(TEMPLATES_ROOT)
    aiohttp_jinja2.setup(app, loader=loader)

    app.cleanup_ctx.append(db_engine_ctx)

    handler = SiteHandler()
    setup_routes(app, handler, STATIC_ROOT)

    app['aiogoogle'] = Aiogoogle(client_creds=app['cfg']['google-auth']['client_secret'])

    return app


def configuration_setup(args):

    cfg = {}

    cfg_parser = configparser.ConfigParser()
    cfg_parser.read(args['--cfg'])

    for section in cfg_parser.sections():
        cfg[section] = {}
        for key in cfg_parser.options(section):
            cfg[section][key] = cfg_parser.get(section, key)

    if cfg['members-db']['log_level'] == 'debug':
        logging.basicConfig(level=logging.DEBUG)
    elif cfg['members-db']['log_level'] == 'info':
        logging.basicConfig(level=logging.INFO)
    elif cfg['members-db']['log_level'] == 'warning':
        logging.basicConfig(level=logging.WARNING)
    elif cfg['members-db']['log_level'] == 'error':
        logging.basicConfig(level=logging.ERROR)
    elif cfg['members-db']['log_level'] == 'critical':
        logging.basicConfig(level=logging.CRITICAL)
    else:
        logging.basicConfig(level=logging.INFO)
        logging.warning('Missing members-db/log_level in configuration file [%s]', args['--cfg'])

    cfg['google-auth']['scopes'] = ['https://www.googleapis.com/auth/userinfo.profile']

    db = cfg['db']  # pylint: disable-msg=C0103
    url = f"mariadb+aiomysql://{db['user']}:{db['pass']}@{db['host']}:{db['port']}/{db['name']}"
    cfg['db']['url'] = url

    return cfg


def main():

    args = docopt(__doc__, version='0.0.1')
    config = configuration_setup(args)

    if args['init_db']:
        try:
            asyncio.run(init_db(config))
        finally:
            logging.info('Successfully shutdown members-db.')

    if args['run']:
        app = init_app(config)
        web.run_app(app, port=config['web']['port_number'])


if __name__ == '__main__':
    main()
