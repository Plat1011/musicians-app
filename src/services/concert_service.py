class ConcertService:
    def __init__(self, repo):
        self.repo = repo

    def list(self):
        return self.repo.all()

    def get(self, concert_id):
        return self.repo.get(concert_id)

    def create(self, data):
        return self.repo.create(data)

    def update(self, concert_id, data):
        return self.repo.update(concert_id, data)

    def delete(self, concert_id):
        return self.repo.delete(concert_id)
