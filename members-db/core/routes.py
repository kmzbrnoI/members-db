

def setup_routes(app, handler, static_root):
    router = app.router
    router.add_get('/', handler.index, name='index')
    router.add_get('/auth/login', handler.auth_login, name='auth_login')
    router.add_get('/auth/callback', handler.auth_callback, name='auth_callback')
    router.add_get('/user/add', handler.user_add, name='user_add')
    router.add_post('/user/check', handler.user_check, name='user_check')
    router.add_static('/static/', path=static_root, name='static')
