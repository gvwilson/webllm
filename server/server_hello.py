from fasthtml.common import FastHTML

app = FastHTML()


@app.get("/")
async def index():
    return "Hello from the Sasquatch Observatory!"
