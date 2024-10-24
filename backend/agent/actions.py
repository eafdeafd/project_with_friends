import boto3
import pandas as pd 

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

bucket_name = "vlr-data"
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket(bucket_name)

def query_past_games(player_name, past_games=5, agent="all"):
    filePath = "unaggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()

    agents = [
    'Brimstone', 'Viper', 'Omen', 'Killjoy', 'Cypher', 'Sova', 'Sage', 'Phoenix', 'Jett', 'Reyna', 'Raze', 
    'Breach', 'Skye', 'Yoru', 'Astra', 'KAY/O', 'Chamber', 'Neon', 'Fade', 'Harbor', 'Gekko', 'Deadlock', 
    'Iso', 'Clove', 'Vyse'
    ]

    if agent != 'all' and agent not in agents:
        raise ValueError(f"Please select a valid agent from Brimstone, Viper, Omen, Killjoy, Cypher, Sova, Sage, Phoenix, Jett, Reyna, Raze, Breach, Skye, Yoru, Astra, KAY/O, Chamber, Neon, Fade, Harbor, Gekko, Deadlock, Iso, Clove, Vyse")
    
    
    ddf = ddf.loc[ddf['player_name'].astype(str) == player_name]
    if agent != 'all':
        ddf = ddf.loc[ddf['player_agent'] == agent]
    ddf = ddf[-past_games:]
    return ddf.to_json(orient='records')

def get_players_from_specifiers(role, bracket, region="all", agent="all", IGL=False):
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()
    if bracket not in ["vct-challengers", "vct-international", "game-changers"]:
        raise ValueError(f"Please select a valid bracket from vct-challengers, vct-international, game-changers")
    if role not in ['Duelist', 'Initiator', 'Controller', 'Sentinel']:
        raise ValueError(f"Please select a valid role from Duelist, Initiator, Controller, Sentinel")
    if region != 'all' and region not in ['NA', 'INTL', 'BR', 'LATAM', 'SEA', 'LAS', 'KR', 'JP', 'EMEA', 'VN', 'CN']:
        raise ValueError(f"Please select a valid role from NA, INTL, BR, LATAM, SEA, LAS, KR, JP, EMEA, VN, CN")
    agents = [
    'Brimstone', 'Viper', 'Omen', 'Killjoy', 'Cypher', 'Sova', 'Sage', 'Phoenix', 'Jett', 'Reyna', 'Raze', 
    'Breach', 'Skye', 'Yoru', 'Astra', 'KAY/O', 'Chamber', 'Neon', 'Fade', 'Harbor', 'Gekko', 'Deadlock', 
    'Iso', 'Clove', 'Vyse'
    ]

    if agent != 'all' and agent not in agents:
        raise ValueError(f"Please select a valid agent from Brimstone, Viper, Omen, Killjoy, Cypher, Sova, Sage, Phoenix, Jett, Reyna, Raze, Breach, Skye, Yoru, Astra, KAY/O, Chamber, Neon, Fade, Harbor, Gekko, Deadlock, Iso, Clove, Vyse")
    
    
    ddf = ddf[ddf['top_roles'].apply(lambda roles: role in roles)]
    ddf = ddf.loc[df['bracket'] == bracket]
    if IGL:
        ddf = ddf[ddf['IGL']]    
    #ddf = ddf[ddf['OPer']]
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if agent != 'all':
        ddf = ddf[ddf['top_3_agents'].apply(lambda roles: agent in roles)]
        
    return ddf.to_json(orient='records')

def query_player(player_name):
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()
    ddf = ddf.loc[ddf['player_name'].astype(str) == player_name]
    return ddf.to_json(orient='records')

