from pydantic import BaseModel
from enum import IntEnum

class StateEnum(IntEnum):
    NULL    = 0
    LOBBY   = 1
    PLAYING = 2

class Lobby(BaseModel):
    join_code: str
    state: StateEnum = StateEnum.NULL
    players: set = set()

class Card(BaseModel):
    number: int
    suite: int
