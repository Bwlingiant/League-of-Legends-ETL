import constants
import json
import psycopg

conn = psycopg.connect(constants.db_connection)
curs = conn.cursor()

patch_no = input('Enter the new patch number:')

with open(f'Data Dragon Files/dragontail-{patch_no}/dragontail-{patch_no}/{patch_no}/data/en_US/championFull.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    # print(data.keys())
    # print(data['data'].keys())
    # print(data['data']['Aatrox'])
    champion_id_dict = {}
    champion_dict = {}
    for keys in data['keys']:
        champion_id_dict.update({'champion_id' : keys,
                                 'champion_name' : data['keys'][keys]})
        
        #print(champion_id_dict)
        curs.execute('''
                     INSERT INTO "lollov".lol_champions (champion_id, champion_name)
                     VALUES (%(champion_id)s, %(champion_name)s);''', champion_id_dict)
    """ 
    In the below for loop I have the following keys
    dict_keys(['id', 'key', 'name', 'title', 'image', 'skins', 'lore', 
    'blurb', 'allytips', 'enemytips', 'tags', 'partype', 'info', 'stats', 
    'spells', 'passive', 'recommended'])

    I need the following:
    'key', 'tags', 'partype', 'stats'(I will delve further into this for more keys)
    """
    for champion in data['data']:
        champion_info = data['data'][champion]
        champ_stats = champion_info['stats']
        # print(champ_stats.keys())
        champion_dict.update({
                              'tags' : champion_info['tags'],
                              'partype' : champion_info['partype'],
                              'champion_id' : champion_info['key'],
                              'hp' : champ_stats['hp'],
                              'hp_per_level' : champ_stats['hpperlevel'],
                              'mp' : champ_stats['mp'],
                              'mp_per_level' : champ_stats['mpperlevel'],
                              'movespeed' : champ_stats['movespeed'],
                              'armor' : champ_stats['armor'],
                              'armorperlevel' : champ_stats['armorperlevel'],
                              'mr' : champ_stats['spellblock'],
                              'mr_per_level' : champ_stats['spellblockperlevel'],
                              'attackrange' : champ_stats['attackrange'],
                              'hp_regen' : champ_stats['hpregen'],
                              'hp_regen_per_level' : champ_stats['hpregenperlevel'],
                              'mp_regen' : champ_stats['mpregen'],
                              'mp_regen_per_level' : champ_stats['mpregenperlevel'],
                              'crit' : champ_stats['crit'],
                              'crit_per_level' : champ_stats['critperlevel'],
                              'attack_damage' : champ_stats['attackdamage'],
                              'attack_damage_per_level' : champ_stats['attackdamageperlevel'],
                              'attack_speed_per_level' : champ_stats['attackspeedperlevel'],
                              'attack_speed' : champ_stats['attackspeed'],
                              'patch_no' : patch_no
                              })
        print(champion_dict)
        champion_update_query = f'''UPDATE "lollov".lol_champions
            SET 
            hp = %(hp)s,
            partype = %(partype)s,
            hp_per_level = %(hp_per_level)s,
            mp = %(mp)s,
            mp_per_level = %(mp_per_level)s,
            movespeed = %(movespeed)s,
            armor = %(armor)s,
            armorperlevel = %(armorperlevel)s,
            mr = %(mr)s,
            mr_per_level = %(mr_per_level)s,
            attackrange = %(attackrange)s,
            hp_regen = %(hp_regen)s,
            hp_regen_per_level = %(hp_regen_per_level)s,
            mp_regen = %(mp_regen)s,
            mp_regen_per_level = %(mp_regen_per_level)s,
            crit = %(crit)s,
            crit_per_level = %(crit_per_level)s,
            attack_damage = %(attack_damage)s,
            attack_damage_per_level = %(attack_damage_per_level)s,
            attack_speed_per_level = %(attack_speed_per_level)s,
            attack_speed = %(attack_speed)s,
            patch_no = %(patch_no)s
            WHERE champion_id = %(champion_id)s;'''
        
        curs.execute(champion_update_query, champion_dict)

    conn.commit()


conn.close()
print('The database connection has closed')