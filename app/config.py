import os
from dotenv import load_dotenv

load_dotenv()

PATH_DIR = os.getenv("DOCS_PATH")

CHUNK_SIZE = 1000
OVERLAP_SIZE = 50
BATCH_SIZE = 20

MODEL_EMBEDDING = "mistral-embed"
MODEL_GENERATION = "mistral-small-2506"

DB_NAME = "embedding_db"
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

API_KEY = os.getenv("API_KEY")
