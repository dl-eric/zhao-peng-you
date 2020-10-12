import socketio


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[])
socket_app = socketio.ASGIApp(sio)

@sio.event
def connect(sid, env):
    print('connect', sid)


@sio.event
def disconnect(sid):
    print('disconnect', sid)