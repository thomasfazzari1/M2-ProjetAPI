import psycopg2
from config import Config


def get_db_connection():
    return psycopg2.connect(
        host=Config.PAIEMENT_DB_HOST,
        user=Config.PAIEMENT_DB_USER,
        password=Config.PAIEMENT_DB_PASSWORD,
        dbname=Config.PAIEMENT_DB_NAME
    )
