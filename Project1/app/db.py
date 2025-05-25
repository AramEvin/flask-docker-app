import psycopg2
import os
import time

def init_db():
    for i in range(5):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host='db',
                port='5432'
            )
            conn.close()
            print("✅ Database connected!")
            return
        except Exception as e:
            print(f"Database not ready, retrying ({i+1}/5)... Error: {e}")
            time.sleep(2)
    raise Exception("❌ Could not connect to the database after multiple retries.")

def get_db():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="db",
        port=5432
    )
    return conn