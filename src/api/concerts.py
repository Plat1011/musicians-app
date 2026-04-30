from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from src.core.db import get_db
from src.core.security import require_admin, require_auth
from src.repositories.concert_repo import ConcertRepository
from src.schemas.concert import ConcertIn
from src.services.concert_service import ConcertService

bp = Blueprint("concerts", __name__, url_prefix="/api/concerts")


def _service():
    return ConcertService(ConcertRepository(get_db()))


@bp.get("")
@require_auth
def list_concerts():
    return jsonify(_service().list())


@bp.get("/<int:concert_id>")
@require_auth
def get_concert(concert_id):
    concert = _service().get(concert_id)
    if concert is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(concert)


@bp.post("")
@require_admin
def create_concert():
    payload = request.get_json(silent=True) or {}
    try:
        data = ConcertIn(**payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    return jsonify(_service().create(data)), 201


@bp.put("/<int:concert_id>")
@require_admin
def update_concert(concert_id):
    payload = request.get_json(silent=True) or {}
    try:
        data = ConcertIn(**payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    concert = _service().update(concert_id, data)
    if concert is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(concert)


@bp.delete("/<int:concert_id>")
@require_admin
def delete_concert(concert_id):
    if not _service().delete(concert_id):
        return jsonify({"error": "not found"}), 404
    return "", 204
