import pandas as pd


class DatasetAnalyzer:

    # Read dataset
    def read_dataset(self, file_path: str) -> pd.DataFrame:

        if file_path.endswith(".csv"):
            df = pd.read_csv(
                file_path,
                engine="python",
                on_bad_lines="skip"
            )

        elif file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)

        else:
            raise ValueError("Unsupported file format.")

        if df.empty:
            raise ValueError("Dataset is empty.")

        return df

    # Detect duplicate rows
    def detect_duplicates(self, df: pd.DataFrame) -> int:
        return int(df.duplicated().sum())

    # Detect missing values
    def detect_missing_values(self, df: pd.DataFrame) -> dict:
        return df.isnull().sum().to_dict()

    # Detect data types
    def detect_data_types(self, df: pd.DataFrame) -> dict:
        return df.dtypes.astype(str).to_dict()

    # Detect date columns
    def detect_date_columns(self, df: pd.DataFrame) -> list:

        keywords = [
            "date",
            "time",
            "timestamp",
            "dob",
            "birth"
        ]

        date_columns = []

        for column in df.columns:

            if any(keyword in column.lower() for keyword in keywords):

                try:
                    pd.to_datetime(df[column], errors="raise")
                    date_columns.append(column)

                except Exception:
                    pass

        return date_columns

    # Detect invalid numeric values
    def detect_invalid_values(self, df: pd.DataFrame) -> dict:

        invalid_values = {}

        numeric_columns = df.select_dtypes(include="number").columns

        for column in numeric_columns:

            count = int((df[column] < 0).sum())

            if count > 0:
                invalid_values[column] = count

        return invalid_values

    # Analyze dataset
    def analyze_dataset(self, df: pd.DataFrame) -> dict:

        report = {
            "rows": len(df),
            "columns": len(df.columns),
            "duplicates": self.detect_duplicates(df),
            "missing_values": self.detect_missing_values(df),
            "data_types": self.detect_data_types(df),
            "date_columns": self.detect_date_columns(df),
            "invalid_values": self.detect_invalid_values(df),
            "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
            "categorical_columns": df.select_dtypes(include=["object", "string"]).columns.tolist(),
        }

        return report