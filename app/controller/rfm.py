import numpy as np
import pandas as pd


class RFM:
    df: pd.DataFrame = None
    df_rfm: pd.DataFrame = None

    def __init__(self, rows: list[dict]):
        self.df = pd.DataFrame(rows)
        self.df["date"] = pd.to_datetime(self.df["date"])

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

        # r_score: 降順スコア
        _, bin_edges_r = pd.qcut(
            rank_rfm["recency"], 5, duplicates="drop", retbins=True
        )
        n_bins_r = len(bin_edges_r) - 1
        labels_r = [str(i) for i in range(n_bins_r, 0, -1)]
        rank_rfm["r_score"] = pd.cut(
            rank_rfm["recency"], bins=bin_edges_r, labels=labels_r, include_lowest=True
        )

        # f_score: 昇順スコア
        _, bin_edges_f = pd.qcut(
            rank_rfm["frequency"].rank(method="first"),
            5,
            duplicates="drop",
            retbins=True,
        )
        n_bins_f = len(bin_edges_f) - 1
        labels_f = [str(i) for i in range(1, n_bins_f + 1)]
        rank_rfm["f_score"] = pd.cut(
            rank_rfm["frequency"].rank(method="first"),
            bins=bin_edges_f,
            labels=labels_f,
            include_lowest=True,
        ).astype(int)

        # m_score: 昇順スコア
        _, bin_edges_m = pd.qcut(
            rank_rfm["monetary"], 5, duplicates="drop", retbins=True
        )
        n_bins_m = len(bin_edges_m) - 1
        labels_m = [str(i) for i in range(1, n_bins_m + 1)]
        rank_rfm["m_score"] = pd.cut(
            rank_rfm["monetary"], bins=bin_edges_m, labels=labels_m, include_lowest=True
        )

        return rank_rfm
