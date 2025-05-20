from flask import Blueprint, render_template, request, redirect, url_for
from app.db import get_db

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def index():
    db = get_db()
    cursor = db.cursor()

    search_query = request.args.get("q", "")
    if search_query:
        cursor.execute(
            """
            SELECT * FROM users 
            WHERE name ILIKE %s OR surname ILIKE %s OR email ILIKE %s OR phone ILIKE %s
            ORDER BY id DESC
            """,
            [f"%{search_query}%"] * 4,
        )
    else:
        cursor.execute("SELECT * FROM users ORDER BY id DESC")

    users = cursor.fetchall()
    cursor.close()
    return render_template("index.html", users=users, search_query=search_query)

