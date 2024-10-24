from typing import Optional
from uuid import uuid4

from aiohttp import ClientError
import boto3
import json

# Initialize the boto3 Bedrock client
class BedrockClient:
    def __init__(self, region_name="us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region_name)

    def stream_bedrock_response(self, prompt, model_id='amazon.titan-text-lite-v1'):
        payload = {
            "inputText": prompt,
            "textGenerationConfig" : {
                "maxTokenCount": 200,  # Adjust maxTokenCount for longer or shorter responses
                "temperature": 0.7  # Adjust the temperature for more or less randomness
            }
        }
        
        response = self.client.invoke_model_with_response_stream(
            modelId=model_id,
            body=json.dumps(payload)
        )

        # Stream of the response chunks
        for event in response["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if "outputText" in chunk:
                yield chunk["outputText"]

class BedrockAgent:
    def __init__(self):
        self.runtime_client = boto3.client(
            service_name="bedrock-agent-runtime", region_name="eu-west-2"
        )
    
    def invoke_agent(self, session_id: Optional[str], prompt):
        """
        Sends a prompt for the agent to process and respond to.

        :param agent_id: The unique identifier of the agent to use.
        :param agent_alias_id: The alias of the agent to use.
        :param session_id: The unique identifier of the session. Use the same value across requests
                           to continue the same conversation.
        :param prompt: The prompt that you want Claude to complete.
        :return: Inference response from the model.
        """

        if session_id is None:
            session_id = str(uuid4())

        try:
            response = self.runtime_client.invoke_agent(
                agentId="R6DHLURAZG",
                agentAliasId="ITQRSRJ1EX",
                sessionId=session_id,
                inputText=prompt,
            )

            for event in response.get("completion"):
                chunk = event["chunk"]
                yield chunk["bytes"].decode("utf-8"), session_id

        except ClientError as e:
            print(f"Couldn't invoke agent. {e}")
            raise