from contextlib import asynccontextmanager

from controller.abc import ABC
from controller.rfm import RFM
from db import database as db
from fastapi import APIRouter
from models import PurchaseData, ResultABC, ResultRFM


@asynccontextmanager
async def lifespan(router: APIRouter):
    try:
        await db.connect()
        yield
    finally:
        await db.disconnect()


router = APIRouter(lifespan=lifespan)


@router.get("/connection")
async def read_root():
    return {"connection": "OK"}


@router.get("/read/{table_name}")
async def read_data(table_name: str, q: int = 10) -> list[PurchaseData]:
    query = f"SELECT * FROM {table_name} LIMIT {q};"
    rows = await db.fetch_all(query)
    return [PurchaseData(**row) for row in rows]


@router.get("/read/{table_name}/abc")
async def get_abc_analysis(table_name: str) -> list[ResultABC]:
    query = f"""
        SELECT section_name, sum(price)/count(price), sum(price) 
        FROM {table_name}
        WHERE price > 0 and card_id is NULL
        GROUP BY section_name;
        """
    rows = await db.fetch_all(query)
    rows_dict = [dict(row) for row in rows]

    controller = ABC(rows_dict)
    result = controller.abc_analysis()
    return [ResultABC(**row) for row in result.to_dict(orient="records")]


@router.get("/read/{table_name}/rfm")
async def get_rfm_analysis(table_name: str) -> list[ResultRFM]:
    # select card_id, date, sum(total_price)/count(total_price) from store_07.takara where card_id is not null group by card_id, date
    query = f"""
        SELECT card_id, date, sum(total_price)/count(total_price)
        FROM {table_name}
        WHERE card_id is not NULL
        GROUP BY card_id, date;
        """
    rows = await db.fetch_all(query)
    rows_dict = [dict(row) for row in rows]

    controller = RFM(rows_dict)
    result = controller.rfm_analysis()
    return [ResultRFM(**row) for row in result.to_dict(orient="records")]
