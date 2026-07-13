def champ_lov(connection, lol_watcher):
    cur = connection.cursor()
    DDRegion = lol_watcher.data_dragon.versions_for_region('na1')['n']
    DDchamps = DDRegion['summoner']
    champs = lol_watcher.data_dragon.champions(DDchamps)
    champ_data = champs['data']
    # pprint.pp(champ_data)
    # print(type(champs))

    for n in champ_data:
        # print(champ_data.keys())
        # print(champ_data[n])
        champ_info = champ_data[n]
        champion_data_dict = {"id": champ_info['id'],
                            "key" : champ_info['key'],
                            "name": champ_info['name'],
                            "title": champ_info['title'],
                            "blurb": champ_info['blurb']
                            }

        # --- SQL Insert Query ---
        INSERT_QUERY = """
        INSERT INTO "lollov".champions_info (
            id, key, name, title, blurb
        )
        VALUES (
            %(id)s, %(key)s, %(name)s, %(title)s, %(blurb)s
        )
        ON CONFLICT (id) DO UPDATE SET
            key = EXCLUDED.key,
            name = EXCLUDED.name,
            title = EXCLUDED.title,
            blurb = EXCLUDED.blurb
        """
        cur.execute(INSERT_QUERY, champion_data_dict)


    print("✅ All champions processed.")
    connection.commit()
    connection.close()
