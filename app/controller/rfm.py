import numpy as np
import pandas as pd


class RFM:
    df: pd.DataFrame = None
    df_rfm: pd.DataFrame = None

    def __init__(self, rows: list[dict]):
        self.df = pd.DataFrame(rows)

    def rfm_analysis(self) -> pd.DataFrame:
        self.df.columns = ["customer_id", "date", "total_price"]
        latest_purchase_date = self.df["date"].max()

        self.df_rfm = self.df.groupby("customer_id").aggregate(
            {
                "date": lambda x: (latest_purchase_date - x.max()).days,
                "customer_id": "count",
                "total_price": "sum",
            }
        )

        rank_rfm = self.df_rfm
        rank_rfm.columns = ["recency", "frequency", "monetary"]

        rank_rfm["r_score"] = pd.qcut(
            rank_rfm["recency"], 5, labels=["5", "4", "3", "2", "1"]
        )

        rank_rfm["f_score"] = pd.qcut(
            rank_rfm["frequency"].rank(method="first"),
            5,
            labels=["1", "2", "3", "4", "5"],
        ).astype(int)

        rank_rfm["m_score"] = pd.qcut(
            rank_rfm["monetary"], 5, labels=["1", "2", "3", "4", "5"]
        )

        return rank_rfm
