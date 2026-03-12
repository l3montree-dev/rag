import psycopg2
from mistralai import Mistral
from app.config import *

def get_mistral_client() -> Mistral:
    """Create and return a Mistral AI client instance"""
    return Mistral(api_key=API_KEY)

def get_db_connection():
    """Establish and return a connection to the PostgreSQL database"""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
