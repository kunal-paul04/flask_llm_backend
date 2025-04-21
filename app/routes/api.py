from flask import Blueprint, jsonify
from app import get_db_connection
from psycopg2 import OperationalError
from flask_jwt_extended import jwt_required, get_jwt_identity

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def welcome():
    return jsonify(message="Welcome to the Flask Docker API!")

@api_bp.route('/health_check')
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify(status="healthy")
    except OperationalError:
        return jsonify(status="unhealthy")

@api_bp.route('/secure-data')
@jwt_required()
def secure_data():
    user = get_jwt_identity()
    return jsonify(message=f"Hello, {user}! This is protected data.")
