# tft_testing.py
'''
This script will currently not run completely due to the lack of permissions for the TFT endpoints.
This will be kept as a reference for later use when I get the permissions for TFT's API.
'''

import constants
import psycopg
from riotwatcher import TftWatcher, ApiError, RiotWatcher

API_KEY = constants.API_KEY_SERVICE
tft_watcher = TftWatcher(API_KEY)
print(tft_watcher)

db_pass = constants.db_password
db_ip = constants.db_ip
db_connection = f'dbname = yrden user=postgres password={db_pass} host={db_ip}'

conn = psycopg.connect(db_connection)
cur = conn.cursor()
print('Connection Established')

cur.execute('''SELECT riot_puuid FROM "yrden".people where riot_id = 'Bwlingiant';''')
riot_id = cur.fetchall()
riot_puuid = riot_id[0][0]
print(riot_puuid)
# print(riot_puuid)

tft_watcher.match.by_puuid('AMERICAS',riot_puuid, start=0, count=10)

conn.close()
print("Connection has closed.")