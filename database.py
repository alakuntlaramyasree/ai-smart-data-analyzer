import sqlite3
from datetime import datetime
import os

DB_PATH = "database/analysis.db"


# -----------------------------------
# Initialize Database
# -----------------------------------

def init_db():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS analysis_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            dataset_type TEXT,

            rows INTEGER,

            columns INTEGER,

            quality_score INTEGER,

            ai_summary TEXT,

            created_at TEXT

        )

    """)

    conn.commit()
    conn.close()


# -----------------------------------
# Save Analysis
# -----------------------------------

def save_analysis(filename, dataset_type, rows, columns, quality_score, ai_summary):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO analysis_history (

            filename,

            dataset_type,

            rows,

            columns,

            quality_score,

            ai_summary,

            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        filename,

        dataset_type,

        rows,

        columns,

        quality_score,

        ai_summary,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()
    conn.close()


# -----------------------------------
# Get History
# -----------------------------------

def get_history():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM analysis_history

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# -----------------------------------
# Delete Record
# -----------------------------------

def delete_analysis(record_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM analysis_history

        WHERE id = ?

    """, (record_id,))

    conn.commit()
    conn.close()


# -----------------------------------
# Total Count
# -----------------------------------

def total_analysis():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*) FROM analysis_history

    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count