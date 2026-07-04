from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import json

from config import *
from detector import detect_dataset
from analyzer import (
    analyze_reviews,
    analyze_stock,
    analyze_sales,
    analyze_student,
    analyze_general
)
from charts import (
    stock_line_chart,
    sales_bar_chart,
    sentiment_pie_chart,
    histogram_chart
)

from smart_ai import smart_ai_analyzer

app = Flask(__name__)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -----------------------------
# Helper Functions
# -----------------------------

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def read_file(filepath):

    extension = filepath.split(".")[-1].lower()

    if extension == "csv":
        return pd.read_csv(filepath)

    elif extension in ["xlsx", "xls"]:
        return pd.read_excel(filepath)

    elif extension == "json":
        return pd.read_json(filepath)

    else:
        return None


def dataset_summary(df):

    summary = {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Column Names": list(df.columns),
        "Missing Values": df.isnull().sum().to_dict(),
        "Duplicate Rows": int(df.duplicated().sum())
    }

    return summary


# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return "No file uploaded."

    file = request.files["file"]

    if file.filename == "":
        return "Please select a file."

    if not allowed_file(file.filename):
        return "Unsupported file format."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    df = read_file(filepath)

    if df is None:
        return "Unable to read file."

    dataset_type = detect_dataset(df)

    summary = dataset_summary(df)

    # -------------------------
    # Route Analysis
    # -------------------------

    ai_result = smart_ai_analyzer(df, dataset_type)

    # Save original dataset

    output_file = os.path.join(
        RESULT_FOLDER,
        "analyzed_data.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    preview = df.head(20).to_html(
        classes="table table-striped",
        index=False
    )

    # -------------------------
    # Generate Charts
    # -------------------------

    chart_html = ""

    if dataset_type == "stock":
        chart_html = stock_line_chart(df)

    elif dataset_type == "sales":
        chart_html = sales_bar_chart(df)

    elif dataset_type == "reviews":
        chart_html = sentiment_pie_chart(df)

    else:
        chart_html = histogram_chart(df)

    return render_template(
    "dashboard.html",
    dataset_type=dataset_type.title(),
    summary=summary,
    ai_result=ai_result,
    preview=preview,
    chart=chart_html
)


@app.route("/download")
def download():

    return send_file(
        os.path.join(
            RESULT_FOLDER,
            "analyzed_data.csv"
        ),
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)