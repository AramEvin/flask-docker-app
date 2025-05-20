import os
from flask import Flask
from app.db import init_db
from app.routes.users import users_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev")
    app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")

    with app.app_context():
        init_db()

    app.register_blueprint(users_bp)
    return app
