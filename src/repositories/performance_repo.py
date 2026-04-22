class PerformanceRepository:
    def __init__(self, conn):
        self.conn = conn

    def all(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT p.id, m.id, m.name, c.id, c.title, c.concert_date, "
                "i.id, i.name, p.fee "
                "FROM performances p "
                "JOIN musicians m ON m.id = p.musician_id "
                "JOIN concerts c ON c.id = p.concert_id "
                "LEFT JOIN instruments i ON i.id = p.instrument_id "
                "ORDER BY c.concert_date DESC, p.id"
            )
            return [self._row(r) for r in cur.fetchall()]

    def add_via_procedure(self, data):
        with self.conn.cursor() as cur:
            cur.execute(
                "CALL sp_add_performance(%s, %s, %s, %s)",
                (data.musician_id, data.concert_id, data.instrument_id, data.fee),
            )
        self.conn.commit()

    def delete(self, performance_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM performances WHERE id = %s", (performance_id,))
            deleted = cur.rowcount
        self.conn.commit()
        return deleted > 0

    @staticmethod
    def _row(row):
        return {
            "id": row[0],
            "musician_id": row[1],
            "musician_name": row[2],
            "concert_id": row[3],
            "concert_title": row[4],
            "concert_date": row[5].isoformat() if row[5] else None,
            "instrument_id": row[6],
            "instrument_name": row[7],
            "fee": float(row[8]) if row[8] is not None else None,
        }
