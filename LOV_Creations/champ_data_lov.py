def champ_data_lov(connection, lol_watcher):
    DDRegion = lol_watcher.data_dragon.versions_for_region('na1')['n']
    DDchamps = DDRegion['summoner']
    champ_data = lol_watcher.data_dragon.champions(DDchamps)['data']
    for champion in champ_data:
        champ_base = champ_data[champion]
        champ_info = champ_base['info']
        champ_stats = champ_base['stats']
        champion_data_dict = {
            "key" : champ_base['key'],
            "info_attack" : champ_info['attack'],
            "info_defense" : champ_info['defense'],
            "info_magic" : champ_info['magic'],
            "info_difficulty": champ_info['difficulty'],
            "tags" : champ_base['tags'],
            "partype" : champ_base['partype'],
            "hp": champ_stats['hp'],
            "hpperlevel": champ_stats['hpperlevel'],
            "mp": champ_stats['mp'],
            "mpperlevel": champ_stats['mpperlevel'],
            "movespeed": champ_stats['movespeed'],
            "armor": champ_stats['armor'],
            "armorperlevel": champ_stats['armorperlevel'],
            "spellblock": champ_stats['spellblock'],
            "spellblockperlevel": champ_stats['spellblockperlevel'],
            "attackrange": champ_stats['attackrange'],
            "hpregen": champ_stats['hpregen'],
            "hpregenperlevel": champ_stats['hpregenperlevel'],
            "mpregen": champ_stats['mpregen'],
            "mpregenperlevel": champ_stats['mpregenperlevel'],
            "crit": champ_stats['crit'],
            "critperlevel": champ_stats['critperlevel'],
            "attackdamage": champ_stats['attackdamage'],
            "attackdamageperlevel": champ_stats['attackdamageperlevel'],
            "attackspeedperlevel": champ_stats['attackspeedperlevel'],
            "attackspeed": champ_stats['attackspeed'],
            "patch_version" : champ_base['version']

        }

        # --- SQL Insert Query ---
        INSERT_QUERY = """
        INSERT INTO "lollov".champions (
            key, info_attack, info_defense, info_magic, info_difficulty,
            tags, partype,
            hp, hpperlevel, mp, mpperlevel, movespeed,
            armor, armorperlevel, spellblock, spellblockperlevel,
            attackrange, hpregen, hpregenperlevel, mpregen, mpregenperlevel,
            crit, critperlevel, attackdamage, attackdamageperlevel,
            attackspeedperlevel, attackspeed, patch_version
        )
        VALUES (
            %(key)s, %(info_attack)s, %(info_defense)s, %(info_magic)s, %(info_difficulty)s,
            %(tags)s, %(partype)s,
            %(hp)s, %(hpperlevel)s, %(mp)s, %(mpperlevel)s, %(movespeed)s,
            %(armor)s, %(armorperlevel)s, %(spellblock)s, %(spellblockperlevel)s,
            %(attackrange)s, %(hpregen)s, %(hpregenperlevel)s, %(mpregen)s, %(mpregenperlevel)s,
            %(crit)s, %(critperlevel)s, %(attackdamage)s, %(attackdamageperlevel)s,
            %(attackspeedperlevel)s, %(attackspeed)s, %(patch_version)s
        )
        ON CONFLICT (key, patch_version) DO UPDATE SET
            key = EXCLUDED.key,
            info_attack = EXCLUDED.info_attack,
            info_defense = EXCLUDED.info_defense,
            info_magic = EXCLUDED.info_magic,
            info_difficulty = EXCLUDED.info_difficulty,
            tags = EXCLUDED.tags,
            partype = EXCLUDED.partype,
            hp = EXCLUDED.hp,
            hpperlevel = EXCLUDED.hpperlevel,
            mp = EXCLUDED.mp,
            mpperlevel = EXCLUDED.mpperlevel,
            movespeed = EXCLUDED.movespeed,
            armor = EXCLUDED.armor,
            armorperlevel = EXCLUDED.armorperlevel,
            spellblock = EXCLUDED.spellblock,
            spellblockperlevel = EXCLUDED.spellblockperlevel,
            attackrange = EXCLUDED.attackrange,
            hpregen = EXCLUDED.hpregen,
            hpregenperlevel = EXCLUDED.hpregenperlevel,
            mpregen = EXCLUDED.mpregen,
            mpregenperlevel = EXCLUDED.mpregenperlevel,
            crit = EXCLUDED.crit,
            critperlevel = EXCLUDED.critperlevel,
            attackdamage = EXCLUDED.attackdamage,
            attackdamageperlevel = EXCLUDED.attackdamageperlevel,
            attackspeedperlevel = EXCLUDED.attackspeedperlevel,
            attackspeed = EXCLUDED.attackspeed,
            patch_version = EXCLUDED.patch_version;
        """


        with connection.cursor() as cur:
            cur.execute(INSERT_QUERY, champion_data_dict)
            connection.commit()

    print("✅ All champions processed.")
