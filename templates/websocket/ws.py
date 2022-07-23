from turtle import end_fill
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, websockets, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from requests import request
from core.db import engine, SessionLocal
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from datetime import datetime

templates = Jinja2Templates(directory="templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            print(connection)
            await connection.send_text(message)


manager = ConnectionManager()

wsRouter = APIRouter()

@wsRouter.get("/", response_class = HTMLResponse)
async def websocket_index(request: Request):
    return templates.TemplateResponse("websocket/websocket.html", context={'request': request})


@wsRouter.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # if data == 'create_post':
                # localsession = SessionLocal()
                # post = Post(title = 'new post', text = 'some text', date = datetime.now())
                # localsession.add(post)
                # localsession.commit()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")