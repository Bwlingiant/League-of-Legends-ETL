import os
import sys
import time
import datetime
import json
import psycopg
from riotwatcher import LolWatcher, ValWatcher, ApiError, RiotWatcher
import requests
import yrden_sql_queries
import pprint

lol_watcher = LolWatcher(os.environ['API_KEY_SERVICE'])
riot_watcher = RiotWatcher(os.environ['API_KEY_SERVICE'])
db_connection = (
    f"dbname={os.environ['DB']} "
    f"user={os.environ['POSTGRES_USER']} "
    f"password={os.environ['POSTGRES_PASSWORD']} "
    f"host={os.environ['PGHOST']} "
    f"port={os.environ['PGPORT']}"
)
# print(db_connection)

conn = psycopg.connect(db_connection)
cur = conn.cursor()

cur.execute(yrden_sql_queries.get_puuids_yrden)
summoner_ids_list = cur.fetchall()

def commit_champ_mastery(conn, summoner_name):
    with conn.cursor() as curs:

        """cur.execute ('''DROP TABLE
              "yrden".lol_champ_mastery''')
        cur.execute('''CREATE TABLE "yrden".lol_champ_mastery
            (puuid varchar , 
            championId int , 
            championLevel int ,
            championPoints int ,
            championPointsUntilNextLevel int,
            championPointsSinceLastLevel int,
            lastPlayTime timestamp,
            tokensEarned int
            )
            ;
            ''')"""

        for i, riot_puuid in enumerate(summoner_name):
            
            api_url = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{riot_puuid}?api_key={os.environ['API_KEY_SERVICE']}"
            resp = requests.get(api_url)
            vals = resp.json()
            # pprint.pp(vals)
            # break
            new_vals = {}
            for n in range(len(vals)):
                new_vals.update({'puuid' : vals[n]['puuid'],
                                 'championId' : vals[n]['championId'],
                                 'championLevel' : vals[n]['championLevel'],
                                 'championPoints' :  vals[n]['championPoints'],
                                 'championPointsUntilNextLevel' :  vals[n]['championPointsUntilNextLevel'],
                                 'championPointsSinceLastLevel' :  vals[n]['championPointsSinceLastLevel'],
                                 'tokensEarned' :  vals[n]['tokensEarned']
                                })

                curs.execute('''DROP TABLE IF EXISTS "yrden".stage_champ_mastery;''')

                curs.execute('''CREATE TABLE "yrden".stage_champ_mastery
                            (puuid varchar , 
                                        championId int , 
                                        championLevel int ,
                                        championPoints int ,
                                        championPointsUntilNextLevel int,
                                        championPointsSinceLastLevel int,
                                        tokensEarned int
                                        );''')
                #print(new_vals)

                curs.execute('''INSERT INTO "yrden".stage_champ_mastery 
                            (puuid, 
                            championId,
                            championLevel,
                            championPoints,
                            championPointsUntilNextLevel,
                            championPointsSinceLastLevel,
                           tokensEarned
                            )
                                VALUES (%(puuid)s, %(championId)s,
                                %(championLevel)s, %(championPoints)s,
                                %(championPointsUntilNextLevel)s,
                                %(championPointsSinceLastLevel)s, 
                                %(tokensEarned)s);''', new_vals)
                
                curs.execute(
                    '''
                    UPDATE "yrden".LOL_CHAMP_MASTERY 
                    SET CHAMPIONLEVEL = %(championLevel)s,
                    CHAMPIONPOINTS = %(championPoints)s,
                    CHAMPIONPOINTSUNTILNEXTLEVEL = %(championPointsUntilNextLevel)s,
                    CHAMPIONPOINTSSINCELASTLEVEL = %(championPointsSinceLastLevel)s, 
                    TOKENSEARNED = %(tokensEarned)s
                    WHERE PUUID = %(puuid)s AND CHAMPIONID = %(championId)s;
                    ''', new_vals
                )



                curs.execute('''INSERT INTO "yrden".lol_champ_mastery (puuid, 
                            championId,
                            championLevel,
                            championPoints,
                            championPointsUntilNextLevel,
                            championPointsSinceLastLevel,
                            tokensEarned
                            )
                                SELECT DISTINCT cmst.puuid, 
                            cmst.championId,
                            cmst.championLevel,
                            cmst.championPoints,
                            cmst.championPointsUntilNextLevel,
                            cmst.championPointsSinceLastLevel,
                            cmst.tokensEarned
                                FROM "yrden".stage_champ_mastery cmst
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