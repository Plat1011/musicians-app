import psycopg2


class PerformanceService:
    def __init__(self, repo):
        self.repo = repo

    def list(self):
        return self.repo.all()

    def add(self, data):
        try:
            self.repo.add_via_procedure(data)
        except psycopg2.errors.RaiseException as e:
            return None, str(e).strip()
        return True, None

    def delete(self, performance_id):
        return self.repo.delete(performance_id)
