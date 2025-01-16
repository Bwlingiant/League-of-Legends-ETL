import constants
import json
import psycopg

conn = psycopg.connect(constants.db_connection)
curs = conn.cursor()

'''
id is needed for all.
name is what is required for our use.
n['name'] and n['id'] are all that is needed from the first section.


['slots'][0]['runes'] is all the keystones for each tree.
'''
patch_no = input('Enter the new patch number:')

with open(f'Data Dragon Files/dragontail-{patch_no}/dragontail-{patch_no}/{patch_no}/data/en_US/runesReforged.json') as file:
    data = json.load(file)
    rune_dict = {}
    for trees in data:
        rune_slots = trees['slots']
        for runes in rune_slots:
            rune = runes['runes']
            for index, r in enumerate(rune):
                curs.execute('''select distinct rune_id, patch_id from "lollov".lol_runes;''')
                id_check = curs.fetchall()
                rune_dict.update({'rune_id' : r['id'],
                                 'rune_name' : r['name'],
                                 'shortDesc' : r['shortDesc'],
                                 'longDesc' : r['longDesc'],
                                 'patch_id' : patch_no})

                for tup in id_check:
                    if tup[0] == rune_dict['rune_id'] and tup[1] == rune_dict['patch_id']:
                        break
                curs.execute(''' INSERT INTO "lollov".lol_runes (rune_id, rune_name, short_desc, long_desc, patch_id)
                             VALUES (%(rune_id)s, %(rune_name)s, %(shortDesc)s, %(longDesc)s, %(patch_id)s)
                             ;
                             ''', rune_dict)
conn.commit()
conn.close()
print('The database connection has closed.')