from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schema import MessagesModel

from .consumers import Consumer
from .models import promt
from database import get_async_session


router = APIRouter(prefix="/chat", tags=["AIChat"])
manager = Consumer()


@router.get("/last_messages")
async def get_last_messages(
    session: AsyncSession = Depends(get_async_session),
) -> List[MessagesModel]:
    query = select(promt).order_by(promt.c.created_at)
    messages = await session.execute(query)
    print("HERE")
    return {"Hello": "Bro"}
    # return messages.scalars().all()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await manager.connect(websocket, session)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"promt #{client_id}: {data}", add_to_db=True)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)
