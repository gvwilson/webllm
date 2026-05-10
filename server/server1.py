from litestar import Litestar, get


@get("/")
async def index() -> str:
    return "Hello from the Sasquatch Observatory!"


app = Litestar([index])
