class WebSocketManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, sid, websocket):
        await websocket.accept()
        self.connections[sid] = websocket

    async def send(self, sid, message):
        if sid in self.connections:
            await self.connections[sid].send_json(message)

    def disconnect(self, sid):
        self.connections.pop(sid, None)


# global singleton
ws_manager = WebSocketManager()