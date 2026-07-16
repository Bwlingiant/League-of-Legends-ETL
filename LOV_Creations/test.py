import json
import psycopg
import os
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
cur = conn.cursor()



DDRegion = lol_watcher.data_dragon.versions_for_region('na1')['n']
DDitems = DDRegion['summoner']
items = lol_watcher.data_dragon.items(DDitems)
item_data = items['data']
patch_version = items['version']
for n in item_data:
    pprint.pp(item_data[n])
    gold = item_data[n]['gold']
    if item_data[n]['into'] == None:
        into = None
    else:
        into = {item for item in item_data[n]['into']}
    tags = {n for n in item_data[n]['tags']}
    item_dict = {
        "id" : n,
        "name" : item_data[n]['name'],
        "colloq" : item_data[n]['colloq'],
        "into" : into,
        "gold_base" : gold['base'],
        "gold_sell" : gold['sell'],
        "gold_total" : gold['total'],
        "purchasable" : gold['purchasable'],
        "tags" : tags,
        "maps" : item_data[n]['maps'],
        "stats" : item_data[n]['stats'],
        "patch_version" : patch_version
    }
    
    INSERT_QUERY = """
    INSERT INTO "lollov".items (
        id, name, colloq, into, gold_base, gold_total, gold_sell, purchasable,
        tags, maps, stats, patch_version
    )
    VALUES (
    %(id)s, %(name)s, %(colloq)s, %(into)s, %(gold_base)s, %(gold_total)s, 
    %(gold_sell)s, %(purchasable)s, %(tags)s, %(maps)s, %(stats)s, %(patch_version)s
    )
    ON CONFLICT (id, patch_version) DO UPDATE SET
        id = EXCLUDED.id,
        name = EXCLUDED.name,
        colloq = EXCLUDED.colloq,
        into = EXCLUDED.into,
        gold_base = EXCLUDED.gold_base,
        gold_total = EXCLUDED.gold_total,
        gold_sell = EXCLUDED.gold_sell,
        purchasable = EXCLUDED.purchasable,
        tags = EXCLUDED.tags,
        maps = EXCLUDED.maps,
        stats = EXCLUDED.stats,
        patch_version = EXCLUDED.patch_version
        ;
    """

conn.commit()
conn.close()
print('Database connection closed.')