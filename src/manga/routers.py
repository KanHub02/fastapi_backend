from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Page

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from scripts.parser import Parser

from manga.models import manga
from manga.schema import MangaListSchema

from pprint import pprint


router = APIRouter(prefix="/api/v1", tags=["Manga"])


@router.get("/generate-manga/")
async def scrapy(session: AsyncSession = Depends(get_async_session)):
    await Parser.create_data(session=session)
    return {"status": 200}


@router.get("/manga/", response_model=Page[MangaListSchema])
async def get_manga_list(session: AsyncSession = Depends(get_async_session)):
    query = manga.select().order_by(manga.c.likes)
    result = await session.execute(query)
    data = {}
    for i in result.all():
        data.update({"content": i})
    return {"status": 200, "data": data}
