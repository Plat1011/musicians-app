class AuthRepository:
    def __init__(self, conn):
        self.conn = conn

    def create(self, username, password_hash, role="user"):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) "
                "VALUES (%s, %s, %s) RETURNING id",
                (username, password_hash, role),
            )
            user_id = cur.fetchone()[0]
        self.conn.commit()
        return user_id

    def get_by_username(self, username):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, password_hash, role FROM users WHERE username = %s",
                (username,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {"id": row[0], "username": row[1], "password_hash": row[2], "role": row[3]}
