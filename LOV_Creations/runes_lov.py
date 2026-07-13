def runes(connection, lol_watcher):
    cur = connection.cursor()
    DDRegion = lol_watcher.data_dragon.versions_for_region('na1')['n']
    DDrunes = DDRegion['summoner']
    runes = lol_watcher.data_dragon.runes_reforged(DDrunes)
    rune_list = runes
                                 
    flattened_runes = {}

    for style in rune_list:
        category = style.get("name", "Unknown")
        # pprint.pp(category)
        for slot_index, slot in enumerate(style.get("slots", []), start=1):
            for rune in slot.get("runes", []):
                rune_id = rune["id"]
                flattened_runes[rune_id] = {
                    **rune,
                    "category": category,
                    "slot": slot_index
                }

    # pprint.pp(flattened_runes)

    INSERT_QUERY = '''
    INSERT INTO "lollov".runes
    (rune_name, rune_id, rune_key, category, rune_slot)
    VALUES
    (%(name)s, %(id)s, %(key)s, %(category)s, %(slot)s)
    ON CONFLICT (rune_id) DO NOTHING;
    '''

    for n, item in flattened_runes.items():
        cur.execute(INSERT_QUERY, item)

    print("All runes processed.")

    connection.commit()