class ConcertRepository:
    def __init__(self, conn):
        self.conn = conn

    def all(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, concert_date, venue, city FROM concerts ORDER BY concert_date DESC"
            )
            return [self._row(r) for r in cur.fetchall()]

    def get(self, concert_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, concert_date, venue, city FROM concerts WHERE id = %s",
                (concert_id,),
            )
            row = cur.fetchone()
        return self._row(row) if row else None

    def create(self, data):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO concerts (title, concert_date, venue, city) "
                "VALUES (%s, %s, %s, %s) RETURNING id, title, concert_date, venue, city",
                (data.title, data.concert_date, data.venue, data.city),
            )
            row = cur.fetchone()
        self.conn.commit()
        return self._row(row)

    def update(self, concert_id, data):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE concerts SET title = %s, concert_date = %s, venue = %s, city = %s "
                "WHERE id = %s RETURNING id, title, concert_date, venue, city",
                (data.title, data.concert_date, data.venue, data.city, concert_id),
            )
            row = cur.fetchone()
        self.conn.commit()
        return self._row(row) if row else None

    def delete(self, concert_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM concerts WHERE id = %s", (concert_id,))
            deleted = cur.rowcount
        self.conn.commit()
        return deleted > 0

    @staticmethod
    def _row(row):
        return {
            "id": row[0],
            "title": row[1],
            "concert_date": row[2].isoformat() if row[2] else None,
            "venue": row[3],
            "city": row[4],
        }
