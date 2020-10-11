from pydantic import BaseModel
from fastapi import WebSocket
from typing import List
    

class Player(BaseModel):
    player_id: str


class LobbyPlayer(Player):
    connection: WebSocket

    class Config:
        arbitrary_types_allowed = True


class Card(BaseModel):
    number: int
    suite: int
