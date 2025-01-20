import time
import constants
import psycopg
import yrden_sql_queries
import update_people
import collect_match_data as lol
from riotwatcher import LolWatcher, RiotWatcher

API_KEY = constants.API_KEY_SERVICE
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)
lol_region = 'na1'

db_pass = constants.db_password
db_ip = constants.db_ip

db_connection = f'dbname = yrden user=postgres password={db_pass} host={db_ip}'

conn = psycopg.connect(db_connection)

cur = conn.cursor()
print('Connection Established')

start_time = time.time()

if __name__ == '__main__':
    # This will be used when new summoners are added to the database. Otherwise it is not needed.
    
    # update_people.update_db_summoner_puuids(lol_region, riot_watcher)
    # update_people.update_summoner_ids(lol_region, lol_watcher)

    #Create Staging Game Table
    cur.execute(yrden_sql_queries.drop_gamedata_staging)
    cur.execute(yrden_sql_queries.create_gamedata_staging)
    # conn.commit()

    cur.execute('''select distinct RIOT_ID, RIOT_PUUID FROM "yrden".people WHERE RIOT_ID is NOT NULL AND "YRDEN_FLAG" = True ORDER BY RIOT_ID; ''')
    # cur.execute('''select distinct RIOT_ID, RIOT_PUUID FROM "yrden".people WHERE RIOT_ID = 'Advil Honeyfruit'; ''')
    result = cur.fetchall()
    print(f"We have started committing games.")
    lol.commit_new_games(conn, result, lol_region, lol_watcher)


    cur.execute('''SELECT riot_puuid FROM "yrden".people WHERE riot_puuid is NOT NULL AND "YRDEN_FLAG" = True ORDER BY RIOT_ID;''')
    # cur.execute('''SELECT riot_puuid FROM "yrden".people WHERE riot_id = 'Advil Honeyfruit'; ''')
    account_ids_sql = cur.fetchall()
    account_results = [account_ids_sql[0] for account_ids_sql in account_ids_sql]

    account_dict = {}
    for name in account_results:
        account_id = lol_watcher.summoner.by_puuid(lol_region, name)['puuid']
        account_dict.update({'puuid' : account_id})
        lol.update_lol_game_data(conn, account_dict, lol_watcher)

    cur.execute('''DELETE FROM "yrden".lol_game_data WHERE WIN IS NULL;''')
    conn.commit()
    conn.close()
    print(f"Database connection has been closed.")

    end_time = time.time()

    execution_time = (end_time - start_time)/60
    print(f"Execution time: {execution_time} minutes")