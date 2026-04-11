from functools import wraps

from flask import current_app, g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

TOKEN_TTL = 86400


def _serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


def make_token(user_id, role):
    return _serializer().dumps({"user_id": user_id, "role": role})


def parse_token(token):
    try:
        return _serializer().loads(token, max_age=TOKEN_TTL)
    except (BadSignature, SignatureExpired):
        return None


def _extract_token():
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        return header[7:]
    return None


def require_auth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        token = _extract_token()
        data = parse_token(token) if token else None
        if data is None:
            return jsonify({"error": "unauthorized"}), 401
        g.current_user = data
        return f(*args, **kwargs)
    return wrapped


def require_admin(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        token = _extract_token()
        data = parse_token(token) if token else None
        if data is None:
            return jsonify({"error": "unauthorized"}), 401
        if data.get("role") != "admin":
            return jsonify({"error": "forbidden"}), 403
        g.current_user = data
        return f(*args, **kwargs)
    return wrapped
