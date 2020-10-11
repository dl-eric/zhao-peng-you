from fastapi import WebSocket

from backend.exceptions import LobbyPlayerExistsException
from backend.pyd_models import Player

class Lobby:
    def __init__(self, join_code):
        self.join_code = join_code
        self.players = dict()
        self.connections = []


    def __getitem__(self, item):
        return self.players[item]


    def join_lobby(self, player_name):
        player_hash = hash(player_name)

        if player_hash in self.players:
            raise LobbyPlayerExistsException
        
        self.players[player_hash] = Player(player_id=player_hash)

        return player_hash


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)


    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)