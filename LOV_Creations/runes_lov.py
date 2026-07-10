import sys
import os
import time
import json
import psycopg
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
DDrunes = DDRegion['summoner']
# print(DDrunes[0][0])
runes = lol_watcher.data_dragon.runes_reforged(DDrunes)
rune_list = runes

                                 
flattened_runes = {}

for style in rune_list:
    category = style.get("name", "Unknown")
    # pprint.pp(category)
    for slot_index, slot in enumerate(style.get("slots", []), start=1):
        for rune in slot.get("runes", []):
            rune_id = rune["id"]
            flattened_runes[rune_id] = {
                **rune,
                "category": category,
                "slot": slot_index
            }

# pprint.pp(flattened_runes)

INSERT_QUERY = '''
INSERT INTO "lollov".runes
(rune_name, rune_id, rune_key, category, rune_slot)
VALUES
(%(name)s, %(id)s, %(key)s, %(category)s, %(slot)s)
ON CONFLICT (rune_id) DO NOTHING;
'''

for n, item in flattened_runes.items():
    cur.execute(INSERT_QUERY, item)

conn.commit()
conn.close()
print('Database connection closed.')