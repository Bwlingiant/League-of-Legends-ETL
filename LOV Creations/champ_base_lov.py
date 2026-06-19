import os
import json
import psycopg
import constants as con
import sys

print(os.curdir)
# print('Fucking work')
# sys.exit()

# --- Database connection (use env vars or refactor later) ---
conn = psycopg.connect(con.db_connection)


# --- Champion directory ---
DATA_DIR = '/home/bwlingiant/python_projects/League-of-Legends-ETL/LOV Creations/ddragon_champions'

# --- SQL Insert Query ---
INSERT_QUERY = """
INSERT INTO "lollov".champions_info (
    id, key, name, title, blurb
)
VALUES (
    %(id)s, %(key)s, %(name)s, %(title)s, %(blurb)s
)
ON CONFLICT (id) DO UPDATE SET
    key = EXCLUDED.key,
    name = EXCLUDED.name,
    title = EXCLUDED.title,
    blurb = EXCLUDED.blurb
"""

# --- Parse and insert data ---
with conn.cursor() as cur:
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                raw = json.load(f)
                champ_data = list(raw["data"].values())[0]  # Unwrap single champ

                payload = {
                    "id": champ_data["id"],
                    "key": champ_data["key"],
                    "name": champ_data["name"],
                    "title": champ_data["title"],
                    "blurb": champ_data["blurb"]
                }

                cur.execute(INSERT_QUERY, payload)
                print(f"Inserted/Updated: {champ_data['id']}")

print("✅ All champions processed.")
conn.commit()
conn.close()
