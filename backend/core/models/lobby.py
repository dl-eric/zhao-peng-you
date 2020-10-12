from fastapi import WebSocket

from backend.core.socket import sio
from backend.config import MAX_NAME_LENGTH
from backend.core.exceptions import LobbyPlayerExistsException
import json
import uuid

class LobbyPlayer:
    def __init__(self, sid, uuid):
        self.sid = sid
        self.uuid = uuid
        self.name = ""
        self.leader = False


class Lobby:
    def __init__(self, join_code):
        self.join_code = join_code
        self.players = dict() # names -> uuids
        self.connections = dict() # uuids -> socket io id
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
        await sio.emit("players", json.dumps(player_names), room=self.join_code)
        await sio.emit("leader", self.leader, room=self.join_code)


    # Returns (uuid4, player_name)
    async def join_lobby(self, player_name: str, sid):
        # Truncate name
        player_name = player_name[:MAX_NAME_LENGTH]

        uniquifier = 1
        while player_name in self.players:
            player_name += str(uniquifier)
            uniquifier += 1

        # Give player back their sanitized name
        await sio.emit('name', player_name, room=sid)

        player_id = uuid.uuid4()
        self.players[player_name] = player_id

        # Give player their id
        await sio.emit('id', str(player_id), room=sid)

        if not self.leader:
            self.leader = player_name

        sio.enter_room(sid, self.join_code)
        
        await self.send_player_update()


    async def leave_lobby(self, player_name, player_id, sid):
        if player_name in self.players and self.players[player_name] == player_id:
            del self.players[player_name]
            del self.connections[player_id]
            sio.disconnect(sio)

            # TODO:If we were the last player in the lobby, clean up this lobby object.
            if len(self.players) <= 0:
                self.leader = None
                self.cleanup = True
            else:
                await self.send_player_update()