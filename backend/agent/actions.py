import boto3
import pandas as pd 

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

bucket_name = "vlr-data"
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket(bucket_name)

def query_aggregated_data(player_name="all", bracket=["vct-challengers", "vct-international", "game-changers"], region="all", past_games="all", agent="all"):
    # Argument assertions
    filePath = "aggregated_data.csv"
    object = bucket.Object(filePath)
    df = pd.read_csv(object.get()['Body'])

    ddf = df.copy()
    for b in bracket:
        if b not in ["vct-challengers", "vct-international", "game-changers"]:
            raise ValueError(f"brackets needs to be valid, {b} not in brackets")
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if player_name != 'all':
        ddf = ddf.loc[ddf['player_name'].astype(str) == player_name]
    ddf = ddf.loc[df['bracket'].isin(bracket)] # does not respect index order which is why is last. everything else does.
    return ddf

def query_unaggregated_data(player_name="all", bracket=["vct-challengers", "vct-international", "game-changers"], region="all", past_games="all", agent="all"):
    # Argument assertions
    filePath = "unaggregated_data.csv"
    object = bucket.Object(filePath)
    df = pd.read_csv(object.get()['Body'])

    ddf = df.copy()
    for b in bracket:
        if b not in ["vct-challengers", "vct-international", "game-changers"]:
            raise ValueError(f"brackets needs to be valid, {b} not in brackets")
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if player_name != 'all':
        ddf = ddf.loc[ddf['player_name'].astype(str) == player_name]
    if agent != 'all':
        ddf = ddf.loc[ddf['player_agent'] == agent]
    if past_games != 'all':
        ddf = ddf[-int(past_games):]
    ddf = ddf.loc[df['bracket'].isin(bracket)] # does not respect index order which is why is last. everything else does.
    return ddf