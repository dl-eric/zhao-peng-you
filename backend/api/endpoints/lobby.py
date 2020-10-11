from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from backend.db.base import db
from backend.lobby_manager import LobbyManager
from backend.exceptions import SessionsFullException, LobbyNotFoundException, LobbyPlayerExistsException


router = APIRouter()

@router.get('/count')
async def get_num_lobbies():
    lm = LobbyManager.get_instance()
    return lm.get_num_lobbies()


@router.put('/create')
async def create_lobby():
    # Ask game if we can create a new lobby
    lm = LobbyManager.get_instance()
    
    code = None

    try:
        code = lm.create_lobby()
    except SessionsFullException:
        raise HTTPException(status_code=400, detail="Can't create lobby")
    # Return lobby code
    return code


@router.post('/join/{lobby_code}')
async def join_lobby(lobby_code: str, player_name: str):
    lm = LobbyManager.get_instance()
    lobby = None
    new_player_id = None

    try:
        lobby = lm.get_lobby(lobby_code)
    except LobbyNotFoundException:
        raise HTTPException(status_code=404, detail="Lobby not found")

    try:
        new_player_id = lobby.join_lobby(player_name)
    except LobbyPlayerExistsException:
        raise HTTPException(status_code=400, detail="Player with that name already exists in the lobby.")

    return new_player_id


@router.websocket('/{lobby_code}')
async def lobby_websocket(websocket: WebSocket, lobby_code: str):
    lm = LobbyManager.get_instance()
    lobby = None

    try:
        lobby = lm.get_lobby(lobby_code)
    except LobbyNotFoundException:
        # Websocket close logic
        await websocket.close()
        return
    
    await lobby.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        lobby.disconnect(websocket)
        print("WS Disconnected")