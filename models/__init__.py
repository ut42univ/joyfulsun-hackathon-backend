from datetime import date, time

from pydantic import BaseModel


class PurchaseData(BaseModel):
    store_id: int
    store_name: str
    receipt_id: int
    date: date
    time: time
    section_id: int
    section_name: str
    subcategory_id: int
    subcategory_name: str
    class_id: int
    class_name: str
    product_id: int
    product_name: str
    price: int
    quantity: int
    total_price: int
    card_id: int | None
    address: int | None
    age: int | None
    gender: str | None
