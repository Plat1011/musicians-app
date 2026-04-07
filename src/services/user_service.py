class UserService:
    def __init__(self, repo):
        self.repo = repo

    def list_users(self):
        return self.repo.all()

    def get_user(self, user_id):
        return self.repo.get(user_id)

    def create_user(self, data):
        return self.repo.create(data.name, data.email, data.age)
