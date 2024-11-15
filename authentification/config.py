import os


class Config:
    AUTH_DB_HOST = os.getenv("AUTH_DB_HOST")
    AUTH_DB_USER = os.getenv("AUTH_DB_USER")
    AUTH_DB_PASSWORD = os.getenv("AUTH_DB_PASSWORD")
    AUTH_DB_NAME = os.getenv("AUTH_DB_NAME")
