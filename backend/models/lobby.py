from fastapi import WebSocket

from backend.config import MAX_NAME_LENGTH
from backend.exceptions import LobbyPlayerExistsException
from backend.pyd_models import Player
import json


class Lobby:
    def __init__(self, join_code):
        self.join_code = join_code
        self.players = dict()
        self.connections = []


    def __getitem__(self, item):
        return self.players[item]


    async def join_lobby(self, player_name: str):
        # Truncate name
        player_name = player_name[:MAX_NAME_LENGTH]

        player_hash = hash(player_name)
        uniquifier = 1
        while player_name in self.players:
            player_name += str(uniquifier)
            player_hash = hash(player_name)
            uniquifier += 1

        self.players[player_name] = Player(player_id=player_hash)

        await self.broadcast("players:" + json.dumps(list(self.players.keys())))

        return (player_hash, player_name)


    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)


    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)