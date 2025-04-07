import sys
import time
import datetime
import json
import constants
import psycopg
from riotwatcher import LolWatcher, ValWatcher, ApiError, RiotWatcher
import constants
import requests
import yrden_sql_queries

db_pass = constants.db_password
db_ip = constants.db_ip
lol_watcher = LolWatcher(constants.API_KEY_SERVICE)
riot_watcher = RiotWatcher(constants.API_KEY_SERVICE)
db_connection = f'dbname=yrden user=postgres password={db_pass} host={db_ip}'

conn = psycopg.connect(db_connection)
cur = conn.cursor()

cur.execute(yrden_sql_queries.get_puuids)
summoner_ids_list = cur.fetchall()

def commit_champ_mastery(conn, summoner_name):
    with conn.cursor() as curs:

        """cur.execute ('''DROP TABLE
              "yrden".lol_champ_mastery''')
        cur.execute('''CREATE TABLE "yrden".lol_champ_mastery
            (puuid varchar , 
            summonerId varchar,
            championId int , 
            championLevel int ,
            championPoints int ,
            championPointsUntilNextLevel int,
            championPointsSinceLastLevel int,
            chestGranted boolean,
            lastPlayTime timestamp,
            tokensEarned int
            )
            ;
            ''')"""

        for i, riot_puuid in enumerate(summoner_name):
            
            api_url = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{riot_puuid}?api_key={constants.API_KEY_SERVICE}"
            resp = requests.get(api_url)
            vals = resp.json()
            new_vals = {}
            for n in range(len(vals)):
                new_vals.update({'puuid' : vals[n]['puuid'],
                                'summonerId' : vals[n]['summonerId'],
                                 'championId' : vals[n]['championId'],
                                 'championLevel' : vals[n]['championLevel'],
                                 'championPoints' :  vals[n]['championPoints'],
                                 'championPointsUntilNextLevel' :  vals[n]['championPointsUntilNextLevel'],
                                 'championPointsSinceLastLevel' :  vals[n]['championPointsSinceLastLevel'],
                                 'chestGranted' :  vals[n]['chestGranted'],
                                 'tokensEarned' :  vals[n]['tokensEarned']
                                })

                curs.execute('''DROP TABLE "yrden".stage_champ_mastery;''')

                curs.execute('''CREATE TABLE "yrden".stage_champ_mastery
                            (puuid varchar , 
                                        summonerId varchar,
                                        championId int , 
                                        championLevel int ,
                                        championPoints int ,
                                        championPointsUntilNextLevel int,
                                        championPointsSinceLastLevel int,
                                        chestGranted boolean,
                                        tokensEarned int
                                        );''')
                #print(new_vals)

                curs.execute('''INSERT INTO "yrden".stage_champ_mastery 
                            (puuid, 
                            summonerId,
                            championId,
                            championLevel,
                            championPoints,
                            championPointsUntilNextLevel,
                            championPointsSinceLastLevel,
                            chestGranted,
                           tokensEarned
                            )
                                VALUES (%(puuid)s, %(summonerId)s, %(championId)s,
                                %(championLevel)s, %(championPoints)s,
                                %(championPointsUntilNextLevel)s,
                                %(championPointsSinceLastLevel)s, 
                                %(chestGranted)s,   %(tokensEarned)s);''', new_vals)
                
                curs.execute(
                    '''
                    UPDATE "yrden".LOL_CHAMP_MASTERY 
                    SET CHAMPIONLEVEL = %(championLevel)s,
                    CHAMPIONPOINTS = %(championPoints)s,
                    CHAMPIONPOINTSUNTILNEXTLEVEL = %(championPointsUntilNextLevel)s,
                    CHAMPIONPOINTSSINCELASTLEVEL = %(championPointsSinceLastLevel)s, 
                    CHESTGRANTED = %(chestGranted)s, TOKENSEARNED = %(tokensEarned)s
                    WHERE PUUID = %(puuid)s AND CHAMPIONID = %(championId)s;
                    ''', new_vals
                )



                curs.execute('''INSERT INTO "yrden".lol_champ_mastery (puuid, 
                            summonerId,
                            championId,
                            championLevel,
                            championPoints,
                            championPointsUntilNextLevel,
                            championPointsSinceLastLevel,
                            chestGranted,
                            tokensEarned
                            )
                                SELECT DISTINCT cmst.puuid, 
                            cmst.summonerId,
                            cmst.championId,
                            cmst.championLevel,
                            cmst.championPoints,
                            cmst.championPointsUntilNextLevel,
                            cmst.championPointsSinceLastLevel,
                            cmst.chestGranted,
                            cmst.tokensEarned
                                FROM stage_champ_mastery cmst
                                WHERE NOT EXISTS (SELECT puuid,
                                championId
                                FROM "yrden".lol_champ_mastery cmt
                                WHERE cmst.puuid = cmt.puuid
                                AND cmst.championId = cmt.championId);
                                 ''')
                            
                conn.commit()
            curs.execute('''SELECT RIOT_ID FROM "yrden".PEOPLE WHERE RIOT_PUUID = %s;''', riot_puuid)
            riot_id = curs.fetchall()
            curs.execute('''SELECT DISTINCT CHAMPIONID FROM "yrden".LOL_CHAMP_MASTERY WHERE PUUID = %s;''', riot_puuid)
            print(curs.rowcount, " masteries added for ", riot_id[0])

if __name__ == "__main__":
    commit_champ_mastery(conn, summoner_ids_list)

    conn.close()
    print('The database connection has closed.')