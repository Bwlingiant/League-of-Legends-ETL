from champ_base_lov import champ_lov
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

champ_lov(conn, API_KEY, lol_watcher=lol_watcher)