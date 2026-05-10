from werkzeug.security import check_password_hash, generate_password_hash

from src.core.security import make_token


class AuthService:
    def __init__(self, repo):
        self.repo = repo

    def register(self, username, password):
        if self.repo.get_by_username(username) is not None:
            return None
        return self.repo.create(username, generate_password_hash(password))

    def login(self, username, password):
        user = self.repo.get_by_username(username)
        if user is None:
            return None
        if not check_password_hash(user["password_hash"], password):
            return None
        return {
            "token": make_token(user["id"], user["role"]),
            "user": {"id": user["id"], "username": user["username"], "role": user["role"]},
        }
