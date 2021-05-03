

def setup_routes(app, handler, static_root):
    router = app.router
    router.add_get('/', handler.index, name='index')
    router.add_static('/static/', path=static_root, name='static')
