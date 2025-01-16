import json
import psycopg
import constants
from riotwatcher import LolWatcher, ApiError, RiotWatcher

API_KEY = constants.API_KEY_SERVICE
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)
lol_region = 'na1'
db_pass = constants.db_password
db_ip = constants.db_ip

db_connection = f'dbname=yrden user=postgres password={db_pass} host={db_ip}'

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