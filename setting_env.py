from dotenv import load_dotenv
import os

load_dotenv("setting.env")

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

PORT = int(os.environ.get("PORT", 5000))

RDB_PATH = os.getenv("RDB_PATH")
SQLITE3_PATH = os.getenv("SQLITE3")
DB_FILE_PATH = os.getenv("DB_FILE_PATH")