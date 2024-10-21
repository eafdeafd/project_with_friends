import json
import boto3
import pandas as pd 

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

bucket_name = "vlr-data"
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket(bucket_name)

roles = ["duelist", "sentinel", "controller", "initiator"]

def call_claude_sonnet(prompt):

    prompt_config = {
        "anthropic_version": "bedrock-2024-02-29",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }

    body = json.dumps(prompt_config)

    modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    accept = "application/json"
    contentType = "application/json"

    print("Invoking Claude Sonnet")
    try:
        response = bedrock_runtime.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
    except Exception as ex:
        print(f"Error: {ex}")

    print("Received response from Claude Sonnet")
    response_body = json.loads(response.get("body").read())

    results = response_body.get("content")[0].get("text")
    return results

# Call Titan model
def call_titan(prompt):
    prompt_config = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 3072,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 1,
        },
    }

    body = json.dumps(prompt_config)

    modelId = "amazon.titan-text-premier-v1:0"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    results = response_body.get("results")[0].get("outputText")
    return results

def query_data(bracket, region, past_games, player_name, agent):
    # Load the JSON file from the S3 bucket
    obj = bucket.Object("unaggregated_data.json")

    data = []
    for line in obj.get()['Body'].iter_lines():
        if line:
            data.append(json.loads(line))

    # Convert the JSON data to a Pandas DataFrame
    df = pd.json_normalize(data)

    # Argument assertions
    if bracket not in ["vct-challengers", "vct-international", "game-changers"]:
        raise ValueError(f"brackets needs to be valid, {bracket} not in brackets")

    # get region
    if region != 'all':
        all_by_region = df.loc[df['region'] == region]
    else:
        all_by_region = df

    # get player_name
    if player_name != 'all':
        by_region_and_player_id = all_by_region.loc[all_by_region['player_name'].astype(str) == player_name]
    else:
        by_region_and_player_id = all_by_region

    # get agent
    if agent != 'all':
        by_region_and_player_id_and_agent = by_region_and_player_id.loc[by_region_and_player_id['player_agent'] == agent]
    else:
        by_region_and_player_id_and_agent = by_region_and_player_id

    # get number of past games
    if past_games != 'all':
        filtered_by_everything = by_region_and_player_id_and_agent[-int(past_games):]
    else:
        filtered_by_everything = by_region_and_player_id_and_agent

    # this does not respect order, but we have the past n games already so ok!
    filtered_by_everything = filtered_by_everything.loc[df['bracket'] == bracket]

    result_json = filtered_by_everything.to_json()

    return result_json

def build_team(bracket):
    """
    Returns a 5-player Valorant roster with the top players in each role.
    """

    obj = bucket.Object("aggregated_data.json")
    # Truncate content to meet the model input limit
    context = obj.get()['Body'].read().decode('utf-8')[:149000]

    prompt = f"""Use the following pieces of context to answer the question at the end.

    {context}

    Question: {f"""Analyze the player data to build the best five-person Valorant team with the top players in each role from {bracket}. 
               Ensure that the team composition is balanced in terms of roles and has exactly one in-game leader(IGL). 
               Consider factors such as team synergy, individual skill, winrate, KDA, win rate, clutches, first bloods, etc. 
               Also ensure that the team has at least one player who frequently uses the Operator.
               For each chosen player in the team, justify their inclusion using statistics and recent performances."""} Answer:"""

    generated_text = call_titan(prompt)

    return generated_text