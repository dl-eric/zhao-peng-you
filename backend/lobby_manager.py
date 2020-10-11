from fastapi import WebSocket

from .models.lobby import Lobby
from .utils import create_lobby_code
from .config import MAX_GAMES
from .exceptions import SessionsFullException, LobbyNotFoundException, LobbyPlayerExistsException, PlayerNotFoundException
import uuid
import threading
import time

class LobbyManager:
    __instance = None
    __lobbies = dict()


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