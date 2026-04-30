from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from src.core.db import get_db
from src.core.security import require_admin, require_auth
from src.repositories.performance_repo import PerformanceRepository
from src.schemas.performance import PerformanceIn
from src.services.performance_service import PerformanceService

bp = Blueprint("performances", __name__, url_prefix="/api/performances")


def _service():
    return PerformanceService(PerformanceRepository(get_db()))


@bp.get("")
@require_auth
def list_performances():
    return jsonify(_service().list())


@bp.post("")
@require_admin
def add_performance():
    payload = request.get_json(silent=True) or {}
    try:
        data = PerformanceIn(**payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    ok, error = _service().add(data)
    if not ok:
        return jsonify({"error": error}), 400
    return "", 201


@bp.delete("/<int:performance_id>")
@require_admin
def delete_performance(performance_id):
    if not _service().delete(performance_id):
        return jsonify({"error": "not found"}), 404
    return "", 204
