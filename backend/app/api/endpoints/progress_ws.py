from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.ws_manager import ws_manager


router = APIRouter(prefix="/progress")

@router.websocket("/{sid}")
async def websocket_progress(websocket: WebSocket, sid: str):
    await ws_manager.connect(sid, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(sid)
