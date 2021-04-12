from aiohttp import web


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    age = request.match_info.get('age', "18")
    text = "Hello, " + name + "! You are " + age + " years old."
    return web.Response(text=text)


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle),
                web.get('/profi_dotaz/{name}/{age}', handle)])


if __name__ == '__main__':
    web.run_app(app)
