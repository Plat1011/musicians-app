from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from src.core.db import get_db
from src.core.security import require_admin, require_auth
from src.repositories.musician_repo import MusicianRepository
from src.schemas.musician import MusicianIn
from src.services.musician_service import MusicianService

bp = Blueprint("musicians", __name__, url_prefix="/api/musicians")


def _service():
    return MusicianService(MusicianRepository(get_db()))


@bp.get("")
@require_auth
def list_musicians():
    return jsonify(_service().list())


@bp.get("/<int:musician_id>")
@require_auth
def get_musician(musician_id):
    musician = _service().get(musician_id)
    if musician is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(musician)


@bp.post("")
@require_admin
def create_musician():
    payload = request.get_json(silent=True) or {}
    try:
        data = MusicianIn(**payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    return jsonify(_service().create(data)), 201


@bp.put("/<int:musician_id>")
@require_admin
def update_musician(musician_id):
    payload = request.get_json(silent=True) or {}
    try:
        data = MusicianIn(**payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    musician = _service().update(musician_id, data)
    if musician is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(musician)


@bp.delete("/<int:musician_id>")
@require_admin
def delete_musician(musician_id):
    if not _service().delete(musician_id):
        return jsonify({"error": "not found"}), 404
    return "", 204
