class InstrumentService:
    def __init__(self, repo):
        self.repo = repo

    def list(self):
        return self.repo.all()

    def create(self, data):
        return self.repo.create(data)

    def delete(self, instrument_id):
        return self.repo.delete(instrument_id)
