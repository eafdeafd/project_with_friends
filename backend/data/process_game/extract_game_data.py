from enum import StrEnum
import orjson as json
from typing import Dict
from game_data_schema import *
import os
import glob

class GamePhase(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    GAME_STARTED = "GAME_STARTED"
    BETWEEN_ROUNDS = "BETWEEN_ROUNDS"
    ROUND_STARTING = "ROUND_STARTING"
    IN_ROUND = "IN_ROUND"
    ROUND_ENDING = "ROUND_ENDING"
    SWITCHING_TEAMS = "SWITCHING_TEAMS"
    GAME_ENDED = "GAME_ENDED"

class GameParser:
    def __init__(self):
        self.game = Game()
        self.current_round = 0
        self.processed_start_round = False
        self.processed_end_round = False
        self.first_blood = True
        self.phase: GamePhase = GamePhase.NOT_STARTED
        # Maps of player and team id to objects
        self.players: Dict[int, Player] = {}
        self.teams: Dict[int, Team] = {}

    def add_team(self, team_json):
        team = Team()
        team.id = team_json["teamId"]["value"]
        team.side = Side(team_json["name"])
        for player in team_json["playersInTeam"]:
            player_id = player["value"]
            if player_id not in self.players:
                self.players[player_id] = Player(id=player_id)
            team.players.append(self.players[player_id])

        self.game.teams.append(team)
        self.teams[team.id] = team

    def extract_game(self, data: dict):
        self.game.id = data[0]["metadata"]["gameId"]["value"]
        for segment in data:
            if "currentGamePhase" in segment["metadata"]:
                self.phase = GamePhase(segment["metadata"]["currentGamePhase"]["phase"])
            else:
                if "gamePhase" in segment:
                    self.phase = GamePhase(segment["gamePhase"]["phase"])

            if self.phase == GamePhase.NOT_STARTED:
                if "snapshot" in segment:
                    continue

                if "configuration" in segment:
                    if self.game.map != Map.UNKNOWN:
                        continue
                    self.game.map = Map.from_code_name(segment["configuration"]["selectedMap"]["fallback"]["displayName"])
                    teams_json = segment["configuration"]["teams"]
                    for team_json in teams_json:
                        self.add_team(team_json)
                    
                    players_json = segment["configuration"]["players"]
                    for player_json in players_json:
                        player_id = player_json["playerId"]["value"]
                        self.players[player_id].name = player_json["displayName"]
                        self.players[player_id].agent = Agent.from_guid(player_json["selectedAgent"]["fallback"]["guid"])

                continue
            
            if self.phase == GamePhase.GAME_STARTED:
                continue

            if self.phase == GamePhase.BETWEEN_ROUNDS:
                if "roundStarted" in segment:
                    round_info = segment["roundStarted"]
                    self.current_round = round_info["roundNumber"]
                    self.processed_start_round = False
                    self.processed_end_round = False
                    self.first_blood = True
                    self.game.rounds.append(Round(number=self.current_round))
                    self.game.rounds[-1].attacker = Side(self.teams[round_info["spikeMode"]["attackingTeam"]["value"]].side)
                
                continue

            if self.phase == GamePhase.ROUND_STARTING:
                continue
            
            if self.phase == GamePhase.IN_ROUND:
                if "snapshot" in segment and "players" in segment["snapshot"]:
                    if self.processed_start_round:
                        continue
                    for player_json in segment["snapshot"]["players"]:
                        player_id = player_json["playerId"]["value"]

                        player = self.players[player_id]
                        player_round = PlayerRound(number=self.current_round)
                        player_round.armor = player_json["aliveState"]["armor"]
                        for item in player_json["inventory"]:
                            if item["slot"]["slot"] == "PRIMARY":
                                player_round.primary = Weapon(item["displayName"])
                            elif item["slot"]["slot"] == "SECONDARY":
                                player_round.secondary = Weapon(item["displayName"])
                        
                        player.rounds.append(player_round)

                    self.processed_start_round = True
                
                if "damageEvent" in segment:
                    attacker = self.players[segment["damageEvent"]["causerId"]["value"]]
                    attacker.rounds[-1].damage += segment["damageEvent"]["damageDealt"]

                if "playerDied" in segment:
                    if not self.first_blood:
                        continue
                    killer = segment["playerDied"]["killerId"]["value"]
                    victim = segment["playerDied"]["deceasedId"]["value"]
                    self.players[killer].first_bloods += 1
                    self.players[victim].first_deaths += 1
                    self.first_blood = False

                continue


            if self.phase == GamePhase.ROUND_ENDING or self.phase == GamePhase.GAME_ENDED:
                if "snapshot" in segment and "players" in segment["snapshot"]:
                    if self.processed_end_round:
                        continue
                    for player_json in segment["snapshot"]["players"]:
                        player = self.players[player_json["playerId"]["value"]]
                        player.rounds[-1].alive = "aliveState" in player_json
                        player.rounds[-1].kills = player_json["kills"] - player.kills
                        player.rounds[-1].deaths = player_json["deaths"] - player.deaths
                        player.rounds[-1].assists = player_json["assists"] - player.assists
                        player.rounds[-1].combat_score = player_json["scores"]["combatScore"]["roundScore"]
                        player.kills = player_json["kills"]
                        player.deaths = player_json["deaths"] 
                        player.assists = player_json["assists"]
                        player.combat_score = player_json["scores"]["combatScore"]["totalScore"] / len(self.game.rounds)
                    
                    self.processed_end_round = True
                
                # overall game over
                if "gameDecided" in segment:
                    gameDecidedSegment = segment["gameDecided"]
                                
                continue
        

        self.game.winner = Side(self.teams[gameDecidedSegment["winningTeam"]["value"]].side)
        for round_data in gameDecidedSegment["spikeMode"]["completedRounds"]:
            current_round: Round = self.game.rounds[round_data["roundNumber"] - 1]
            current_round.winner = Side(self.teams[round_data["winningTeam"]["value"]].side)
            current_round.win_method = WinMethod(round_data["spikeModeResult"]["cause"])
            
            winning_team = self.teams[round_data["winningTeam"]["value"]]
            living_winners = [player.rounds[current_round.number - 1].alive for player in winning_team.players]
            if sum(living_winners) == 1:
                winning_team.players[living_winners.index(True)].clutches += 1



def process_file(file_path, league):
    with open(file_path, 'r') as f:
        data = json.loads(f.read())
    
    game_data = GameParser()
    game_data.extract_game(data)
    
    year = file_path.split('/')[-3]  
    output_dir = os.path.join('extracted_games', league, year)
    os.makedirs(output_dir, exist_ok=True)
    
    original_filename = os.path.basename(file_path)
    output_filename = f"{os.path.splitext(original_filename)[0]}_extract.json"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, 'w') as f:
        f.write(game_data.game.model_dump_json(indent=2))
    
    print(f"Processed game to {output_path}")

if __name__ == "__main__":
    leagues = ['vct-international', 'game-changers', 'vct-challengers']
    years = ['2022', '2024', '2023']
    
    for league in leagues:
        for year in years:
            base_path = f'{league}/games/{year}'
            if os.path.exists(base_path):
                names = glob.glob(base_path + '/*.json')
                percentage_failed = 0
                for name in names:
                    try:
                        process_file(name, league)
                    except KeyError or IndexError as e:
                        print(e)
                        percentage_failed += 1
                print((percentage_failed/len(names)))
                exit()
            else:
                print(f"Path does not exist: {base_path}")