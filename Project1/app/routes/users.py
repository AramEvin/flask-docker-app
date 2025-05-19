from flask import Blueprint, render_template, request, redirect, url_for
from app.db import get_db, init_db

users_bp = Blueprint("users", __name__)

@users_bp.route("/")
def index():
    init_db()  # ✅ ensure DB is initialized inside context
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return render_template("index.html", users=users)

@users_bp.route("/create", methods=["POST"])
def create_user():
    name = request.form["name"]
    email = request.form["email"]
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    db.commit()
    cursor.close()
    return redirect(url_for("users.index"))

@users_bp.route("/delete/<int:user_id>")
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("users.index"))
