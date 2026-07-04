def detect_dataset(df):

    cols = [c.lower() for c in df.columns]

    if any(col in cols for col in ["review", "reviews", "feedback", "comment"]):
        return "reviews"

    if {"open", "high", "low", "close"}.issubset(cols):
        return "stock"

    if any(col in cols for col in ["sales", "revenue", "quantity"]):
        return "sales"

    if any(col in cols for col in ["marks", "attendance", "student"]):
        return "student"

    if any(col in cols for col in ["survey", "response"]):
        return "survey"

    return "general"