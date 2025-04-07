import constants
import psycopg
import yrden_sql_queries
from datetime import datetime

from riotwatcher import LolWatcher, ApiError, RiotWatcher

'''
API Error needs to be used in this to catch important errors during API calls.
'''

API_KEY = constants.API_KEY_SERVICE
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)
lol_region = 'na1'

db_pass = constants.db_password
db_ip = constants.db_ip

db_connection = f'dbname=yrden user=postgres password={db_pass} host={db_ip}'

conn = psycopg.connect(db_connection)
cur = conn.cursor()

# cur.execute('''SELECT DISTINCT riot_id, riot_puuid FROM "STONEHILL".people WHERE riot_id is NOT NULL AND riot_puuid is NOT NULL;''')
# result = cur.fetchall()

# for riot_id, riot_puuid in result:
#     print(riot_puuid,)
# cur.execute('''SELECT DISTINCT GAME_ID FROM "STONEHILL".LOL_GAME_DATA WHERE WIN IS NULL AND PUUID = %s;''' (riot_puuid,))

# print(challenges['totalPoints'])
# Contains basic informaation on total challenges points

# print(challenges['categoryPoints'])
# Contains basic informaiton on category points.

# print(list(enumerate(challenges['challenges'])))
# challenges['challenges'][0] has a dict structured like the following: {level, current, max, percentile} We also want to have information regarding the splits between current and next level.
# challenges['challenges'][n]
# challenges['challenges'][1+n] will always have a dictionary of length 5 or 7. Use this to create some if statement.



#acheievedTime is a UNIX timestamp
def update_lol_challenges(conn, region, riot_puuids):
    with conn.cursor() as curs:
        cur.execute('DROP TABLE "yrden".STAGE_LOL_CHALLENGES;')
        cur.execute('''CREATE TABLE
                    "yrden".STAGE_LOL_CHALLENGES
                    (
                        puuid varchar,
                        challenge_id integer,
                        percentile real,
                        pos int,
                        players_in_level int,
                        challenge_level varchar,
                        value real,
                        achieved_time timestamp
                    )
                    ;''')
        for riot_puuid in riot_puuids:
            
            challenges = lol_watcher.challenges.by_puuid(region, riot_puuid)
            challenge_trees_dict = {}
            for index, dict in enumerate(challenges['challenges']):
                achieved_time_milliseconds = dict.get('achievedTime', 0)
                challenge_time = datetime.utcfromtimestamp(achieved_time_milliseconds/1000.0)
                if len(dict) == 7:
                    challenge_trees_dict.update({
                        'puuid' : riot_puuid,
                        'challenge_id' : dict['challengeId'],
                        'percentile' : dict['percentile'],
                        'pos' : dict['position'],
                        'players_in_level' : dict['playersInLevel'],
                        'challenge_level' : dict['level'],
                        'value' : dict['value'],
                        'achieved_time' : challenge_time
                    })
                    seven_query = '''
                        INSERT INTO "yrden".STAGE_LOL_CHALLENGES
                        (puuid, challenge_id, percentile, pos, players_in_level, challenge_level, value, achieved_time)
                        VALUES
                        (%(puuid)s, %(challenge_id)s, %(percentile)s, %(pos)s, 
                        %(players_in_level)s, %(challenge_level)s, %(value)s, %(achieved_time)s);
                                '''
                    curs.execute(seven_query, challenge_trees_dict)
                else:
                    challenge_trees_dict.update({
                        'puuid' : riot_puuid,
                        'challenge_id' : dict['challengeId'],
                        'percentile' : dict['percentile'],
                        'challenge_level' : dict['level'],
                        'value' : dict['value'],
                        'achieved_time' : challenge_time
                    })
                    five_query = '''
                        INSERT INTO "yrden".STAGE_LOL_CHALLENGES
                        (puuid, challenge_id, percentile, challenge_level, value, achieved_time)
                        VALUES
                        (%(puuid)s, %(challenge_id)s, %(percentile)s, %(challenge_level)s, %(value)s, %(achieved_time)s);
                        '''
                    curs.execute(five_query, challenge_trees_dict)

        curs.execute(
            '''INSERT INTO "yrden".LOL_CHALLENGES 
                (puuid, challenge_id, percentile, players_in_level, challenge_level, value, achieved_time)
                    SELECT
                        sct.puuid,
                        sct.challenge_id,
                        sct.percentile,
                        sct.players_in_level,
                        sct.challenge_level,
                        sct.value,
                        sct.achieved_time
                    FROM
                        "yrden".STAGE_LOL_CHALLENGES sct
                    WHERE NOT EXISTS
                    (SELECT LC.PUUID
                    FROM "yrden".LOL_CHALLENGES LC
                    WHERE LC.PUUID = SCT.PUUID);'''
                    )

        curs.execute(
            '''
            UPDATE "yrden".LOL_CHALLENGES
            SET CHALLENGE_LEVEL = SCT.CHALLENGE_LEVEL,
            ACHIEVED_TIME = SCT.ACHIEVED_TIME,
            PERCENTILE = SCT.PERCENTILE,
            VALUE = SCT.VALUE
            FROM "yrden".STAGE_LOL_CHALLENGES SCT
            WHERE "yrden".LOL_CHALLENGES.CHALLENGE_ID = SCT.CHALLENGE_ID
            AND "yrden".LOL_CHALLENGES.PUUID = SCT.PUUID
            '''
            )

        curs.execute
        ('''
        UPDATE "yrden".LOL_CHALLENGES
        SET TIER = SCT.NAME
         ''')

    conn.commit()



if __name__ == '__main__':

    cur.execute(yrden_sql_queries.get_current_riot_puuids_yrden)
    puuids_list = cur.fetchall()
    puuids = [n[0] for n in puuids_list]
    update_lol_challenges(conn, lol_region, puuids)
    conn.close()
    print('The database connection has closed')