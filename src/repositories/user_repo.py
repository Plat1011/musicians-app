class UserRepository:
    def __init__(self):
        self._users = {}
        self._next_id = 1

    def all(self):
        return list(self._users.values())

    def get(self, user_id):
        return self._users.get(user_id)

    def create(self, name, email, age):
        user_id = self._next_id
        self._next_id += 1
        user = {"id": user_id, "name": name, "email": email, "age": age}
        self._users[user_id] = user
        return user
