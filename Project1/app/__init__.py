import os
from flask import Flask
from dotenv import load_dotenv
from app.db import init_db
from app.routes.users import users_bp

# Load env vars
load_dotenv()

def create_app():
    # Tell Flask where to find templates/static explicitly
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, "templates")
    static_dir = os.path.join(base_dir, "static")

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    app.config['DATABASE_URL'] = os.getenv("DATABASE_URL")

    app.register_blueprint(users_bp)
    init_db()
    return app
