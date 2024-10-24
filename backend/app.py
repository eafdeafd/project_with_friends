from litestar import Litestar, Response, get
from litestar.response import Stream
from lib.bedrock import BedrockClient, BedrockAgent
from lib.sample import stream_sample
from litestar.serialization import encode_json
from litestar.config.cors import CORSConfig

from typing import Optional

def get_bedrock_client(app: Litestar) -> BedrockClient:
    app.state.bedrock_client = BedrockClient()
    return app.state.bedrock_client

def get_bedrock_agent(app: Litestar) -> BedrockAgent:
    app.state.bedrock_agent = BedrockAgent()
    return app.state.bedrock_agent

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
async def sample_query(prompt: Optional[str]=None, session_id: Optional[str]=None) -> Stream:
    async def stream_sample_wrapper(prompt: str):
        for i, chunk in enumerate(stream_sample(prompt)):
            yield encode_json({ "chunk_id": i, "session_id": "4bd3ac5-6e2b-4276-970e-dc97a977e51a", "response": chunk })

    return Stream(stream_sample_wrapper(prompt), media_type="application/json")

@get("/query_agent")
async def query_agent(prompt: str, session_id: Optional[str]=None) -> Stream:
    async def stream_agent_wrapper(prompt: str, session_id: Optional[str]):
        for i, (chunk, ret_session_id) in enumerate(app.state.bedrock_agent.invoke_agent(session_id, prompt)):
            yield encode_json({ "chunk_id": i, "session_id": ret_session_id, "response": chunk })

    return Stream(stream_agent_wrapper(prompt, session_id), media_type="application/json")

cors_config = CORSConfig(allow_origins=["http://localhost:3000"])
app = Litestar(on_startup=[get_bedrock_client, get_bedrock_agent], route_handlers=[hello_world, query_model, sample_query, query_agent], cors_config=cors_config)

# Query looks something like this in Python
# def get_stream(url, prompt):
#     s = requests.Session()
#     params = {"prompt": prompt}
#     with s.get(url + "query_model", params=params, headers=None, stream=True) as resp:
#         for line in resp.iter_lines():
#             if line:
#                 print(line)
