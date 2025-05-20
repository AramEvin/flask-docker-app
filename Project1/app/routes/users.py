from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

users_bp = Blueprint("users", __name__)

@users_bp.route("/")
def index():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template("index.html", users=users)

@users_bp.route('/add', methods=['POST'])
def add_user():
    db = get_db()
    cursor = db.cursor()
    name = request.form['name']
    surname = request.form.get('surname')
    email = request.form.get('email')
    phone = request.form.get('phone')

    cursor.execute(
        "INSERT INTO users (name, surname, email, phone) VALUES (%s, %s, %s, %s)",
        (name, surname, email, phone)
    )
    db.commit()
    cursor.close()
    return redirect(url_for('users.index'))

@users_bp.route("/create", methods=["POST"])
def create_user():
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO users (name, surname, email, phone) VALUES (%s, %s, %s, %s)",
        (request.form["name"], request.form["surname"], request.form["email"], request.form["phone"])
    )
    db.commit()
    cur.close()
    flash("User created.")
    return redirect(url_for("users.index"))

@users_bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        cur.execute(
            "UPDATE users SET name=%s, surname=%s, email=%s, phone=%s WHERE id=%s",
            (request.form["name"], request.form["surname"], request.form["email"], request.form["phone"], user_id)
        )
        db.commit()
        cur.close()
        flash("User updated.")
        return redirect(url_for("users.index"))

    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    return render_template("edit.html", user=user)

@users_bp.route("/delete/<int:user_id>")
def delete_user(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    cur.close()
    flash("User deleted.")
    return redirect(url_for("users.index"))

