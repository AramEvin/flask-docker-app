from flask import Blueprint, render_template, request, redirect, url_for
from app.db import get_conn

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            conn.commit()
            cur.close()
            conn.close()
        return redirect(url_for('users.index'))

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY id DESC")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", users=users)

@users_bp.route("/delete/<int:user_id>")
def delete(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('users.index'))

@users_bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit(user_id):
    conn = get_conn()
    cur = conn.cursor()
    if request.method == "POST":
        new_name = request.form.get("name")
        cur.execute("UPDATE users SET name = %s WHERE id = %s", (new_name, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('users.index'))

    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("edit.html", user=user)
