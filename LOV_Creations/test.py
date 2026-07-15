def summoners_lov(connection, lol_watcher):
    cur = connection.cursor()
    DDRegion = lol_watcher.data_dragon.versions_for_region('na1')['n']
    DDsummoner = DDRegion['summoner']
    summoners = lol_watcher.data_dragon.summoner_spells(DDsummoner)['data']
    summoner_dict = {}
    cur.execute(''' DROP TABLE "lollov".summoner_spells ''')
    cur.execute(''' CREATE TABLE "lollov".summoner_spells
    (
    spell_name varchar,
    spell_id int,
    modes varchar
    );''')
    for n in summoners:
        summoner_dict.update({'spell_name' : summoners[n]['name'],
                                'spell_id' : summoners[n]['key'],
                                'modes' : summoners[n]['modes']})
        cur.execute('''INSERT INTO "lollov".summoner_spells
        (spell_name, spell_id, modes)
        VALUES
        (%(spell_name)s, %(spell_id)s, %(modes)s);''', summoner_dict)
        print(f"{n} has been added to the LOV.")
    connection.commit()
