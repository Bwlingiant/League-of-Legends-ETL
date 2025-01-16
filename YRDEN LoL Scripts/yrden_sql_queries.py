get_new_summoners = 'SELECT distinct summoner_name FROM "yrden".people WHERE summoner_name is NOT NULL AND riot_puuid is NULL;'
get_current_riot_puuids_yrden = 'SELECT distinct riot_puuid FROM "yrden".people WHERE riot_puuid is NOT NULL AND "YRDEN_FLAG" = True;'
missing_riotids = 'SELECT riot_id, riot_key FROM "yrden".people WHERE riot_id is NOT NULL AND riot_puuid is NULL; '
get_current_riotids_yrden = 'SELECT distinct riot_id FROM "yrden".people WHERE summoner_name is NOT NULL AND riot_puuid is NOT NULL AND "YRDEN_FLAG" = True;'
get_current_riotids_all = 'SELECT riot_id FROM "yrden".people WHERE summoner_name is NOT NULL AND riot_puuid is NOT NULL;'
udpate_riotids = 'UPDATE "yrden".people SET riot_puuid = %(puuid)s WHERE riot_id = %(riot_id)s AND riot_key = %(riot_key)s;'
get_summoner_ids = '''SELECT SUMMONER_ID FROM "yrden".PEOPLE WHERE SUMMONER_ID IS NOT NULL AND "YRDEN_FLAG" = True;'''
get_puuids_yrden = '''SELECT DISTINCT RIOT_PUUID FROM "yrden".PEOPLE WHERE RIOT_PUUID IS NOT NULL AND "YRDEN_FLAG" = True;'''
get_puuids_all = '''SELECT DISTINCT RIOT_PUUID FROM "yrden".PEOPLE WHERE RIOT_PUUID IS NOT NULL;'''
update_game_data = '''UPDATE "yrden".lol_game_data
                SET game_duration = %s,
                    game_mode = %s,
                    queue_id = %s,
                    game_patch = %s,
                    champion_id = %s,
                    champion_name = %s,
                    lane = %s,
                    teamid = %s,
                    win = %s,
                    kills = %s,
                    deaths = %s,
                    assists = %s,
                    double_kills = %s,
                    triple_kills = %s,
                    quadra_kills = %s,
                    penta_kills = %s,
                    gold_earned = %s,
                    champion_damage = %s,
                    objective_damage = %s,
                    damage_healed = %s,
                    vision_score = %s,
                    minions_killed = %s,
                    neutral_monsters_killed = %s,
                    keystone_rune_code = %s,
                    keystone_rune_var1 = %s,
                    keystone_rune_var2 = %s,
                    keystone_rune_var3 = %s,
                    primary_rune_code1 = %s,
                    primary_rune_code2 = %s,
                    primary_rune_code3 = %s,
                    primary_rune1_var1 = %s,
                    primary_rune1_var2 = %s,
                    primary_rune1_var3 = %s,
                    primary_rune2_var1 = %s,
                    primary_rune2_var2 = %s,
                    primary_rune2_var3 = %s,
                    primary_rune3_var1 = %s,
                    primary_rune3_var2 = %s,
                    primary_rune3_var3 = %s,
                    secondary_rune_code1 = %s,
                    secondary_rune_code2 = %s,
                    secondary_rune1_var1 = %s,
                    secondary_rune1_var2 = %s,
                    secondary_rune1_var3 = %s,
                    secondary_rune2_var1 = %s,
                    secondary_rune2_var2 = %s,
                    secondary_rune2_var3 = %s,
                    largest_critical_strike = %s,
                    nexus_kills = %s,
                    summoner1_id = %s,
                    summoner1_casts = %s,
                    summoner2_id = %s,
                    summoner2_casts = %s,
                    control_wards_purchased = %s,
                    wards_killed = %s,
                    wards_placed = %s
                WHERE game_id = %s AND riot_puuid = %s;'''

drop_gamedata_staging = '''DROP TABLE "yrden".stage_lol_game_data;'''
create_gamedata_staging = '''CREATE TABLE "yrden".stage_lol_game_data
            (puuid varchar,
            game_id varchar,
            riot_id varchar);'''