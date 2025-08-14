from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket) -> None:
        conns = self.active_connections.get(user_id, [])
        if websocket in conns:
            conns.remove(websocket)
        if not conns and user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, user_id: int, message: dict) -> None:
        for connection in self.active_connections.get(user_id, []):
            await connection.send_json(message)


manager = ConnectionManager()
