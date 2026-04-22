from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from src.core.db import get_db
from src.core.security import require_admin, require_auth
from src.repositories.instrument_repo import InstrumentRepository
from src.schemas.instrument import InstrumentIn
from src.services.instrument_service import InstrumentService

bp = Blueprint("instruments", __name__, url_prefix="/instruments")


def _service():
    return InstrumentService(InstrumentRepository(get_db()))


@bp.get("")
@require_auth
def list_instruments():
    return jsonify(_service().list())


@bp.post("")
@require_admin
def create_instrument():
    payload = request.get_json(silent=True) or {}
    try:
        data = InstrumentIn(**payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    return jsonify(_service().create(data)), 201


@bp.delete("/<int:instrument_id>")
@require_admin
def delete_instrument(instrument_id):
    if not _service().delete(instrument_id):
        return jsonify({"error": "not found"}), 404
    return "", 204
