import pandas as pd


class CleaningExecutor:

    def execute(self, df: pd.DataFrame, report: dict, plan: dict):

        cleaning_summary = {
            "duplicates_removed": 0,
            "numeric_missing_strategy": None,
            "categorical_missing_strategy": None,
            "date_columns_converted": [],
            "invalid_rows_removed": 0
        }

        # Remove duplicate rows
        if plan.get("remove_duplicates", False):

            before = len(df)

            df = self.remove_duplicates(df)

            after = len(df)

            cleaning_summary["duplicates_removed"] = before - after

        # Fill missing numeric values
        strategy = plan.get("fill_numeric_missing")

        if strategy:

            df = self.fill_numeric_missing(df, strategy)

            cleaning_summary["numeric_missing_strategy"] = strategy

        # Fill missing categorical values
        strategy = plan.get("fill_categorical_missing")

        if strategy:

            df = self.fill_categorical_missing(df, strategy)

            cleaning_summary["categorical_missing_strategy"] = strategy

        # Convert date columns
        if plan.get("convert_date_columns", False):

            df = self.convert_date_columns(df, report["date_columns"])

            cleaning_summary["date_columns_converted"] = report["date_columns"]

        # Remove invalid rows
        if plan.get("remove_invalid_rows", False):

            before = len(df)

            df = self.remove_invalid_rows(df)

            after = len(df)

            cleaning_summary["invalid_rows_removed"] = before - after

        return df, cleaning_summary

    # -------------------------------------------------------
    # Remove duplicate rows
    # -------------------------------------------------------

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:

        return df.drop_duplicates()

    # -------------------------------------------------------
    # Fill numeric missing values
    # -------------------------------------------------------

    def fill_numeric_missing(self, df: pd.DataFrame, strategy: str) -> pd.DataFrame:

        numeric_columns = df.select_dtypes(include="number").columns

        for column in numeric_columns:

            if strategy == "mean":
                df[column] = df[column].fillna(df[column].mean())

            elif strategy == "median":
                df[column] = df[column].fillna(df[column].median())

            elif strategy == "zero":
                df[column] = df[column].fillna(0)

        return df

    # -------------------------------------------------------
    # Fill categorical missing values
    # -------------------------------------------------------

    def fill_categorical_missing(self, df: pd.DataFrame, strategy: str) -> pd.DataFrame:

        categorical_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in categorical_columns:

            if strategy == "mode":

                mode = df[column].mode()

                if not mode.empty:
                    df[column] = df[column].fillna(mode.iloc[0])

        return df

    # -------------------------------------------------------
    # Convert date columns
    # -------------------------------------------------------

    def convert_date_columns(
        self,
        df: pd.DataFrame,
        date_columns: list
    ) -> pd.DataFrame:

        for column in date_columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

        return df

    # -------------------------------------------------------
    # Remove invalid rows
    # -------------------------------------------------------

    def remove_invalid_rows(self, df: pd.DataFrame) -> pd.DataFrame:

        numeric_columns = df.select_dtypes(include="number").columns

        for column in numeric_columns:

            df = df[df[column] >= 0]

        return df

    # -------------------------------------------------------
    # Save cleaned dataset
    # -------------------------------------------------------

    def save_dataset(
        self,
        df: pd.DataFrame,
        output_path: str
    ) -> None:

        if output_path.endswith(".csv"):

            df.to_csv(output_path, index=False)

        elif output_path.endswith((".xlsx", ".xls")):

            df.to_excel(output_path, index=False)

        else:

            raise ValueError("Unsupported output format.")