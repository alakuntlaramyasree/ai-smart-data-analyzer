import plotly.express as px
import pandas as pd


# -------------------------
# STOCK CHART
# -------------------------
def stock_line_chart(df):

    fig = px.line(
        df,
        x=df.index,
        y="Close",
        title="Stock Closing Price Trend"
    )

    return fig.to_html(full_html=False)


# -------------------------
# SALES BAR CHART
# -------------------------
def sales_bar_chart(df):

    if "Product" in df.columns and "Sales" in df.columns:

        grouped = df.groupby("Product")["Sales"].sum().reset_index()

        fig = px.bar(
            grouped,
            x="Product",
            y="Sales",
            title="Sales by Product"
        )

        return fig.to_html(full_html=False)

    return "<p>No sales chart available</p>"


# -------------------------
# REVIEW SENTIMENT PIE
# -------------------------
def sentiment_pie_chart(df):

    if "sentiment" in df.columns:

        counts = df["sentiment"].value_counts().reset_index()
        counts.columns = ["Sentiment", "Count"]

        fig = px.pie(
            counts,
            names="Sentiment",
            values="Count",
            title="Sentiment Distribution"
        )

        return fig.to_html(full_html=False)

    return "<p>No sentiment data found</p>"


# -------------------------
# GENERAL HISTOGRAM
# -------------------------
def histogram_chart(df):

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        fig = px.histogram(
            df,
            x=numeric_cols[0],
            title=f"Distribution of {numeric_cols[0]}"
        )

        return fig.to_html(full_html=False)

    return "<p>No numeric data available</p>"