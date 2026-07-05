import pandas as pd


def detect_dataset(df: pd.DataFrame) -> str:
    """
    Automatically detect dataset type based on columns and patterns.
    Returns: stock | sales | reviews | student | general
    """

    columns = [col.lower() for col in df.columns]

    # ------------------------------------
    # 1. Reviews Dataset
    # ------------------------------------
    review_keywords = ["review", "rating", "comment", "feedback", "sentiment"]

    if any(col in " ".join(columns) for col in review_keywords):
        return "reviews"


    # ------------------------------------
    # 2. Stock Market Dataset
    # ------------------------------------
    stock_keywords = ["open", "close", "high", "low", "volume", "price", "date"]

    if any(col in columns for col in stock_keywords):
        return "stock"


    # ------------------------------------
    # 3. Sales Dataset
    # ------------------------------------
    sales_keywords = ["sales", "revenue", "profit", "quantity", "amount", "order"]

    if any(col in " ".join(columns) for col in sales_keywords):
        return "sales"


    # ------------------------------------
    # 4. Student Dataset
    # ------------------------------------
    student_keywords = ["marks", "score", "grade", "student", "attendance"]

    if any(col in " ".join(columns) for col in student_keywords):
        return "student"


    # ------------------------------------
    # Default
    # ------------------------------------
    return "general"