import psycopg2
from config import Config


def get_db_connection():
    return psycopg2.connect(
        host=Config.PARI_DB_HOST,
        user=Config.PARI_DB_USER,
        password=Config.PARI_DB_PASSWORD,
        dbname=Config.PARI_DB_NAME
    )
