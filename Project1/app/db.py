import time
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

def init_db():
    retries = 5
    for i in range(retries):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Database initialized.")
            return
        except Exception as e:
            print(f"Database connection failed, retrying... ({i+1}/{retries})")
            time.sleep(2)
    raise Exception("Could not connect to the database after several attempts")
