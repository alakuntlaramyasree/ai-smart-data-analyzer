import pandas as pd
import numpy as np


def profile_dataset(df):
    """
    Create a complete profile of the uploaded dataset.
    """

    profile = {}

    # Basic Information
    profile["rows"] = len(df)
    profile["columns"] = len(df.columns)
    profile["column_names"] = list(df.columns)

    # Missing Values
    profile["missing_values"] = df.isnull().sum().to_dict()
    profile["total_missing"] = int(df.isnull().sum().sum())

    # Duplicate Rows
    profile["duplicate_rows"] = int(df.duplicated().sum())

    # Data Types
    profile["data_types"] = {
        col: str(dtype)
        for col, dtype in df.dtypes.items()
    }

    # Numeric Columns
    numeric_cols = df.select_dtypes(include=np.number)

    profile["numeric_columns"] = list(numeric_cols.columns)

    # Text Columns
    text_cols = df.select_dtypes(include="object")

    profile["text_columns"] = list(text_cols.columns)

    return profile


def numeric_summary(df):

    numeric = df.select_dtypes(include=np.number)

    if numeric.empty:
        return {}

    summary = {}

    for column in numeric.columns:

        summary[column] = {

            "mean": round(float(numeric[column].mean()), 2),

            "median": round(float(numeric[column].median()), 2),

            "minimum": round(float(numeric[column].min()), 2),

            "maximum": round(float(numeric[column].max()), 2),

            "std": round(float(numeric[column].std()), 2)

        }

    return summary


def categorical_summary(df):

    summary = {}

    object_cols = df.select_dtypes(include="object")

    for column in object_cols.columns:

        summary[column] = (

            object_cols[column]

            .astype(str)

            .value_counts()

            .head(5)

            .to_dict()

        )

    return summary


def correlation_matrix(df):

    numeric = df.select_dtypes(include=np.number)

    if len(numeric.columns) < 2:
        return {}

    corr = numeric.corr()

    return corr.round(2).to_dict()


def detect_outliers(df):

    numeric = df.select_dtypes(include=np.number)

    result = {}

    for column in numeric.columns:

        Q1 = numeric[column].quantile(0.25)

        Q3 = numeric[column].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR

        upper = Q3 + 1.5 * IQR

        count = numeric[
            (numeric[column] < lower) |
            (numeric[column] > upper)
        ].shape[0]

        result[column] = int(count)

    return result


def memory_usage(df):

    memory = df.memory_usage(deep=True).sum()

    return round(memory / (1024 * 1024), 2)


def quality_score(df):

    rows = len(df)

    cols = len(df.columns)

    total_cells = rows * cols

    if total_cells == 0:
        return 0

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    score = 100

    score -= (missing / total_cells) * 60

    if rows > 0:
        score -= (duplicates / rows) * 40

    score = max(0, round(score))

    return score


def full_profile(df):

    return {

        "basic": profile_dataset(df),

        "numeric": numeric_summary(df),

        "categorical": categorical_summary(df),

        "correlation": correlation_matrix(df),

        "outliers": detect_outliers(df),

        "memory_mb": memory_usage(df),

        "quality_score": quality_score(df)

    }