import boto3
import pandas as pd 
import re
import json

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

bucket_name = "vlr-data"
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket(bucket_name)

def compress_valorant_stats(df, which=0):
    """
    Compresses Valorant player statistics into a minimal string format.
    Format: SCHEMA#DATA where:
    - SCHEMA defines column types (n=number,s=string,b=boolean,l=list,p=percentage)
    - DATA contains rows with minimal separators
    """
    df = df.copy()    
    query_team_schema = {
        'player_name': 's',
        'team_name': 's',
        'player_kda': 'n',
        'player_combat_score': 'n',
        'top_3_agents': 'l',
        'region': 's',
        'games_played': 'n',
        'rank': 'n',
        'win_rate': 'p',
        'fb-fd ratio': 'n',
        'clutches_per_game': 'n',
        'KPR': 'n',
        'KPR_Variance': 'n',
        'kill_assists_survived_traded': 'p',
        'IGL': 'b',
        'OPer': 'b',
    }

    query_past_games_schema = {
        'player_name': 's',
        'wins': 'n',
        'loss': 'n',
        'player_agent': 's',
        'player_kills':'n',
        'player_deaths':'n',
        'player_assists':'n',
        'player_first_bloods':'n',
        'player_first_deaths':'n',
        'player_clutches':'n',
        'player_combat_score': 'n',
        'bracket': 's',
        'region': 's',
        'KPR': 'n',
        'KPR_Variance': 'n',
    }
    
    query_player_schema = {
        'player_name': 's',
        'team_name': 's',
        'player_kda': 'n',
        'player_combat_score': 'n',
        'top_3_agents': 'l',
        'top_roles':'l',
        'region': 's',
        'bracket': 's',
        'games_played': 'n',
        'rank': 'n',
        'earnings': 'n',
        'win_rate': 'p',
        'fb-fd ratio': 'n',
        'clutches_per_game': 'n',
        'KPR': 'n',
        'KPR_Variance': 'n',
        'kill_assists_survived_traded': 'p',
        'IGL': 'b',
        'OPer': 'b',
    }
    schemas = [query_team_schema, query_past_games_schema, query_player_schema]
    schema = schemas[which]
    
    def format_number(n):
        """Format number removing trailing zeros and leading zeros in decimals"""
        if pd.isna(n):
            return ''
        s = f"{float(n):.2f}".rstrip('0').rstrip('.')
        # Replace leading "0." with "."
        if s.startswith('0.'):
            s = s[1:]
        return s
    
    def parse_agents(agent_str):
        """Parse the agents string into a list of agent names"""
        # Extract names using regex
        agents = re.findall(r"'([^']*)'", agent_str)
        return agents
    def parse_roles(agent_str):
        """Parse the agents string into a list of agent names"""
        # Extract names using regex
        agents = re.findall(r"'([^']*)'", agent_str)
        return agents
            
    schema_str = ','.join(f"{k}:{v}" for k, v in schema.items())
    rows = []
    for _, row in df.iterrows():
        row_data = []
        for col in df.columns:
            val = row[col]
            if col == 'top_3_agents':
                # Parse the agents string and join with +
                agents = parse_agents(str(val))
                val = '+'.join(agents)
            elif col == 'top_roles':
                roles = parse_roles(str(val))
                val = '+'.join(roles)
            elif isinstance(val, bool):
                val = '1' if val else '0'
            elif isinstance(val, (float, int)):
                # Format numbers efficiently
                val = format_number(val)
            elif pd.isna(val):
                val = ''
            row_data.append(str(val))
        rows.append('|'.join(row_data))
    
    return f"{schema_str}#{';'.join(rows)}"

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
    data = {
        f"query_past_games_{player_name}_{past_games}_{agent}": compress_valorant_stats(ddf, 1)
    }
    return json.dumps(data)
# [initiator, duelist, initor, dulesit, sentile], ['vct-internaotinl, gamehcanger,s chaegamdf], []

def get_players_from_specifiers(role: list, bracket: list, igl: list, region=["all","all","all","all","all"], agent=["all","all","all","all","all"]):
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()
    agents = [
    'Brimstone', 'Viper', 'Omen', 'Killjoy', 'Cypher', 'Sova', 'Sage', 'Phoenix', 'Jett', 'Reyna', 'Raze', 
    'Breach', 'Skye', 'Yoru', 'Astra', 'KAY/O', 'Chamber', 'Neon', 'Fade', 'Harbor', 'Gekko', 'Deadlock', 
    'Iso', 'Clove', 'Vyse'
    ]

    data = {}
    for i in range(5):

        curr = ddf.copy()
        if bracket[i] not in ["vct-challengers", "vct-international", "game-changers"]:
            raise ValueError(f"Please select a valid bracket from vct-challengers, vct-international, game-changers")
        if role[i] not in ['Duelist', 'Initiator', 'Controller', 'Sentinel']:
            raise ValueError(f"Please select a valid role from Duelist, Initiator, Controller, Sentinel")
        if region[i] != 'all' and region[i] not in ['NA', 'INTL', 'BR', 'LATAM', 'SEA', 'LAS', 'KR', 'JP', 'EMEA', 'VN', 'CN']:
            raise ValueError(f"Please select a valid role from NA, INTL, BR, LATAM, SEA, LAS, KR, JP, EMEA, VN, CN")
        if agent[i] != 'all' and agent[i] not in agents:
            raise ValueError(f"Please select a valid agent from Brimstone, Viper, Omen, Killjoy, Cypher, Sova, Sage, Phoenix, Jett, Reyna, Raze, Breach, Skye, Yoru, Astra, KAY/O, Chamber, Neon, Fade, Harbor, Gekko, Deadlock, Iso, Clove, Vyse")
        curr = curr[curr['top_roles'].apply(lambda roles: role[i] in roles)]
        curr = curr.loc[curr['bracket'] == bracket[i]]
        if igl[i]:
            curr = curr[curr['IGL']]    
        if region[i] != 'all':
            curr = curr.loc[curr['region'] == region[i]]
        if agent[i] != 'all':
            curr = curr[curr['top_3_agents'].apply(lambda roles: agent[i] in roles)]
        
        curr = curr.drop(columns=['earnings', 'bracket', 'top_roles', ])
        curr['player_combat_score'] = curr['player_combat_score'].astype(int)
        curr['win_rate'] = curr['win_rate'].str.rstrip('%').astype(float) / 100
        curr['win_rate'] = curr['win_rate'].round(2)
        curr['kill_assists_survived_traded'] = curr['kill_assists_survived_traded'].fillna('').astype(str)
        data[f"get_players_{i}_{role[i]}_{bracket[i]}_{region[i]}_{agent[i]}_{igl[i]}"] = compress_valorant_stats(curr, 0)
    return json.dumps(data)

def query_player(player_name):
    filePath = "aggregated_data.csv"
    g = bucket.Object(filePath)
    df = pd.read_csv(g.get()['Body'])
    ddf = df.copy()
    ddf = ddf.loc[ddf['player_name'].astype(str) == player_name]
    data = {
        f'query_player_{player_name}' : compress_valorant_stats(ddf, 2)
    }
    return json.dumps(data)
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