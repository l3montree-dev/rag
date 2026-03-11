import os
from dotenv import load_dotenv

load_dotenv()

PATH_DIR = os.getenv("DOCS_PATH")

CHUNK_SIZE = 800
OVERLAP_SIZE = 120 # overlap rule of thumb: around 10-20% of chunk size
BATCH_SIZE = 50

MODEL_EMBEDDING = "mistral-embed"
MODEL_GENERATION = "mistral-medium-2508" # alternatively use: "mistral-small-2506"

DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = "db"
DB_PORT = 5432
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

API_KEY = os.getenv("API_KEY")
