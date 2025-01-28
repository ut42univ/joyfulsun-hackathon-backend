from contextlib import asynccontextmanager

from db import database as db
from fastapi import APIRouter
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
    return {"connection": "OK"}


@router.get("/read/{table_name}")
async def read_data(table_name: str, q: int = 10) -> list[PurchaseData]:
    query = f"SELECT * FROM {table_name} LIMIT {q};"
    rows = await db.fetch_all(query)
    return [PurchaseData(**row) for row in rows]
