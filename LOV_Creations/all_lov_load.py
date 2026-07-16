from champ_base_lov import champ_lov
from runes_lov import runes
from challenges_lov import challenge_lov
from champ_data_lov import champ_data_lov
from SummonerSpellLOV import summoners_lov
from item_lov import item_lov
import os
import json
import psycopg
import sys
import pprint
from riotwatcher import LolWatcher, ApiError, RiotWatcher

API_KEY = os.environ['API_KEY_SERVICE']
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)
lol_region = 'na1'

db_connection = (
    f"dbname={os.environ['DB']} "
    f"user={os.environ['POSTGRES_USER']} "
    f"password={os.environ['POSTGRES_PASSWORD']} "
    f"host={os.environ['PGHOST']} "
    f"port={os.environ['PGPORT']}"
)
conn = psycopg.connect(db_connection)
DDRegion = lol_watcher.data_dragon.versions_for_region('na1')['n']
DDchamps = DDRegion['summoner']
champs = lol_watcher.data_dragon.items(DDchamps)

if __name__ == "__main__":
    champ_lov(conn, lol_watcher=lol_watcher)
    runes(conn, lol_watcher=lol_watcher)
    challenge_lov(conn, lol_watcher=lol_watcher)
    champ_data_lov(conn, lol_watcher=lol_watcher)
    summoners_lov(conn, lol_watcher=lol_watcher)
    item_lov(conn, lol_watcher=lol_watcher)

conn.close()