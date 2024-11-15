import psycopg2
from config import Config


def get_db_connection():
    return psycopg2.connect(
        host=Config.AUTH_DB_HOST,
        user=Config.AUTH_DB_USER,
        password=Config.AUTH_DB_PASSWORD,
        dbname=Config.AUTH_DB_NAME
    )
