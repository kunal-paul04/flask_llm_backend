import os
import psycopg2
import logging
from flask import Flask, request
from flask_cors import CORS
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['DB_CONFIG'] = {
        "host": os.getenv("POSTGRES_HOST"),
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "port": os.getenv("POSTGRES_PORT")
    }

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret")

    # Extensions
    CORS(app, resources={r"/*": {"origins": "*"}})
    is_production = os.environ.get("FLASK_ENV") == "production"
    Talisman(app, force_https=is_production)
    JWTManager(app)
    Limiter(get_remote_address, app=app, default_limits=["100 per minute"])
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB limit

    # Logging
    logging.basicConfig(level=logging.INFO)

    @app.before_request
    def log_request_info():
        logging.info(f"{request.remote_addr} - {request.method} {request.path}")

    @app.after_request
    def remove_server_header(response):
        response.headers["Server"] = "Secure-API"
        return response

    from app.routes.api import api_bp
    from app.auth import auth_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    return app

def get_db_connection():
    config = {
        "host": os.getenv("POSTGRES_HOST"),
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "port": os.getenv("POSTGRES_PORT")
    }
    return psycopg2.connect(**config)
