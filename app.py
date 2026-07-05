from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
    flash
)

import os
import traceback
import pandas as pd

from config import *

from detector import detect_dataset

from profiler import full_profile

from smart_ai import smart_ai_analyzer

from charts import generate_dashboard

from database import (
    init_db,
    save_analysis,
    get_history,
    delete_analysis,
    total_analysis
)

app = Flask(__name__)

app.secret_key = "AI_SMART_ANALYZER"

init_db()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


####################################################
# Helper Functions
####################################################

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".",1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def read_dataset(filepath):

    extension = filepath.split(".")[-1].lower()

    if extension == "csv":
        return pd.read_csv(filepath)

    elif extension in ["xlsx","xls"]:
        return pd.read_excel(filepath)

    elif extension == "json":
        return pd.read_json(filepath)

    else:
        return None


####################################################
# HOME
####################################################

@app.route("/")
def home():

    history = get_history()

    total = total_analysis()

    return render_template(

        "index.html",

        history=history,

        total_analysis=total

    )


####################################################
# HISTORY
####################################################

@app.route("/history")
def history():

    history = get_history()

    return render_template(

        "history.html",

        history=history

    )


####################################################
# DELETE HISTORY
####################################################

@app.route("/delete/<int:id>")
def delete(id):

    delete_analysis(id)

    flash("History deleted successfully.")

    return redirect("/history")


####################################################
# DOWNLOAD
####################################################

@app.route("/download")
def download():

    return send_file(

        os.path.join(

            RESULT_FOLDER,

            "analyzed_data.csv"

        ),

        as_attachment=True

    )


####################################################
# UPLOAD
####################################################

@app.route("/upload", methods=["POST"])
def upload():

    try:

        if "file" not in request.files:

            flash("No file selected.")

            return redirect("/")

        file = request.files["file"]

        if file.filename == "":

            flash("Please choose a file.")

            return redirect("/")

        if not allowed_file(file.filename):

            flash("Unsupported file.")

            return redirect("/")

        filepath = os.path.join(

            app.config["UPLOAD_FOLDER"],

            file.filename

        )

        file.save(filepath)

        df = read_dataset(filepath)

        if df is None:

            flash("Unable to read file.")

            return redirect("/")

        dataset_type = detect_dataset(df)

        profile = full_profile(df)

        quality_score = profile["quality_score"]

        ai_result = smart_ai_analyzer(

            df,

            dataset_type

        )

        save_analysis(

            filename=file.filename,

            dataset_type=dataset_type,

            rows=len(df),

            columns=len(df.columns),

            quality_score=quality_score,

            ai_summary=ai_result

        )

        output_file = os.path.join(

            RESULT_FOLDER,

            "analyzed_data.csv"

        )

        df.to_csv(

            output_file,

            index=False

        )

        preview = df.head(

            MAX_PREVIEW_ROWS

        ).to_html(

            index=False,

            classes="table"

        )

        charts = generate_dashboard(

            df,

            dataset_type

        )

        return render_template(

            "dashboard.html",

            app_name=APP_NAME,

            dataset_type=dataset_type.title(),

            filename=file.filename,

            summary=profile["basic"],

            quality_score=quality_score,

            ai_result=ai_result,

            preview=preview,

            charts=charts,

            numeric_summary=profile["numeric"],

            categorical_summary=profile["categorical"],

            correlation=profile["correlation"],

            outliers=profile["outliers"],

            memory=profile["memory_mb"]

        )

    except Exception as e:

        traceback.print_exc()

        return render_template(

            "error.html",

            error=str(e)

        )


####################################################
# ERROR HANDLER
####################################################

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "error.html",

        error="Page not found."

    ), 404


####################################################
# SERVER
####################################################

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )