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
