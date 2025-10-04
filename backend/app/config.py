# backend/app/config.py
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SQLite database path
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Secret key for JWT
SECRET_KEY = "your_secret_key"

# Debug mode
DEBUG = True
