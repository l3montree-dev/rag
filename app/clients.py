import psycopg2
from mistralai import Mistral
from app.config import *

def get_mistral_client() -> Mistral:
    return Mistral(api_key=API_KEY)

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
