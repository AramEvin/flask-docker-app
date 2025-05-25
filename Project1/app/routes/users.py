from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db
import re


users_bp = Blueprint("users", __name__)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return phone == "" or phone.isdigit()

@users_bp.route("/", methods=["GET"])
def index():
    db = get_db()
    cursor = db.cursor()

    search_query = request.args.get("q", "")
    sort_by = request.args.get("sort", "date")
    sort_column = {"name": "name", "surname": "surname", "date": "created_at"}.get(sort_by, "created_at")

    if search_query:
        cursor.execute(
            f"""
            SELECT id, name, surname, email, phone, created_at FROM users
            WHERE name ILIKE %s OR surname ILIKE %s OR email ILIKE %s OR phone ILIKE %s
            ORDER BY {sort_column} ASC
            """,
            [f"%{search_query}%"] * 4,
        )
    else:
        cursor.execute(f"SELECT id, name, surname, email, phone, created_at FROM users ORDER BY {sort_column} ASC")

    users = cursor.fetchall()
    cursor.close()
    return render_template("index.html", users=users, search_query=search_query, sort_by=sort_by)

@users_bp.route("/add", methods=["POST"])
def add_user():
    db = get_db()
    cursor = db.cursor()

    name = request.form["name"].strip()
    surname = request.form["surname"].strip()
    email = request.form["email"].strip()
    phone = request.form["phone"].strip()

    errors = []

    if not name:
        errors.append("Name is required.")
    if not surname:
        errors.append("Surname is required.")
    if email and not is_valid_email(email):
        errors.append("Email is invalid.")
    if not is_valid_phone(phone):
        errors.append("Phone must contain digits only.")

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("users.index"))

    cursor.execute(
        "INSERT INTO users (name, surname, email, phone) VALUES (%s, %s, %s, %s)",
        (name, surname, email, phone),
    )
    db.commit()
    cursor.close()
    flash("User added successfully!", "success")
    return redirect(url_for("users.index"))

@users_bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":
        name = request.form["name"].strip()
        surname = request.form["surname"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()

        errors = []
        if not name:
            errors.append("Name is required.")
        if not surname:
            errors.append("Surname is required.")
        if email and not is_valid_email(email):
            errors.append("Email is invalid.")
        if not is_valid_phone(phone):
            errors.append("Phone must contain digits only.")

        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("users.edit_user", user_id=user_id))

        cursor.execute(
            "UPDATE users SET name=%s, surname=%s, email=%s, phone=%s WHERE id=%s",
            (name, surname, email, phone, user_id),
        )
        db.commit()
        cursor.close()
        flash("User updated successfully!", "success")
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
    flash("User deleted!", "success")
    return redirect(url_for("users.index"))

