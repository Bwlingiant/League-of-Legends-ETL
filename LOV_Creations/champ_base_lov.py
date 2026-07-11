import os
import json
import psycopg
import sys
import pprint
from riotwatcher import LolWatcher, ApiError, RiotWatcher

API_KEY = os.environ['API_KEY_SERVICE']
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)
lol_region = 'na1'

db_connection = (
    f"dbname={os.environ['DB']} "
    f"user={os.environ['POSTGRES_USER']} "
    f"password={os.environ['POSTGRES_PASSWORD']} "
    f"host={os.environ['PGHOST']} "
    f"port={os.environ['PGPORT']}"
)
conn = psycopg.connect(db_connection)
cur = conn.cursor()

DDRegion = lol_watcher.data_dragon.versions_for_region('na1')['n']
DDchamps = DDRegion['summoner']
champs = lol_watcher.data_dragon.champions(DDchamps)
champ_data = champs['data']
# pprint.pp(champ_data)
# print(type(champs))

for n in champ_data:
    # print(champ_data.keys())
    # print(champ_data[n])
    champ_info = champ_data[n]
    champion_data_dict = {"id": champ_info['id'],
                          "key" : champ_info['key'],
                          "name": champ_info['name'],
                          "title": champ_info['title'],
                          "blurb": champ_info['blurb']
                          }

    # --- SQL Insert Query ---
    INSERT_QUERY = """
    INSERT INTO "lollov".lol_champions_info (
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
    cur.execute(INSERT_QUERY, champion_data_dict)


print("✅ All champions processed.")
conn.commit()
conn.close()
