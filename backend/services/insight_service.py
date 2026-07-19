import pandas as pd


class InsightService:
    """
    Generates a generic statistical profile for any tabular dataset.
    This profile is later passed to the LLM to generate business insights.
    """

    def generate_profile(self, df: pd.DataFrame) -> dict:

        profile = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "numeric_columns": {},
            "categorical_columns": {},
            "datetime_columns": {}
        }

    

        numeric_cols = df.select_dtypes(include="number").columns

        for column in numeric_cols:

            profile["numeric_columns"][column] = {
                "min": float(df[column].min()),
                "max": float(df[column].max()),
                "mean": round(float(df[column].mean()), 2),
                "median": round(float(df[column].median()), 2),
                "std": round(float(df[column].std()), 2)
                if df[column].std() is not None else 0,
                "missing": int(df[column].isnull().sum())
            }

      

        categorical_cols = df.select_dtypes(
            include=["object", "string", "category"]
        ).columns

        for column in categorical_cols:

            profile["categorical_columns"][column] = {
                "unique_values": int(df[column].nunique()),
                "missing": int(df[column].isnull().sum()),
                "top_values": (
                    df[column]
                    .value_counts()
                    .head(5)
                    .to_dict()
                )
            }

      

        for column in df.columns:

            try:

                converted = pd.to_datetime(
                    df[column],
                    errors="raise"
                )

                profile["datetime_columns"][column] = {
                    "start_date": str(converted.min()),
                    "end_date": str(converted.max())
                }

            except Exception:
                continue

   

        if len(numeric_cols) >= 2:

            corr = (
                df[numeric_cols]
                .corr()
                .round(2)
                .fillna(0)
            )

            profile["correlations"] = corr.to_dict()

        else:

            profile["correlations"] = {}

        return profile