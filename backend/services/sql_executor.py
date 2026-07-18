import duckdb
import pandas as pd


class SQLExecutor:

    def __init__(self):
        self.conn = duckdb.connect()

    def load_dataset(self, file_path: str) -> pd.DataFrame:

        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)

        elif file_path.endswith((".xlsx", ".xls")):
            return pd.read_excel(file_path)

        else:
            raise ValueError("Unsupported file format.")

    def get_schema(self, df: pd.DataFrame) -> dict:

        return df.dtypes.astype(str).to_dict()

    def execute_query(
        self,
        df: pd.DataFrame,
        sql_query: str
    ) -> pd.DataFrame:

        self.conn.register("dataset", df)

        result = self.conn.execute(sql_query).fetchdf()

        return result

    def close(self):

        self.conn.close()