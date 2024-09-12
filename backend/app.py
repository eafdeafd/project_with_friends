from litestar import Litestar, get

@get("/")
async def hello_world() -> str:
    return "Hello, world!"

app = Litestar(route_handlers=[hello_world])