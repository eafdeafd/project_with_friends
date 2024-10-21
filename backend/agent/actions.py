import json

import boto3

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

roles = ["duelist", "sentinel", "controller", "initiator"]

def claude_prompt_format(prompt: str) -> str:
    # Add headers to start and end of prompt
    return "\n\nHuman: " + prompt + "\n\nAssistant:"

def call_claude(prompt):
    prompt_config = {
        "prompt": claude_prompt_format(prompt),
        "max_tokens_to_sample": 4096,
        "temperature": 0.7,
        "top_k": 250,
        "top_p": 0.5,
        "stop_sequences": [],
    }

    body = json.dumps(prompt_config)

    modelId = "anthropic.claude-v2"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    results = response_body.get("completion")
    return results

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
    Returns a 5-player Valorant roster with the top players in each role.
    """
    context = ""
    for role in roles:
        context += get_top_players_by_role(team_condition, role, player_data)

    prompt = f"""Use the following pieces of context to answer the question at the end.

    {context}

    Question: {f"Build the best five-person Valorant team with the top players in each role. 
    Ensure that the team composition is balanced in terms of roles, has exactly one in-game leader(IGL), and meets the {team_condition}. 
    Consider factors such as team synergy, individual skill, winrate, and past tournament performances."}""
    Answer:"""

    generated_text = call_claude(prompt)
    print(generated_text)

    return generated_text

def get_top_players_by_role(team_condition, role, player_data):
    """
    Returns the top 10 players in a role for the given team setting using the player data.
    """
    prompt = f"""Use the following pieces of context to answer the question at the end.

    {player_data}

    Question: {f"Find the top 10 {role} players. Ensure that the players meet the {team_condition}.
               Consider factors such as KDA, win rate, clutches, first bloods, etc."}"
    Answer:"""

    generated_text = call_titan(prompt)
    print(generated_text)

    return generated_text