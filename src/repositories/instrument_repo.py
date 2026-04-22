class InstrumentRepository:
    def __init__(self, conn):
        self.conn = conn

    def all(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name, kind FROM instruments ORDER BY name")
            return [{"id": r[0], "name": r[1], "kind": r[2]} for r in cur.fetchall()]

    def create(self, data):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO instruments (name, kind) VALUES (%s, %s) "
                "RETURNING id, name, kind",
                (data.name, data.kind),
            )
            row = cur.fetchone()
        self.conn.commit()
        return {"id": row[0], "name": row[1], "kind": row[2]}

    def delete(self, instrument_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM instruments WHERE id = %s", (instrument_id,))
            deleted = cur.rowcount
        self.conn.commit()
        return deleted > 0
