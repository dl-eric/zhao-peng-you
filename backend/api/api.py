from fastapi import APIRouter

from .endpoints import lobby, player

api_router = APIRouter()
api_router.include_router(lobby.router, prefix="/lobby", tags=['Lobby'])
api_router.include_router(player.router, prefix="/player", tags=['Player'])
#api_router.include_router(note.router, prefix="/note", tags=['Note'])
#api_router.include_router(utils.router, prefix="/utils", tags=['Utils'])
