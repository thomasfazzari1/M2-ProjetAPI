import os


class Config:
    PAIEMENT_DB_HOST = os.getenv("PAIEMENT_DB_HOST")
    PAIEMENT_DB_USER = os.getenv("PAIEMENT_DB_USER")
    PAIEMENT_DB_PASSWORD = os.getenv("PAIEMENT_DB_PASSWORD")
    PAIEMENT_DB_NAME = os.getenv("PAIEMENT_DB_NAME")
