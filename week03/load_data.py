"""Week 3, Friday: load the CSVs in data/ into Postgres.

Start Postgres first:  docker compose -f week03/docker-compose.yml up -d
Install:               pip install "psycopg[binary]"
Run:                   python week03/load_data.py

Done when: running it TWICE leaves the same row counts (idempotent load).
Learn: https://www.psycopg.org/psycopg3/docs/basic/usage.html

Steps:
  1. Connect with psycopg.connect(DATABASE_URL). Print "connected".
  2. Run your schema.sql (create tables if they don't exist).
  3. For each CSV, read rows with csv.DictReader and INSERT them.
     Map CSV columns (camelCase) to your table columns (snake_case).
  4. Make it idempotent: INSERT ... ON CONFLICT (id) DO NOTHING
     (or DO UPDATE SET ... if you want reloads to refresh data).
  5. Print row counts per table at the end.
"""
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://fde:fde@localhost:5432/o2c")


def main():
    raise NotImplementedError


if __name__ == "__main__":
    main()
