from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from src.core.db import get_db
from src.repositories.auth_repo import AuthRepository
from src.schemas.auth import LoginIn, RegisterIn
from src.services.auth_service import AuthService

bp = Blueprint("auth", __name__, url_prefix="/auth")


def _service():
    return AuthService(AuthRepository(get_db()))


@bp.post("/register")
def register():
    payload = request.get_json(silent=True) or {}
    try:
        data = RegisterIn(**payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    user_id = _service().register(data.username, data.password)
    if user_id is None:
        return jsonify({"error": "username taken"}), 409
    return jsonify({"id": user_id, "username": data.username}), 201


@bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    try:
        data = LoginIn(**payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    token = _service().login(data.username, data.password)
    if token is None:
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"token": token})
