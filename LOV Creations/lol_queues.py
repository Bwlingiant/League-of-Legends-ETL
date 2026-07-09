import json
import psycopg
import os
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
print('Database connection opened.')


with open('/Riot API/queues.json') as file:
    data = json.load(file)
    for n in data:
        cur.execute('''INSERT INTO "lollov".lol_queues (queueId, map, description, notes) VALUES (%(queueId)s,%(map)s,%(description)s, %(notes)s);''', n)

conn.commit()
conn.close()
print('Database connection closed.')