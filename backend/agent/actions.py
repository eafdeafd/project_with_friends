import json

import boto3

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

# Call Titan model
def call_titan(prompt):
    prompt_config = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 4096,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 1,
        },
    }

    body = json.dumps(prompt_config)

    modelId = "amazon.titan-text-lite-v1"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    print(response_body)

    results = response_body.get("results")[0].get("outputText")
    return results


def get_top_players_by_role(team_setting, role, player_data):
    """
    Returns the top 3 players in a role for the given team setting using the player data.
    """
    prompt = f"""Use the following pieces of context to answer the question at the end.

    {player_data}

    Question: {f"Find the top 3 {role} players that play in {team_setting}."}"
    Answer:"""

    generated_text = call_titan(prompt)
    print(generated_text)

    resp_string = (
        f"\n The top 3 players that play {role} in {team_setting} are: \n" +
        generated_text
    )

    return resp_string