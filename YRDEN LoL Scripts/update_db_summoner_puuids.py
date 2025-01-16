import constants
import psycopg
import yrden_sql_queries
from riotwatcher import LolWatcher, ApiError, RiotWatcher

db_pass = constants.db_password
db_ip = constants.db_ip

db_connection = f'dbname = yrden user=postgres password={db_pass} host={db_ip}'

conn = psycopg.connect(db_connection)

cur = conn.cursor()
def update_db_summoner_puuids(region, riot_watcher):
    with conn.cursor() as curs:
        summoner_puuids = {}
        curs.execute(yrden_sql_queries.missing_riotids)
        id_result = curs.fetchall()
        for riot_id, riot_tag in id_result:
                ids = riot_watcher.account.by_riot_id(region, riot_id, riot_tag)['puuid']
                summoner_puuids.update({'puuid' : ids,
                               'riot_id' : riot_id,
                               'riot_key' : riot_tag})
                curs.execute(yrden_sql_queries.udpate_riotids, summoner_puuids)
                conn.commit()