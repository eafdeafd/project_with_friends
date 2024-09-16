from litestar import Litestar, Response, get
from litestar.response import Stream
from lib.bedrock import BedrockClient
from lib.sample import stream_sample
from litestar.serialization import encode_json

from typing import Optional

def get_bedrock_client(app: Litestar) -> BedrockClient:
    app.state.bedrock_client = BedrockClient()
    return app.state.bedrock_client

@get("/")
async def hello_world() -> str:
    return "Hello, world!"

@get("/query_model")
async def query_model(prompt: str) -> Stream:
    async def stream_model_wrapper(prompt: str):
        for i, chunk in enumerate(app.state.bedrock_client.stream_bedrock_response(prompt)):
            yield encode_json({ "chunk_id": i, "response": chunk })
    
    return Stream(stream_model_wrapper(prompt), media_type="application/json")

@get("/sample_query")
async def sample_query(prompt: Optional[str]=None) -> Stream:
    async def stream_sample_wrapper(prompt: str):
        for i, chunk in enumerate(stream_sample(prompt)):
            yield encode_json({ "chunk_id": i, "response": chunk })

    return Stream(stream_sample_wrapper(prompt), media_type="application/json")

app = Litestar(on_startup=[get_bedrock_client], route_handlers=[hello_world, query_model, sample_query])

# Query looks something like this in Python
# def get_stream(url, prompt):
#     s = requests.Session()
#     params = {"prompt": prompt}
#     with s.get(url + "query_model", params=params, headers=None, stream=True) as resp:
#         for line in resp.iter_lines():
#             if line:
#                 print(line)