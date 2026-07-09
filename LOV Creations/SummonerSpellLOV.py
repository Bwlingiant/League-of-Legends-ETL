import sys
import os
import time
import json
import psycopg
import constants

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
DDsummoner = DDRegion['summoner']
summoners = lol_watcher.data_dragon.summoner_spells(DDsummoner)['data']
summoner_dict = {}
cur.execute(''' DROP TABLE "lollov".summoner_spells ''')
cur.execute(''' CREATE TABLE "lollov".summoner_spells
(
spell_name varchar,
spell_id int,
modes varchar
);''')
for n in summoners:
    summoner_dict.update({'spell_name' : summoners[n]['name'],
                            'spell_id' : summoners[n]['key'],
                            'modes' : summoners[n]['modes']})
    cur.execute('''INSERT INTO "lollov".summoner_spells
    (spell_name, spell_id, modes)
    VALUES
    (%(spell_name)s, %(spell_id)s, %(modes)s);''', summoner_dict)
    print(f"{n} has been added to the LOV.")
conn.commit()
conn.close()
# print('Database connection closed.')

    