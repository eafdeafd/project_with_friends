from litestar import Litestar, get
from litestar.response import Stream
from lib.bedrock import BedrockClient
from lib.sample import stream_sample

def get_bedrock_client(app: Litestar) -> BedrockClient:
    app.state.bedrock_client = BedrockClient()
    return app.state.bedrock_client

@get("/")
async def hello_world() -> str:
    return "Hello, world!"

@get("/query_model")
async def query_model(prompt: str) -> str:
    bedrock_client = app.state.bedrock_client
    return Stream(bedrock_client.stream_bedrock_response(prompt))

@get("/sample_query")
async def sample_query(prompt: str) -> str:
    return Stream(stream_sample(prompt))

app = Litestar(on_startup=[get_bedrock_client], route_handlers=[hello_world, query_model, sample_query])

# Query looks something like this in Python
# def get_stream(url, prompt):
#     s = requests.Session()
#     params = {"prompt": prompt}
#     with s.get(url + "query_model", params=params, headers=None, stream=True) as resp:
#         for line in resp.iter_lines():
#             if line:
#                 print(line)