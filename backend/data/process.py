import os
import json
from dataclasses import dataclass
from typing import Type, Dict, List

BRACKET_GAME_CHANGERS = 'game-changers'
BRACKET_CHALLENGERS = 'vct-challengers'
BRACKET_INTERNATIONAL = 'vct-international'
ESPORTS_DIR = 'esports-data'
GAMES_DIR = 'games'
LEAGUE_FILEPATH = 'leagues.json'
MAPPING_FILEPATH = 'mapping_data.json'
PLAYERS_FILEPATH = 'players.json'
TEAMS_FILEPATH = 'teams.json'
TOURNAMENTS_FILEPATH = 'tournaments.json'

@dataclass
class Team:
    tid: int
    league_id: int
    name: str

@dataclass
class Tournament:
    tid: int
    league_id: int
    name: str

@dataclass
class League:
    tid: int
    region: str
    name: str

def build_file_path(*segments):
    """
    Builds a file path by joining multiple path segments together.
    """
    return os.path.join(*segments)

def load_data(bracket: str, file_path: str, cls: Type, mapping: Dict[str, str], id_key: str = 'id') -> Dict[int, object]:
    """
    Generalized function to load JSON data, create class instances, and map them by the specified id field.
    
    Parameters:
    - bracket (str): The bracket to fetch the data from (e.g., 'game-changers').
    - file_path (str): The specific file path to load (e.g., 'teams.json').
    - cls (Type): The data class type (e.g., Team, Tournament, League).
    - mapping (Dict[str, str]): A mapping from the JSON keys to the data class attributes.
    - id_key (str): The key in the JSON data to use as the id (e.g., 'id', 'league_id').
    
    Returns:
    - Dict[int, object]: A dictionary mapping the id to the data class instance.
    """
    result = {}

    with open(build_file_path(bracket, ESPORTS_DIR, file_path), 'r') as file:
        data = json.load(file)

    for item in data:
        instance = cls(**{attr: item[key] for key, attr in mapping.items()})
        result[item[id_key]] = instance

    return result

def get_all_teams(bracket=BRACKET_INTERNATIONAL):
    return load_data(
        bracket=bracket,
        file_path=TEAMS_FILEPATH,
        cls=Team,
        mapping={'id': 'tid', 'home_league_id': 'league_id', 'name': 'name'},
        id_key='id'
    )

def get_all_tournaments(bracket=BRACKET_INTERNATIONAL):
    return load_data(
        bracket=bracket,
        file_path=TOURNAMENTS_FILEPATH,
        cls=Tournament,
        mapping={'id': 'tid', 'league_id': 'league_id', 'name': 'name'},
        id_key='id'
    )

def get_all_leagues(bracket=BRACKET_INTERNATIONAL):
    return load_data(
        bracket=bracket,
        file_path=LEAGUE_FILEPATH,
        cls=League,
        mapping={'league_id': 'tid', 'region': 'region', 'name': 'name'},
        id_key='league_id'
    )



if __name__ == "__main__":
    print(get_all_teams())
    print(get_all_tournaments())
    print(get_all_leagues())