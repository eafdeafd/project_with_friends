from typing import List
from enum import StrEnum

from pydantic import BaseModel, Field
import orjson as json
from pathlib import Path

agent_guids = {}
with open(Path(__file__).parent / "agent_guids.json", "r") as f:
    agent_guids = json.loads(f.read())

map_codes = {}
with open(Path(__file__).parent / "map_codes.json", "r") as f:
    map_codes = json.loads(f.read())

class Weapon(StrEnum):
    CLASSIC = "Classic"
    SHORTY = "Shorty"
    FRENZY = "Frenzy"
    GHOST = "Ghost"
    SHERIFF = "Sheriff"
    STINGER = "Stinger"
    SPECTRE = "Spectre"
    BUCKY = "Bucky"
    JUDGE = "Judge"
    BULLDOG = "Bulldog"
    GUARDIAN = "Guardian"
    PHANTOM = "Phantom"
    VANDAL = "Vandal"
    MARSHAL = "Marshal"
    OUTLAW = "Outlaw"
    OPERATOR = "Operator"
    ARES = "Ares"
    ODIN = "Odin"
    MELEE = "Melee"
    UNKNOWN = "Unknown"

class Map(StrEnum):
    BIND = "Bind"
    HAVEN = "Haven"
    SPLIT = "Split"
    ASCENT = "Ascent"
    ICEBOX = "Icebox"
    BREEZE = "Breeze"
    FRACTURE = "Fracture"
    PEARL = "Pearl"
    LOTUS = "Lotus"
    SUNSET = "Sunset"
    ABYSS = "Abyss"
    UNKNOWN = "Unknown"

    def from_code_name(code_name: str):
        return Map(map_codes[code_name])

class Agent(StrEnum):
    BRIMSTONE = "Brimstone"
    PHOENIX = "Phoenix"
    SAGE = "Sage"
    SOVA = "Sova"
    VIPER = "Viper"
    CYPHER = "Cypher"
    REYNA = "Reyna"
    KILLJOY = "Killjoy"
    BREACH = "Breach"
    OMEN = "Omen"
    JETT = "Jett"
    RAZE = "Raze"
    SKYE = "Skye"
    YORU = "Yoru"
    ASTRA = "Astra"
    KAYO = "KAY/O"
    CHAMBER = "Chamber"
    NEON = "Neon"
    FADE = "Fade"
    HARBOR = "Harbor"
    GEKKO = "Gekko"
    DEADLOCK = "Deadlock"
    ISO = "Iso"
    CLOVE = "Clove"
    VYSE = "Vyse"
    UNKNOWN = "Unknown"
        
    def from_guid(guid: str):
        return Agent(agent_guids[guid])

class WinMethod(StrEnum):
    ELIMINATION = "ELIMINATION"
    SPIKE_DEFUSE = "SPIKE_DEFUSE"
    DETONATE = "DETONATE"
    TIME_EXPIRED = "TIME_EXPIRED"
    UNKNOWN = "Unknown"

class Side(StrEnum):
    RED = "Red"
    BLUE = "Blue"
    UNKNOWN = "Unknown"

class Round(BaseModel):
    number: int = -1
    winner: Side = Side.UNKNOWN
    attacker: Side = Side.UNKNOWN
    win_method: WinMethod = WinMethod.UNKNOWN

class PlayerRound(BaseModel):
    number: int = -1
    alive: bool = False
    primary: Weapon = Weapon.UNKNOWN
    secondary: Weapon = Weapon.UNKNOWN
    armor: int = -1
    damage: float = 0.
    kills: int = -1
    deaths: int = -1
    assists: int = -1
    combat_score: int = -1

class Player(BaseModel):
    id: int = -1
    name: str = ""
    agent: Agent = Agent.UNKNOWN
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    first_bloods: int = 0
    first_deaths: int = 0
    clutches: int = 0
    combat_score: float = -1
    rounds: List[PlayerRound] = Field(default_factory=list)

class Team(BaseModel):
    id: int = -1
    name: str = ""
    side: Side = Side.UNKNOWN
    players: List[Player] = Field(default_factory=list)

class Game(BaseModel):
    id: str = ""
    map: Map = Map.UNKNOWN
    winner: Side = Side.UNKNOWN
    rounds: List[Round] = Field(default_factory=list)
    teams: List[Team] = Field(default_factory=list)