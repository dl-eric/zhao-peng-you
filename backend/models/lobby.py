from fastapi import WebSocket

from backend.config import MAX_NAME_LENGTH
from backend.exceptions import LobbyPlayerExistsException
import json
import uuid


class Lobby:
    def __init__(self, join_code):
        self.join_code = join_code
        self.players = dict() # names -> uuids
        self.connections = dict() # uuids -> WebSocket
        self.leader = None
        self.cleanup = False


    def __getitem__(self, item):
        return self.players[item]


    def set_leader(self, player_name: str):
        if player_name not in self.players:
            raise PlayerNotFoundException
        
        self.leader = player_name
        return "success"


    # player_id is the id of the person initiating the kick. This person should be the leader
    async def kick(self, player_to_kick, player_id):
        # Only the leader can kick
        if self.players[self.leader] != player_id:
            return

        await self.leave_lobby(player_to_kick)


    async def send_player_update(self):
        print(json.dumps(list(self.players.keys())))
        await self.broadcast("players:" + json.dumps(list(self.players.keys())))
        await self.broadcast("leader:" + self.leader)


    # Returns (uuid4, player_name)
    async def join_lobby(self, player_name: str):
        # Truncate name
        player_name = player_name[:MAX_NAME_LENGTH]

        uniquifier = 1
        while player_name in self.players:
            player_name += str(uniquifier)
            uniquifier += 1

        player_id = uuid.uuid4()
        self.players[player_name] = player_id

        if not self.leader:
            self.leader = player_name

        return (player_id, player_name)


    async def broadcast(self, message: str):
        for player_id in self.connections:
            await self.connections[player_id].send_text(message)


    async def connect(self, websocket: WebSocket, player_id):
        if player_id in self.connections:
            return

        await websocket.accept()
        self.connections[player_id] = websocket

        await self.send_player_update()


    async def disconnect(self, websocket: WebSocket, player_name: str, player_id):
        if player_name in self.players and self.players[player_name] == player_id:
            del self.players[player_name]
            del self.connections[player_id]
            await websocket.close()

            # TODO:If we were the last player in the lobby, clean up this lobby object.
            if len(self.players) <= 0:
                self.leader = None
                self.cleanup = True
            else:
                await self.send_player_update()