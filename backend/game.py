from .utils import create_lobby_code
from .config import MAX_GAMES
from .models import Lobby
from .exceptions import SessionsFullException, LobbyNotFoundException, LobbyPlayerExistsException
import uuid

class GameMaster:
    __instance = None
    __lobbies = dict()

    @staticmethod
    def get_instance():
        if GameMaster.__instance == None:
            GameMaster()
        return GameMaster.__instance
    
    # Should never call this constructor directly. Use get_instance
    def __init__(self):
        if GameMaster.__instance != None:
            raise Exception("Trying to init a second game master")
        else:
            GameMaster.__instance = self

    def create_lobby(self):
        if self.get_num_lobbies() >= MAX_GAMES:
            raise SessionsFullException # TODO Make this a custom class

        code = create_lobby_code()
        while code in self.__lobbies:
            code = create_lobby_code()

        # Create the session
        self.__lobbies[code] = Lobby(join_code=code)

        return code

    def get_num_lobbies(self):
        return len(self.__lobbies)

    def join_lobby(self, lobby_code, player_name):
        lobby = self.__lobbies.get(lobby_code)
        
        if not lobby:
            raise LobbyNotFoundException
        
        player_hash = hash(player_name)

        if player_hash in lobby.players:
            raise LobbyPlayerExistsException

        lobby.players.add(player_hash)

    def in_lobby(self, lobby_code, player_id):
        return player_id in self.__lobbies.get(lobby_code).players

    def get_players(self, lobby_code):
        return list(self.__lobbies.get(lobby_code).players)