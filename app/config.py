# app/config.py
import os

# DATABASE_URL reads the database connection string from environment variables.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/restaurant_db")
