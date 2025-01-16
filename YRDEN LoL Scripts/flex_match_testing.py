import sys
import time
import constants
import psycopg
import yrden_sql_queries
import collect_match_data as lol
from riotwatcher import LolWatcher, ApiError, RiotWatcher

sys.stdout.reconfigure(encoding='utf-8')

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

fiveman_flex_query = '''SELECT GAME_ID FROM "yrden".lol_game_data
                        WHERE RIOT_ID IN ('YDN Rock Coaches', 'Triggerman', 'wyzrdsnvrdie', 'Hypocritus', 'Blue')
                        AND QUEUE_ID IN (440,700)
						AND GAME_ID NOT IN 
                            (select game_id
                            from "yrden".lol_game_data
                            where 1=1
                            -- and riot_id in ('YDN Rock Coaches', 'Triggerman', 'wyzrdsnvrdie', 'Hypocritus', 'Blue')
                            and queue_id in (440, 700)
                            group by game_id
                            having count(game_id) = 10)
                        GROUP BY GAME_ID
                        HAVING COUNT(GAME_ID) = 5;'''
cur.execute(fiveman_flex_query)
game_ids = cur.fetchall()

# for game in game_ids:
#     print(game[0])

def add_player_puuid(account_info):
    insert_query = '''INSERT INTO "yrden".people (riot_puuid, riot_id, riot_key) SELECT %(puuid)s::VARCHAR, %(gameName)s, %(tagLine)s
                WHERE NOT EXISTS (select 1 from "yrden".people WHERE riot_puuid = %(puuid)s);'''
    cur.execute(insert_query, account_info)
    conn.commit()

with conn.cursor() as curs:
    for game in game_ids:
        id_list = []
        try:
            match = lol_watcher.match.by_id(lol_region, game[0])

            
            for id in match['metadata']['participants']:
                id_list.append(id)

            for id in id_list:
                curs.execute(yrden_sql_queries.get_puuids_all)
                raw_puuids = curs.fetchall()
                puuid_list = [raw_puuids[0] for raw_puuids in raw_puuids]
                if id in (puuid_list):
                    continue
                riot_id = riot_watcher.account.by_puuid('AMERICAS', id)
                print(riot_id)
                time.sleep(1)
                add_player_puuid(riot_id)

            for id in id_list:
                test = lol.collect_match_data('NA1', id, game[0], lol_watcher)
                print(test)
                time.sleep(3)
                insert_query = '''INSERT INTO "yrden".lol_game_data (riot_puuid, game_duration, game_id,
                        game_mode, queue_id, game_patch, champion_id, champion_name, lane, teamid, win,
                        kills, deaths, assists, double_kills, triple_kills, quadra_kills,  penta_kills,
                        gold_earned, champion_damage, objective_damage, damage_healed, vision_score,  minions_killed,
                        neutral_monsters_killed, keystone_rune_code, keystone_rune_var1, keystone_rune_var2, keystone_rune_var3,
                        primary_rune_code1, primary_rune_code2, primary_rune_code3, primary_rune1_var1, primary_rune1_var2,
                        primary_rune1_var3, primary_rune2_var1, primary_rune2_var2, primary_rune2_var3, primary_rune3_var1,
                        primary_rune3_var2, primary_rune3_var3, secondary_rune_code1, secondary_rune_code2, secondary_rune1_var1,
                        secondary_rune1_var2, secondary_rune1_var3, secondary_rune2_var1, secondary_rune2_var2, secondary_rune2_var3,
                        largest_critical_strike, nexus_kills, summoner1_id, summoner1_casts, summoner2_id, summoner2_casts, 
                        control_wards_purchased, wards_killed, wards_placed)
                SELECT %(puuid)s::VARCHAR, %(duration)s, %(game_id)s::VARCHAR,
                        %(gameMode)s, %(queueId)s, %(gameVersion)s, %(championId)s, %(championName)s, %(lane)s, %(teamId)s, %(win)s,
                        %(kills)s, %(deaths)s, %(assists)s, %(doublekills)s, %(triplekills)s, %(quadrakills)s, %(pentakills)s,
                        %(gold_earned)s, %(champion_damage)s, %(objective_damage)s, %(damage_healed)s, %(vision_score)s,  %(minions_killed)s,
                        %(neutral_monsters_killed)s, %(keystone_rune)s, %(keystone_rune_var1)s, %(keystone_rune_var2)s, %(keystone_rune_var3)s,
                        %(primary_rune1)s, %(primary_rune2)s, %(primary_rune3)s, %(primary_rune1_var1)s, %(primary_rune1_var2)s,
                        %(primary_rune1_var3)s, %(primary_rune2_var1)s, %(primary_rune2_var2)s, %(primary_rune2_var3)s, %(primary_rune3_var1)s,
                        %(primary_rune3_var2)s, %(primary_rune3_var3)s, %(secondary_rune1)s, %(secondary_rune2)s, %(secondary_rune1_var1)s,
                        %(secondary_rune1_var2)s, %(secondary_rune1_var3)s, %(secondary_rune2_var1)s, %(secondary_rune2_var2)s, %(secondary_rune2_var3)s,
                        %(largestCriticalStrike)s, %(nexusKills)s, %(summoner1_id)s, %(summoner1_casts)s, %(summoner2_id)s, %(summoner2_casts)s, 
                        %(control_wards_purchased)s, %(wardsKilled)s, %(wardsPlaced)s
                        WHERE NOT EXISTS (select 1 from "yrden".lol_game_data WHERE riot_puuid = %(puuid)s AND game_id = %(game_id)s);'''
                curs.execute(insert_query, test)
                conn.commit()
        except ApiError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
            elif err.response.status_code == 404:
                print(err)
            # elif err.response.status_code == 504 or err.response.status_code == 503 or err.response.status_code == 500:
            #     # 504 happens randomly, wait a couple seconds then try again
            #    This is currently commented out as we need to clean this up. There are too many API calls in this try-except. 
            #    Need to find how to differentiate between the different calls so I can ensure that I reach the correct API endpoint.
            #     time.sleep(5)
            else:
                raise

conn.commit()
conn.close()
print('Connection closed')
