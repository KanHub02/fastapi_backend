from fastapi import WebSocket, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_maker, get_async_session
from .models import promt, connection, answer

from sqlalchemy import insert, select, delete
from scripts.openai_service import RequestService


class Consumer:
    def __init__(self) -> None:
        self.connection: List[WebSocket] = []

    async def connect(
        self, websocket: WebSocket, session: AsyncSession = Depends(get_async_session)
    ):
        await websocket.accept()
        self.connection.append(websocket)
        stmt = insert(connection).values(ws_code=str(websocket))
        await session.execute(stmt)
        await session.commit()

    def disconnect(
        self, websocket: WebSocket, session: AsyncSession = Depends(get_async_session)
    ):
        self.connection.remove(websocket)
        stmt = delete(connection).where(ws_code=str(websocket))
        session.execute(stmt)
        session.commit()
        return

    async def send_personal_message(self, message: str, websocket: WebSocket, session: AsyncSession = Depends(get_async_session)):
        data = RequestService.send_request(message)
        print(message)
        answer_stmt = insert(answer).values(text=str(data))
        promt_stmt = insert(promt).values(text=str(data))
        await session.execute(answer_stmt)
        await session.execute(promt_stmt)
        await session.commit()
        await websocket.send_text(message)
        await websocket.send_text(data)

    async def chatgpt_response(self, message: str):
        data = RequestService.send_request(message)
        await data
        async with async_session_maker() as session:
            stmt = insert(answer).values(text=data)
            await session.execute(stmt)
            await session.commit()

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_database(message)
        for connection in self.connection:
            await connection.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str):
        async with async_session_maker() as session:
            stmt = insert(promt).values(text=message)
            await session.execute(stmt)
            await session.commit()
