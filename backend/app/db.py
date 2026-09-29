import os

def get_database_url()->str|None:
    return os.getenv("DATABASE_URL")
