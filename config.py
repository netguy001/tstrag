import os
import shutil
from dotenv import load_dotenv

load_dotenv()


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    UPLOAD_FOLDER = "uploads"
    DATABASE_PATH = "database/chroma_db"
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 100
    TOP_K_RESULTS = 5
    MODEL_NAME = "llama-3.3-70b-versatile"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # If database exists but is corrupted, remove it
    if os.path.exists(DATABASE_PATH):
        db_file = os.path.join(DATABASE_PATH, "chroma.sqlite3")
        if os.path.exists(db_file):
            try:
                # Try to check if database is accessible
                import sqlite3

                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                conn.close()

                # Check if required table exists
                table_names = [t[0] for t in tables]
                if "collections" not in table_names:
                    print("⚠️  Corrupted database detected. Recreating...")
                    shutil.rmtree(DATABASE_PATH)
                    os.makedirs(DATABASE_PATH, exist_ok=True)
            except Exception as e:
                print(f"⚠️  Database error: {e}. Recreating...")
                shutil.rmtree(DATABASE_PATH)
                os.makedirs(DATABASE_PATH, exist_ok=True)
    else:
        os.makedirs(DATABASE_PATH, exist_ok=True)
