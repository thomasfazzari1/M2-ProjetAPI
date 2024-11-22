import os


class Config:
    PARI_DB_HOST = os.getenv("PARI_DB_HOST")
    PARI_DB_USER = os.getenv("PARI_DB_USER")
    PARI_DB_PASSWORD = os.getenv("PARI_DB_PASSWORD")
    PARI_DB_NAME = os.getenv("PARI_DB_NAME")
