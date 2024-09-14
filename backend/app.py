from litestar import Litestar, get
from litestar.response import Stream
from lib.bedrock import BedrockClient

def get_bedrock_client(app: Litestar) -> BedrockClient:
    app.state.bedrock_client = BedrockClient()
    return app.state.bedrock_client

@get("/")
async def hello_world() -> str:
    return "Hello, world!"

@get("/query_model")
async def query_model(prompt: str) -> str:
    bedrock_client = app.state.bedrock_client
    def response_stream():
        for chunk in bedrock_client.stream_bedrock_response(prompt):
            yield chunk

    return Stream(response_stream())

app = Litestar(on_startup=[get_bedrock_client], route_handlers=[hello_world, query_model])

# Query looks something like this in Python
# def get_stream(url, prompt):
#     s = requests.Session()
#     params = {"prompt": prompt}
#     with s.get(url + "query_model", params=params, headers=None, stream=True) as resp:
#         for line in resp.iter_lines():
#             if line:
#                 print(line)