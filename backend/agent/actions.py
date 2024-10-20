import json

import boto3

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

roles = ["duelist", "sentinel", "controller", "initiator"]

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

def build_team(team_condition, player_data):
    """
    Returns a 5-player Valorant roster
    """
    context = ""
    for role in roles:
        context += get_top_players_by_role(team_condition, role, player_data)

    prompt = f"""Use the following pieces of context to answer the question at the end.

    {player_data}

    Question: {f"Build a 5-man team with the top players in each role for {team_condition}. 
    Ensure that the team composition is balanced in terms of roles and that it has exactly one in-game leader(IGL). "}""
    Answer:"""

    generated_text = call_titan(prompt)
    print(generated_text)

    return generated_text

def get_top_players_by_role(team_condition, role, player_data):
    """
    Returns the top 3 players in a role for the given team setting using the player data.
    """
    prompt = f"""Use the following pieces of context to answer the question at the end.

    {player_data}

    Question: {f"Find the top 3 {role} players that play in {team_condition}."}"
    Answer:"""

    generated_text = call_titan(prompt)
    print(generated_text)

    resp_string = (
        f"\n The top 3 players that play {role} in {team_condition} are: \n" +
        generated_text
    )

    return resp_string