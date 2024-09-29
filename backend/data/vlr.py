import requests
import os
import json

def fetch_player_data():
    regions = ['na', 'eu', 'ap','sa', 'jp', 'oce', 'mn']
    for region in regions:
        print(f"Fetching player data for {region}")
        try:
            url = f"https://vlrggapi.vercel.app/stats?region={region}&timespan=all"
            response = requests.get(url)
            data = json.loads(response.content.decode('utf-8'))

            output_dir = os.path.join('vlr', 'players')
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, f"{region}.json")
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error fetching data for {region}: {e}")
            break

def fetch_match_data():
    print("Fetching match data")
    try:
        url = "https://vlrggapi.vercel.app/match?q=results"
        response = requests.get(url)
        data = json.loads(response.content.decode('utf-8'))

        output_dir = os.path.join('vlr', 'matches')
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, "matches.json")
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error fetching match data: {e}")

def fetch_rankings_data():
    regions = ['na', 'eu', 'ap', 'la', 'la-s', 'la-n', 'oce', 'kr', 'mn', 'gc', 'br', 'cn', 'jp', 'col']
    for region in regions:
        print(f"Fetching rankings data for {region}")
        try:
            url = f"https://vlrggapi.vercel.app/rankings?region={region}"
            response = requests.get(url)
            data = json.loads(response.content.decode('utf-8'))

            output_dir = os.path.join('vlr', 'rankings')
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, f"{region}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error fetching ranking data for region {region} : {e}")
            break
         
fetch_player_data()
fetch_match_data()
fetch_rankings_data()