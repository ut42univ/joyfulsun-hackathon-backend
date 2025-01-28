from contextlib import asynccontextmanager

from fastapi import APIRouter

from db import database as db
from models import PurchaseData


@asynccontextmanager
async def lifespan(router: APIRouter):
    try:
        await db.connect()
        yield
    finally:
        await db.disconnect()


router = APIRouter(lifespan=lifespan)


@router.get("/")
async def read_root():
    return {"Hello": "World"}


@router.get("/read")
async def read_data(q: int = 10) -> list[PurchaseData]:
    query = f"SELECT * FROM store LIMIT {q};"
    rows = await db.fetch_all(query)
    return [PurchaseData(**row) for row in rows]
