import os


class Config:
    MATCH_DB_HOST = os.getenv("MATCH_DB_HOST")
    MATCH_DB_USER = os.getenv("MATCH_DB_USER")
    MATCH_DB_PASSWORD = os.getenv("MATCH_DB_PASSWORD")
    MATCH_DB_NAME = os.getenv("MATCH_DB_NAME")
