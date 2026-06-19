import sys
import time
import json
import psycopg
import constants
import pprint

from riotwatcher import LolWatcher, ApiError, RiotWatcher

API_KEY = constants.API_KEY_SERVICE
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)
lol_region = 'na1'


#Connect to Yrden DB
#Private args are executed and then deleted for safety
db_pass = constants.db_password
db_ip = constants.db_ip
db_connection = f'dbname = yrden user=postgres password={db_pass} host={db_ip}'
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
'''INSERT INTO "lollov".summoner_spells
    (spell_name, spell_id, modes)
    VALUES
    (%(spell_name)s, %(spell_id)s, %(modes)s);'''
INSERT_QUERY = '''
INSERT INTO "lollov".runes
(rune_name, rune_id, rune_key, category, rune_slot)
VALUES
(%(name)s, %(id)s, %(key)s, %(category)s, %(slot)s);
'''

for n, item in flattened_runes.items():
    cur.execute(INSERT_QUERY, item)

conn.commit()
conn.close()
print('Database connection closed.')