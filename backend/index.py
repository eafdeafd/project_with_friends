from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from lib.bedrock import BedrockAgent
import json

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Initialize Bedrock client and agent
bedrock_agent = BedrockAgent()

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/query_agent', methods=['GET'])
def query_agent():
    prompt = request.args.get('prompt')
    session_id = request.args.get('session_id', None)

    def stream_agent_wrapper():
        for i, (chunk, ret_session_id) in enumerate(bedrock_agent.invoke_agent(session_id, prompt)):
            yield json.dumps({
                "chunk_id": i,
                "session_id": ret_session_id,
                "response": chunk
            }) + '\n'

    return Response(stream_agent_wrapper(), content_type='application/json')
