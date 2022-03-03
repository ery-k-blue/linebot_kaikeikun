from dotenv import load_dotenv
import os

load_dotenv("setting.env")

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

RDB_PATH = os.getenv("RDB_PATH")
DB_FILE_PATH = os.getenv("DB_FILE_PATH")