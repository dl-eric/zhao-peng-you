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


# Message Protocol:
# First message client sends should be the player name they want
# First message client receives should be the player name they're assigned (server sanitized)
#       Name message format: 
#           name:<name here>:<uuid>
#
#       Chat message format:
#           send_chat:<message>
#
#       Disconnect msg format:
#           disconnect:<player_name>:<player_id>
#
#       New player msg format:
#           new:<new player's name>
#
#       Kick player msg format:
#           kick:<player being kicked name>:<player id>
#
@router.websocket('/{lobby_code}')
async def lobby_websocket(websocket: WebSocket, lobby_code: str, player_name: str = None):
    lm = LobbyManager.get_instance()
    lobby = None

    try:
        lobby = lm.get_lobby(lobby_code)
    except LobbyNotFoundException:
        # Websocket close logic
        await websocket.close()
        return

    if not player_name or len(player_name) < 2:
        await websocket.close()
        return

    (new_player_id, new_player_name) = await lobby.join_lobby(player_name)
    await lobby.connect(websocket, new_player_id)

    print(new_player_name, "joined lobby", lobby_code, "with id", new_player_id)
    await websocket.send_text("name:" + new_player_name + ":" + str(new_player_id))

    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {message}")

            values = message.split(':')

            if values[0] == "disconnect":
                try:
                    await lobby.disconnect(websocket, values[1], values[2])
                except:
                    pass
            elif values[0] == "send_chat":
                await lobby.broadcast(new_player_name + ": " + values[1])
            elif values[0] == "kick":
                await lobby.kick(values[1], values[2])

    except WebSocketDisconnect:
        await lobby.disconnect(websocket, new_player_name, new_player_id)
        print(new_player_name, "WS Disconnected from", lobby_code)