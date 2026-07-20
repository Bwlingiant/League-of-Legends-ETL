from psycopg.types.json import Jsonb
def item_lov(connection, lol_watcher):
    DDRegion = lol_watcher.data_dragon.versions_for_region('na1')['n']
    DDitems = DDRegion['summoner']
    items = lol_watcher.data_dragon.items(DDitems)
    item_data = items['data']
    patch_version = items['version']
    for n in item_data:
        gold = item_data[n]['gold']
        into = Jsonb(item_data[n].get('into'))

        tags = Jsonb(item_data[n]['tags'])
        icon_url = f"https://ddragon.leagueoflegends.com/cdn/{patch_version}/img/item/{item_data[n]['image']['full']}"
        item_dict = {
            "id" : n,
            "name" : item_data[n]['name'],
            "colloq" : item_data[n].get('colloq'),
            "into" : into,
            "gold_base" : gold['base'],
            "gold_sell" : gold['sell'],
            "gold_total" : gold['total'],
            "purchasable" : gold['purchasable'],
            "tags" : tags,
            "maps" : Jsonb(item_data[n]['maps']),
            "stats" : Jsonb(item_data[n]['stats']),
            "patch_version" : patch_version,
            "icon_url" : icon_url
        }
        
        INSERT_QUERY = """
        INSERT INTO "lollov".items (
            id, name, colloq, "into", gold_base, gold_total, gold_sell, purchasable,
            tags, maps, stats, patch_version, icon_url
        )
        VALUES (
        %(id)s, %(name)s, %(colloq)s, %(into)s, %(gold_base)s, %(gold_total)s,
        %(gold_sell)s, %(purchasable)s, %(tags)s, %(maps)s, %(stats)s, %(patch_version)s, %(icon_url)s
        )
        ON CONFLICT (id, patch_version) DO UPDATE SET
            id = EXCLUDED.id,
            name = EXCLUDED.name,
            colloq = EXCLUDED.colloq,
            "into" = EXCLUDED."into",
            gold_base = EXCLUDED.gold_base,
            gold_total = EXCLUDED.gold_total,
            gold_sell = EXCLUDED.gold_sell,
            purchasable = EXCLUDED.purchasable,
            tags = EXCLUDED.tags,
            maps = EXCLUDED.maps,
            stats = EXCLUDED.stats,
            patch_version = EXCLUDED.patch_version,
            icon_url = EXCLUDED.icon_url
            ;
        """
        with connection.cursor() as cur:
            cur.execute(INSERT_QUERY, item_dict)

    connection.commit()
    print('Items processed successfully.')