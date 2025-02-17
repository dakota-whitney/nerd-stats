from shiny import render
import pandas as pd
import pathlib

dir_ = pathlib.Path(__file__).parent
excel_ = dir_ / "data.xlsx"

class ShinyDF:
    df_ = pd.DataFrame()

    @staticmethod
    def data_table(df: pd.DataFrame): return render.DataTable(
        df,
        width = "100%",
        height = "750px",
        summary = False,
        selection_mode = "rows"
    )

    @classmethod
    def get(self, col_attr: str = "", index: pd.Index|list|tuple = pd.Index([]), *col_attrs):
        if len(index): return self.df_.loc[index]
        elif col_attr == "Index": return self.df_.index
        elif col_attr in self.df_.columns: return self.df_[col_attr]
        elif col_attr and hasattr(self, col_attr + "_"): return getattr(self, col_attr + "_")
        elif col_attrs: return [self.df[a] if a in self.df_.columns else getattr(self, a + "_") for a in col_attrs]
        else: return self.df_.copy()

    @classmethod
    def set(self, **col_attrs):
        for k, v in col_attrs.items():
            if k in self.df_.columns : self.df_[k] = v
            else: setattr(self, k + "_", v)
        return self
    
    @classmethod
    def range(self, col: str, seq: bool = True):
        r = range(self.df_[col].min(), self.df_[col].max() + 1)
        return list(r) if seq else r
     
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.q = ""
    
    def query(self, q: str = "", strict: bool = False):
        if q: self.q += q + ("&" if strict else "|")
        elif self.q: self.df = self.df.query(self.q[:-1])
        return self