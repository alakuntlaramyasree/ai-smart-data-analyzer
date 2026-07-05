import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _numeric_columns(df):
    return df.select_dtypes(include="number").columns.tolist()


def _date_columns(df):
    cols = []

    for col in df.columns:
        try:
            pd.to_datetime(df[col])
            cols.append(col)
        except:
            pass

    return cols


# --------------------------------------------------
# Histogram
# --------------------------------------------------

def histogram_chart(df):

    numeric = _numeric_columns(df)

    if len(numeric) == 0:
        return "<h4>No numeric columns found.</h4>"

    fig = px.histogram(
        df,
        x=numeric[0],
        title=f"Distribution of {numeric[0]}"
    )

    fig.update_layout(height=450)

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )


# --------------------------------------------------
# Sales Bar Chart
# --------------------------------------------------

def sales_bar_chart(df):

    numeric = _numeric_columns(df)

    if len(numeric) == 0:
        return histogram_chart(df)

    category = None

    for col in df.columns:
        if df[col].dtype == object:
            category = col
            break

    if category is None:
        category = df.columns[0]

    grouped = (
        df.groupby(category)[numeric[0]]
        .sum()
        .reset_index()
    )

    fig = px.bar(

        grouped,

        x=category,

        y=numeric[0],

        title="Sales by Category"

    )

    fig.update_layout(height=500)

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )


# --------------------------------------------------
# Stock Line Chart
# --------------------------------------------------

def stock_line_chart(df):

    numeric = _numeric_columns(df)

    if len(numeric) == 0:
        return histogram_chart(df)

    date_cols = _date_columns(df)

    if len(date_cols):

        fig = px.line(

            df,

            x=date_cols[0],

            y=numeric[0],

            title=f"{numeric[0]} Trend"

        )

    else:

        fig = px.line(

            df,

            y=numeric[0],

            title=f"{numeric[0]} Trend"

        )

    fig.update_layout(height=500)

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )


# --------------------------------------------------
# Pie Chart
# --------------------------------------------------

def sentiment_pie_chart(df):

    for col in df.columns:

        if "sentiment" in col.lower():

            counts = df[col].value_counts()

            fig = px.pie(

                values=counts.values,

                names=counts.index,

                title="Sentiment Distribution"

            )

            return fig.to_html(
                full_html=False,
                include_plotlyjs="cdn"
            )

    return histogram_chart(df)


# --------------------------------------------------
# Correlation Heatmap
# --------------------------------------------------

def correlation_heatmap(df):

    numeric = df.select_dtypes(include="number")

    if len(numeric.columns) < 2:

        return "<h4>Correlation needs at least 2 numeric columns.</h4>"

    corr = numeric.corr()

    fig = px.imshow(

        corr,

        text_auto=True,

        color_continuous_scale="Blues",

        title="Correlation Heatmap"

    )

    fig.update_layout(height=600)

    return fig.to_html(

        full_html=False,

        include_plotlyjs="cdn"

    )


# --------------------------------------------------
# Box Plot
# --------------------------------------------------

def box_plot(df):

    numeric = _numeric_columns(df)

    if len(numeric) == 0:
        return "<h4>No numeric columns.</h4>"

    fig = px.box(

        df,

        y=numeric,

        title="Outlier Detection"

    )

    fig.update_layout(height=500)

    return fig.to_html(

        full_html=False,

        include_plotlyjs="cdn"

    )


# --------------------------------------------------
# Scatter Plot
# --------------------------------------------------

def scatter_plot(df):

    numeric = _numeric_columns(df)

    if len(numeric) < 2:
        return "<h4>Need at least two numeric columns.</h4>"

    fig = px.scatter(

        df,

        x=numeric[0],

        y=numeric[1],

        title=f"{numeric[0]} vs {numeric[1]}"

    )

    fig.update_layout(height=500)

    return fig.to_html(

        full_html=False,

        include_plotlyjs="cdn"

    )


# --------------------------------------------------
# Dashboard Charts
# --------------------------------------------------

def generate_dashboard(df, dataset_type):

    charts = {}

    charts["main"] = histogram_chart(df)

    charts["box"] = box_plot(df)

    charts["scatter"] = scatter_plot(df)

    charts["heatmap"] = correlation_heatmap(df)

    if dataset_type == "sales":
        charts["special"] = sales_bar_chart(df)

    elif dataset_type == "stock":
        charts["special"] = stock_line_chart(df)

    elif dataset_type == "reviews":
        charts["special"] = sentiment_pie_chart(df)

    else:
        charts["special"] = histogram_chart(df)

    return charts