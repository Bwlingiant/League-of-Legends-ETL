def item_lov(connection, lol_watcher):
    DDRegion = lol_watcher.data_dragon.versions_for_region('na1')['n']
    DDitems = DDRegion['summoner']
    items = lol_watcher.data_dragon.items(DDitems)
    item_data = items['data']
    patch_version = items['version']
    for n in item_data:
        gold = item_data[n]['gold']
        into = item_data[n].get('into')

        tags = {n for n in item_data[n]['tags']}
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
        with connection.cursor() as cur:
            cur.execute(INSERT_QUERY, item_dict)

    connection.commit()
    print('Items processed successfully.')