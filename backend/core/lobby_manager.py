from fastapi import WebSocket

from backend.core.socket import sio
from .models.lobby import Lobby
from .utils import create_lobby_code
from backend.config import MAX_GAMES
from .exceptions import SessionsFullException, LobbyNotFoundException, LobbyPlayerExistsException, PlayerNotFoundException
import uuid
import threading
import time

class LobbyManager:
    __instance = None
    __lobbies = dict()
    __sids = dict() # sid -> lobby code


    @staticmethod
    def get_instance():
        if LobbyManager.__instance == None:
            LobbyManager()
        return LobbyManager.__instance
    

    # Should never call this constructor directly. Use get_instance
    def __init__(self):
        if LobbyManager.__instance != None:
            raise Exception("Trying to init a second game master")
        else:
            LobbyManager.__instance = self

        cleaner = threading.Thread(target=self.lobby_cleaner)
        cleaner.daemon = True
        cleaner.start()


    def create_lobby(self):
        if self.get_num_lobbies() >= MAX_GAMES:
            raise SessionsFullException # TODO Make this a custom class

        code = create_lobby_code()
        while code in self.__lobbies:
            code = create_lobby_code()

        # Create the session
        self.__lobbies[code] = Lobby(code)

        return code


    def remove_lobby(self, code):
        del self.__lobbies[code]


    def get_lobby(self, lobby_code):
        lobby = self.__lobbies.get(lobby_code)

        if not lobby:
            raise LobbyNotFoundException

        return lobby


    def get_num_lobbies(self):
        return len(self.__lobbies)


    def lobby_cleaner(self):
        while True:
            self.clean_up_lobbies()
            time.sleep(5)


    def clean_up_lobbies(self):
        to_delete = []
        for code in self.__lobbies:
            lobby = self.__lobbies[code]
            if lobby.cleanup:
                to_delete.append(code)

        for code in to_delete:
            print("Lobby", code, "marked for cleaning. Deleting...")
            self.remove_lobby(code)

    def add_sid(self, sid, code):
        self.__sids[sid] = code

    def get_sid_lobby(self, sid):
        return self.__sids.get(sid)


# Socket IO stuff
@sio.event
def disconnect(sid):
    lm = LobbyManager.get_instance()
    lobby = lm.get_lobby(lm.get_sid_lobby(sid))
    print('disconnect', sid)


@sio.on('join_lobby')
async def sio_join_lobby(sid, code, player_name):
    lm = LobbyManager.get_instance()

    lobby = None
    try:
        lobby = lm.get_lobby(code)
    except LobbyNotFoundException:
        await sio.emit('invalid_lobby', code, room=sid)
        return

    lm.add_sid(sid, code)
    await lobby.join_lobby(player_name, sid)
