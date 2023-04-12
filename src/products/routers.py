from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from scripts.parser import Parser
from .models import product, category
from .schemas import ProductCreateSchema


router = APIRouter(prefix="/api/v1", tags=["Products"])


@router.get("/products/")
async def get_products(session: AsyncSession = Depends(get_async_session)):
    query = product.select()
    result = await session.execute(query)
    return {"data": result.all(), "status": 200}


@router.get("/products/")
async def retrieve_product(
    product_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = select(product).where(product.c.id == product_id)
    result = await session.execute(query)
    return {"data": result.all(), "status": 200}


@router.post("/create-product/")
async def create_product(
    new_product: ProductCreateSchema, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(product).values(**new_product.dict())
    await session.execute(stmt)
    await session.commit()
    return {"data": new_product.dict(), "status": 200}
