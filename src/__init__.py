from flask import Flask, jsonify

from src.api import users
from src.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(users.bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "not found"}), 404

    return app
