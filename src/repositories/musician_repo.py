class MusicianRepository:
    def __init__(self, conn):
        self.conn = conn

    def all(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, country, birth_year, bio FROM musicians ORDER BY id"
            )
            return [self._row(r) for r in cur.fetchall()]

    def get(self, musician_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, country, birth_year, bio FROM musicians WHERE id = %s",
                (musician_id,),
            )
            row = cur.fetchone()
        return self._row(row) if row else None

    def create(self, data):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO musicians (name, country, birth_year, bio) "
                "VALUES (%s, %s, %s, %s) RETURNING id, name, country, birth_year, bio",
                (data.name, data.country, data.birth_year, data.bio),
            )
            row = cur.fetchone()
        self.conn.commit()
        return self._row(row)

    def update(self, musician_id, data):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE musicians SET name = %s, country = %s, birth_year = %s, bio = %s "
                "WHERE id = %s RETURNING id, name, country, birth_year, bio",
                (data.name, data.country, data.birth_year, data.bio, musician_id),
            )
            row = cur.fetchone()
        self.conn.commit()
        return self._row(row) if row else None

    def delete(self, musician_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM musicians WHERE id = %s", (musician_id,))
            deleted = cur.rowcount
        self.conn.commit()
        return deleted > 0

    @staticmethod
    def _row(row):
        return {
            "id": row[0],
            "name": row[1],
            "country": row[2],
            "birth_year": row[3],
            "bio": row[4],
        }
