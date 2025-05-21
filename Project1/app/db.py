import psycopg2
import time
from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(current_app.config["DATABASE_URL"])
    return g.db

def init_db(retries=5, delay=2):
    import time
    for i in range(retries):
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    surname TEXT,
                    email TEXT,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            db.commit()
            cursor.close()
            print("✅ Database initialized.")
            return
        except Exception as e:
            print(f"Database not ready, retrying ({i+1}/{retries})...")
            time.sleep(delay)
    raise Exception("❌ Could not connect to the database after multiple retries.")
