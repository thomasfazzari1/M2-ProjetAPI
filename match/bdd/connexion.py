import psycopg2
from config import Config


def get_db_connection():
    return psycopg2.connect(
        host=Config.MATCH_DB_HOST,
        user=Config.MATCH_DB_USER,
        password=Config.MATCH_DB_PASSWORD,
        dbname=Config.MATCH_DB_NAME
    )
