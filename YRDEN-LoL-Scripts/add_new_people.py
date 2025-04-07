
import constants
import psycopg
import yrden_sql_queries
from riotwatcher import LolWatcher, ApiError, RiotWatcher

''' ApiError needs to be used inside of this script to
    ensure a clean run of the script.
     
    I should think about making the SQL queries into variables. '''

API_KEY = constants.API_KEY_SERVICE
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)
lol_region = 'na1'

db_pass = constants.db_password
db_ip = constants.db_ip

db_connection = f'dbname = yrden user=postgres password={db_pass} host={db_ip}'

conn = psycopg.connect(db_connection)

cur = conn.cursor()
if __name__ == '__main__':
    cur.execute('''SELECT riot_id, riot_key FROM "yrden".people WHERE riot_puuid is null;''')
    name_result = cur.fetchall()
    for name in name_result:
        print(name)
        riot_puuid = riot_watcher.account.by_riot_id(game_name=name[0], tag_line=name[1], region='AMERICAS')
        print(riot_puuid['puuid'])
        update_query = f'''UPDATE "yrden".people SET riot_puuid = '{riot_puuid['puuid']}' WHERE riot_id ='{name[0]}';'''
        print(update_query)
        cur.execute(update_query)
        conn.commit()

    cur.execute('''SELECT riot_puuid FROM "yrden".people WHERE summoner_id is null;''')
    puuid_result = cur.fetchall()
    for riot_puuid in puuid_result:
        # break
        summ_id = lol_watcher.summoner.by_puuid('NA1', riot_puuid)
        print(summ_id['id'])
        update_query = f'''UPDATE "yrden".people SET summoner_id = '{summ_id['id']}' WHERE riot_puuid ='{riot_puuid[0]}';'''
        print(update_query)
        cur.execute(update_query)
        conn.commit()