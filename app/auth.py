from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username == "admin" and password == "password":
        token = create_access_token(identity=username)
        return jsonify(access_token=token)

    return jsonify(msg="Bad username or password"), 401
