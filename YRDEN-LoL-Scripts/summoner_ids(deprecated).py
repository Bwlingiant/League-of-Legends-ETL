import json
import constants
import psycopg
import yrden_sql_queries
from riotwatcher import LolWatcher, ValWatcher, ApiError, RiotWatcher

API_KEY = constants.API_KEY_SERVICE
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)
lol_region = 'na1'

db_pass = constants.db_password
db_ip = constants.db_ip

db_connection = f'dbname = yrden user=postgres password={db_pass} host={db_ip}'

conn = psycopg.connect(db_connection)

cur = conn.cursor()

cur.execute('''SELECT RIOT_PUUID FROM "yrden".people where RIOT_PUUID is not null''')
result = cur.fetchall()
# print(result[0][0])

summoner_id = lol_watcher.summoner.by_puuid('NA1',result[0][0])
print(summoner_id['id'])

cur.execute('''SELECT riot_puuid FROM "yrden".people WHERE summoner_id is null;''')
puuid_result = cur.fetchall()
for riot_puuid in puuid_result:
    summ_id = lol_watcher.summoner.by_puuid('NA1', riot_puuid)
    print(summ_id['id'])
    update_query = f'''UPDATE "yrden".people SET summoner_id = '{summ_id['id']}' WHERE riot_puuid ='{riot_puuid[0]}';'''
    print(update_query)
    cur.execute(update_query)
    conn.commit()

conn.close()
print(f"The database connection has closed.")