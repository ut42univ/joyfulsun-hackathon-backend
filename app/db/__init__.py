import os

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)
