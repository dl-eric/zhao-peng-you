from fastapi import APIRouter, HTTPException, WebSocket

from backend.db.base import db
from backend.game import GameMaster
from backend.exceptions import SessionsFullException, LobbyNotFoundException

router = APIRouter()

@router.get('/count')
async def get_num_lobbies():
    gm = GameMaster.get_instance()
    return gm.get_num_lobbies()

@router.put('/create')
async def create_lobby():
    # Ask game if we can create a new lobby
    gm = GameMaster.get_instance()
    
    code = None

    try:
        code = gm.create_lobby()
    except SessionsFullException:
        raise HTTPException(status_code=400, detail="Can't create lobby")
    # Return lobby code
    return code

@router.post('/join')
async def join_lobby(lobby_code: str, player_name: str):
    gm = GameMaster.get_instance()

    new_player_id = None

    try:
        new_player_id = gm.join_lobby(lobby_code, player_name)
    except LobbyNotFoundException:
        raise HTTPException(status_code=404, detail="Lobby not found")
    except LobbyPlayerExistsException:
        raise HTTPException(status_code=400, detail="Player with that name already exists in the lobby.")

    # Return player id
    return 'hi'

@router.get('/{lobby_code}/players')
async def get_players(lobby_code: str):
    gm = GameMaster.get_instance()
    return gm.get_players(lobby_code)

@router.websocket('/{lobby_code}')
async def lobby_websocket(websocket: WebSocket, lobby_code: str, player_id: str = None):
    if not player_id or not gm.in_lobby(lobby_code, player_id):
        await websocket.close()
        return

    await websocket.accept()

    websocket.send_text("hi!")

    await websocket.close()

    # Connect websocket