import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

ALLOWED_EXTENSIONS = {
    "csv",
    "xlsx",
    "xls",
    "json"
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")