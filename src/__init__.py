from flask import Flask, jsonify

from src.api import auth, musicians, users
from src.config import Config
from src.core.db import close_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.teardown_appcontext(close_db)

    app.register_blueprint(users.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(musicians.bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "not found"}), 404

    return app
