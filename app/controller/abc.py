import numpy as np
import pandas as pd


class ABC:
    df: pd.DataFrame = None
    df_sorted: pd.DataFrame = None

    def __init__(self, rows: list[dict]):
        self.df = pd.DataFrame(rows)

    def abc_analysis(self) -> pd.DataFrame:
        self.df.columns = ["category", "price", "sales"]
        self.df_sorted = self.df.sort_values(by="sales", ascending=False)
        self.df_sorted["cumulative_percentage"] = (
            np.cumsum(self.df_sorted["sales"]) / self.df_sorted["sales"].sum()
        )

        self.df_sorted["classed_as"] = pd.cut(
            self.df_sorted["cumulative_percentage"],
            bins=[0, 0.7, 0.9, 1.0],
            labels=["A", "B", "C"],
        )
        return self.df_sorted


if __name__ == "__main__":
    dummy_data = [
        {"section_name": "テスト", "column": 564, "sum": 880612},
        {"section_name": "その他", "column": 4, "sum": 28984},
    ]

    controller = ABC(dummy_data)
    result = controller.abc_analysis()
    print(result.to_dict(orient="records"))
