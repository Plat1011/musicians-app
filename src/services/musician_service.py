class MusicianService:
    def __init__(self, repo):
        self.repo = repo

    def list(self):
        return self.repo.all()

    def get(self, musician_id):
        return self.repo.get(musician_id)

    def create(self, data):
        return self.repo.create(data)

    def update(self, musician_id, data):
        return self.repo.update(musician_id, data)

    def delete(self, musician_id):
        return self.repo.delete(musician_id)
