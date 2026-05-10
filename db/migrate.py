import os
import sys

import psycopg2

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config


def run():
    conn = psycopg2.connect(Config.DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS _migrations ("
        "name VARCHAR(255) PRIMARY KEY, "
        "applied_at TIMESTAMP NOT NULL DEFAULT NOW())"
    )

    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations")
    files = sorted(f for f in os.listdir(folder) if f.endswith(".sql"))

    for name in files:
        cur.execute("SELECT 1 FROM _migrations WHERE name = %s", (name,))
        if cur.fetchone():
            print(f"skip {name}")
            continue
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            sql = f.read()
        cur.execute(sql)
        cur.execute("INSERT INTO _migrations (name) VALUES (%s)", (name,))
        print(f"applied {name}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    run()
