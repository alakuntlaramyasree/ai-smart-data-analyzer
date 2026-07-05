import os

# ==========================================
# APP CONFIGURATION
# ==========================================

APP_NAME = "AI Smart Data Analyzer Pro"

# Upload settings
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

# Allowed file types
ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "json"}

# Preview settings
MAX_PREVIEW_ROWS = 50

# AI Settings
AI_MODEL = "gemini-2.5-flash"

# ==========================================
# DATABASE CONFIG
# ==========================================

DATABASE_PATH = os.path.join("database", "analysis.db")

# ==========================================
# UI SETTINGS
# ==========================================

THEME = "light"

PRIMARY_COLOR = "#4a69bd"

SECONDARY_COLOR = "#6a89cc"

# ==========================================
# CHART SETTINGS
# ==========================================

CHART_HEIGHT = 500

ENABLE_PLOTLY_MODEBAR = True

# ==========================================
# SAFETY SETTINGS
# ==========================================

ENABLE_FILE_VALIDATION = True

MAX_FILE_SIZE_MB = 20