'''

def query_duelists(bracket, region="all", agent="all"):
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()
    if bracket not in ["vct-challengers", "vct-international", "game-changers"]:
        raise ValueError(f"Please select a valid bracket from vct-challengers, vct-international, game-changers")
    ddf = ddf[ddf['top_roles'].apply(lambda roles: 'Duelist' in roles)]
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if agent != 'all':
        ddf = ddf[ddf['top_3_agents'].apply(lambda roles: agent in roles)]
    ddf = ddf.loc[df['bracket'] == bracket] 
    return ddf.to_json(orient='records')

def query_initiators(bracket, region="all", agent="all"):
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()
    if bracket not in ["vct-challengers", "vct-international", "game-changers"]:
        raise ValueError(f"Please select a valid bracket from vct-challengers, vct-international, game-changers")
    ddf = ddf[ddf['top_roles'].apply(lambda roles: 'Initiator' in roles)]
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if agent != 'all':
        ddf = ddf[ddf['top_3_agents'].apply(lambda roles: agent in roles)]
    ddf = ddf.loc[df['bracket'] == bracket] 
    return ddf.to_json(orient='records')

def query_controllers(bracket, region="all", agent="all"):
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()
    if bracket not in ["vct-challengers", "vct-international", "game-changers"]:
        raise ValueError(f"Please select a valid bracket from vct-challengers, vct-international, game-changers")
    ddf = ddf[ddf['top_roles'].apply(lambda roles: 'Controller' in roles)]
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if agent != 'all':
        ddf = ddf[ddf['top_3_agents'].apply(lambda roles: agent in roles)]
    ddf = ddf.loc[df['bracket'] == bracket] 
    return ddf.to_json(orient='records')

def query_sentinels(bracket, region="all", agent="all"):
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()
    if bracket not in ["vct-challengers", "vct-international", "game-changers"]:
        raise ValueError(f"Please select a valid bracket from vct-challengers, vct-international, game-changers")
    ddf = ddf[ddf['top_roles'].apply(lambda roles: 'Sentinel' in roles)]
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if agent != 'all':
        ddf = ddf[ddf['top_3_agents'].apply(lambda roles: agent in roles)]
    ddf = ddf.loc[df['bracket'] == bracket] 
    return ddf.to_json(orient='records')

def query_IGL(bracket, region="all", agent="all"):
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()
    if bracket not in ["vct-challengers", "vct-international", "game-changers"]:
        raise ValueError(f"Please select a valid bracket from vct-challengers, vct-international, game-changers")
    ddf = ddf[ddf['IGL']]
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if agent != 'all':
        ddf = ddf[ddf['top_3_agents'].apply(lambda roles: agent in roles)]
    ddf = ddf.loc[df['bracket'] == bracket] 
    return ddf.to_json(orient='records')

def query_OPer(bracket, region="all", agent="all"):
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()
    if bracket not in ["vct-challengers", "vct-international", "game-changers"]:
        raise ValueError(f"Please select a valid bracket from vct-challengers, vct-international, game-changers")
    
    ddf = ddf[ddf['OPer']]
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if agent != 'all':
        ddf = ddf[ddf['top_3_agents'].apply(lambda roles: agent in roles)]
    ddf = ddf.loc[df['bracket'] == bracket] 
    return ddf.to_json(orient='records')

def query_aggregated_data(player_name="all", bracket=["vct-challengers", "vct-international", "game-changers"], region="all"):
    # Argument assertions
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])

    ddf = df.copy()
    if bracket not in ["vct-challengers", "vct-international", "game-changers"]:
        raise ValueError(f"Please select a valid bracket from vct-challengers, vct-international, game-changers")
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if player_name != 'all':
        ddf = ddf.loc[ddf['player_name'].astype(str) == player_name]
    ddf = ddf.loc[df['bracket'].isin(bracket)] # does not respect index order which is why is last. everything else does.
    return ddf.to_json(orient='records')

def query_unaggregated_data(player_name="all", bracket=["vct-challengers", "vct-international", "game-changers"], region="all", past_games="all", agent="all"):
    # Argument assertions
    filePath = "unaggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])

    ddf = df.copy()

    if bracket not in ["vct-challengers", "vct-international", "game-changers"]:
        raise ValueError(f"Please select a valid bracket from vct-challengers, vct-international, game-changers")
    if region != 'all':
        ddf = ddf.loc[df['region'] == region]
    if player_name != 'all':
        ddf = ddf.loc[ddf['player_name'].astype(str) == player_name]
    if agent != 'all':
        ddf = ddf.loc[ddf['player_agent'] == agent]
    if past_games != 'all':
        ddf = ddf[-int(past_games):]
    ddf = ddf.loc[df['bracket'].isin(bracket)] # does not respect index order which is why is last. everything else does.
    return ddf.to_json(orient='records')
'''