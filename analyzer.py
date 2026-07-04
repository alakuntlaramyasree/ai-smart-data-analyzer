import pandas as pd

from gemini_service import ask_gemini


def analyze_reviews(df):

    reviews = "\n".join(df.iloc[:,0].astype(str))

    prompt = f"""
Analyze these customer reviews.

Provide:

1. Overall sentiment
2. Top complaints
3. Positive points
4. Suggestions

Reviews:

{reviews}
"""

    return ask_gemini(prompt)


def analyze_stock(df):

    summary = f"""

Rows : {len(df)}

Highest Close : {df['Close'].max()}

Lowest Close : {df['Close'].min()}

Average Close : {df['Close'].mean()}

Average Volume : {df['Volume'].mean()}
"""

    prompt = f"""

Explain this stock dataset.

{summary}

Give trends and recommendations.
"""

    return ask_gemini(prompt)


def analyze_sales(df):

    prompt = f"""

Dataset Summary

{df.describe().to_string()}

Explain the business insights.
"""

    return ask_gemini(prompt)


def analyze_student(df):

    prompt = f"""

Student Dataset

{df.describe(include='all').to_string()}

Summarize performance.
"""

    return ask_gemini(prompt)


def analyze_general(df):

    prompt = f"""

Dataset

Columns

{list(df.columns)}

Statistics

{df.describe(include='all').to_string()}

Provide insights.
"""

    return ask_gemini(prompt)