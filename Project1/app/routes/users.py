from flask import Blueprint, render_template, request, redirect, url_for
from app.db import get_db

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def index():
    db = get_db()
    cursor = db.cursor()

    search_query = request.args.get("q", "")
    sort_by = request.args.get("sort", "date")

    sort_column = "name" if sort_by == "name" else "id"

    if search_query:
        cursor.execute(
            f"""SELECT * FROM users 
                WHERE name ILIKE %s OR surname ILIKE %s OR email ILIKE %s OR phone ILIKE %s
                ORDER BY {sort_column} ASC""",
            [f"%{search_query}%"] * 4
        )
    else:
        cursor.execute(f"SELECT * FROM users ORDER BY {sort_column} ASC")

    users = cursor.fetchall()
    cursor.close()
    return render_template("index.html", users=users, search_query=search_query, sort_by=sort_by)

@users_bp.route("/add", methods=["POST"])
def add_user():
    db = get_db()
    cursor = db.cursor()
    name = request.form["name"]
    surname = request.form.get("surname", "")
    email = request.form.get("email", "")
    phone = request.form.get("phone", "")
    cursor.execute("INSERT INTO users (name, surname, email, phone) VALUES (%s, %s, %s, %s)", (name, surname, email, phone))
    db.commit()
    cursor.close()
    return redirect(url_for("users.index"))

@users_bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        phone = request.form["phone"]
        cursor.execute(
            "UPDATE users SET name=%s, surname=%s, email=%s, phone=%s WHERE id=%s",
            (name, surname, email, phone, user_id)
        )
        db.commit()
        cursor.close()
        return redirect(url_for("users.index"))

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return render_template("edit.html", user=user)

@users_bp.route("/delete/<int:user_id>")
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("users.index"))

