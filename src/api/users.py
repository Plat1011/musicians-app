from flask import Blueprint, abort, jsonify, request
from pydantic import ValidationError

from src.repositories.user_repo import UserRepository
from src.schemas.user import UserCreate
from src.services.user_service import UserService

bp = Blueprint("users", __name__, url_prefix="/users")
service = UserService(UserRepository())


@bp.get("")
def list_users():
    return jsonify(service.list_users())


@bp.get("/<int:user_id>")
def get_user(user_id):
    user = service.get_user(user_id)
    if user is None:
        abort(404)
    return jsonify(user)


@bp.post("")
def create_user():
    payload = request.get_json(silent=True) or {}
    try:
        data = UserCreate(**payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    user = service.create_user(data)
    return jsonify(user), 201
