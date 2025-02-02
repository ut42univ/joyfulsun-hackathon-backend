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


class ResultABC(BaseModel):
    """
    Result of ABC Analysis Model

    category: 商品名
    price: 価格
    sales: 売上高
    cumulative_percentage: 累積構成比
    classed_as: ABCクラス
    """

    category: str
    price: float
    sales: float
    cumulative_percentage: float
    classed_as: str


class ResultRFM(BaseModel):
    """
    Result of RFM Analysis Model

    Recency: 最終購入日からの日数
    Frequency: 購入回数
    Monetary: 購入金額
    R_score: Rスコア
    F_score: Fスコア
    M_score: Mスコア
    """

    recency: int
    frequency: int
    monetary: int
    r_score: int
    f_score: int
    m_score: int
