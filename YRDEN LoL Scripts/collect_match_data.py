import time
import yrden_sql_queries
from riotwatcher import ApiError



def get_match_json(region, game_id, lol_watcher, max_retries=5):
    retries = 0

    while retries <= max_retries:
        try:
            return lol_watcher.match.by_id(region, game_id)
        except ApiError as err:
            if err.response.status_code == 429:
                retry_after = int(err.response.headers.get('Retry-After', 1))
                print(f'We should retry in {retry_after} seconds...')
                time.sleep(retry_after)
            elif err.response.status_code == 404:
                print('Match not found for game ID: {}'.format(game_id))
                return None
            elif err.response.status_code == 504 or err.response.status_code == 503 or err.response.status_code == 500:
                # 504 happens randomly, wait a couple seconds then try again
                print('Error Happened')
                retries += 1
                time.sleep(5)
            else:
                raise

# parses the participant ID based on the given summoner name
def get_participant_id(match_json, account_id):
    if match_json is None or 'metadata' not in match_json or 'participants' not in match_json['metadata']:
        
        return -1
    participant_json = match_json['metadata']['participants'] 
    # print(participant_json)
    if isinstance(account_id, str):
        for index, participant in enumerate(participant_json):
            if participant_json[index] in account_id:
                return index
    if isinstance(account_id, list):
        # account_id is a list of puuids
        for index, participant in enumerate(participant_json):
            if participant_json[index] in account_id:
                return index
    elif isinstance(account_id, dict):
        # account_id is a dictionary with a 'puuid' key
        for index, participant in enumerate(participant_json):
            if participant_json[index] == account_id.get('puuid'):
                return index
    print(account_id)
    print(type(participant_json))
    print(type(account_id))
    print('Error here')
    return -1

def collect_match_data(region, account_id, game_id, lol_watcher):
    match_json = get_match_json(region, game_id, lol_watcher)
    if match_json is None:
        print(f"No data available for game ID {game_id}.")
        return None
    # print(match_json)
    # dictionary to hold all the data values of interest from the MatchDto
    data = {}

    data.update({'duration': match_json['info']['gameDuration']})

    # rest of the stats are found in the participants section
    if type(account_id) != dict:
        participant_id = get_participant_id(match_json, account_id)
    else:
        participant_id = get_participant_id(match_json, account_id)
    # this shouldn't ever run but a -1 represents that the summoner was not in the match
    if participant_id == -1:
        print(game_id)
        return None
    if len(match_json['info']['participants']) == 0:
        return None
    # riot orders participants in the section 1-10, so can be indexed by subtracting one from the id
    # print(participant_id)
    participant_json = match_json['info']['participants'][participant_id]
    stats = participant_json
    primary_runes = participant_json['perks']['styles'][0]['selections']
    secondary_runes = participant_json['perks']['styles'][1]['selections']

    data.update({'gameMode' : match_json['info']['gameMode'],
        'queueId' : match_json['info']['queueId'],
        'gameVersion' : match_json['info']['gameVersion'],
        'championId': participant_json['championId'],
        'championName': participant_json['championName'],
        'lane' : participant_json['teamPosition'],
        'teamId' : participant_json['teamId'],
        'win': stats['win'],
        'kills': stats['kills'],
        'deaths': stats['deaths'],
        'assists': stats['assists'],
        'doublekills' : stats['doubleKills'],
        'triplekills' : stats['tripleKills'],
        'quadrakills' : stats['quadraKills'],
        'pentakills' : stats['pentaKills'],
        'gold_earned': stats['goldEarned'],
        'champion_damage': stats['totalDamageDealtToChampions'],
        'objective_damage': stats['damageDealtToObjectives'],
        'damage_healed': stats['totalHeal'],
        'vision_score': stats['visionScore'],
        'minions_killed': stats['totalMinionsKilled'],
        'neutral_monsters_killed': stats['neutralMinionsKilled'],
        'control_wards_purchased': stats['visionWardsBoughtInGame'],
        'keystone_rune': primary_runes[0]['perk'],
        'keystone_rune_var1' : primary_runes[0]['var1'],
        'keystone_rune_var2' : primary_runes[0]['var2'],
        'keystone_rune_var3' : primary_runes[0]['var3'],
        'primary_rune1': primary_runes[1]['perk'],
        'primary_rune2': primary_runes[2]['perk'],
        'primary_rune3': primary_runes[3]['perk'],
        'primary_rune1_var1' : primary_runes[1]['var1'],
        'primary_rune1_var2' : primary_runes[1]['var2'],
        'primary_rune1_var3' : primary_runes[1]['var3'],
        'primary_rune2_var1' : primary_runes[2]['var1'],
        'primary_rune2_var2' : primary_runes[2]['var2'],
        'primary_rune2_var3' : primary_runes[2]['var3'],
        'primary_rune3_var1' : primary_runes[3]['var1'],
        'primary_rune3_var2' : primary_runes[3]['var2'],
        'primary_rune3_var3' : primary_runes[3]['var3'],
        'secondary_rune1': secondary_runes[0]['perk'],
        'secondary_rune2': secondary_runes[1]['perk'],
        'secondary_rune1_var1': secondary_runes[0]['var1'],
        'secondary_rune1_var2': secondary_runes[0]['var2'],
        'secondary_rune1_var3': secondary_runes[0]['var3'],
        'secondary_rune2_var1': secondary_runes[1]['var1'],
        'secondary_rune2_var2': secondary_runes[1]['var2'],
        'secondary_rune2_var3': secondary_runes[1]['var3'],
        'summoner1_id': participant_json['summoner1Id'],
        'summoner1_casts':participant_json['summoner1Casts'],
        'summoner2_id': participant_json['summoner2Id'],
        'summoner2_casts': participant_json['summoner2Casts'],
        'nexusKills' : participant_json['nexusKills'],
                 'controlwardsbought' : participant_json['visionWardsBoughtInGame'],
                 'wardsKilled' : participant_json['wardsKilled'],
                 'wardsPlaced' : participant_json['wardsPlaced'],
                 'largestCriticalStrike' : participant_json['largestCriticalStrike'],
                 'game_id' : game_id,
                 'puuid' : participant_json['puuid']
    })
    
    return data


def get_all_summoner_matches(region, account_id, lol_watcher, max_retries=5):
    # maximum range of indices for match lists can only be 100
    index = 0

    retries = 0
    while retries <= max_retries:
        for n in range(1):
            #Start can go up to 900. Count can go to max 100. Can get last 1000 games. Must increment the start index in order to do so.
            try:
                response = lol_watcher.match.matchlist_by_puuid(region, account_id, start=0, count=50)
            except ApiError as err:
                if err.response.status_code == 429:
                    retry_after = int(err.response.headers.get('Retry-After', 1))
                    print(f'429 error in get_all_summoner_matches. We should retry in {retry_after} seconds...')
                    time.sleep(retry_after)
                    continue
                elif err.response.status_code == 404:
                    print('No matches found for Account ID: {}'.format(account_id))
                    return None
                elif err.response.status_code == 403:
                    print('Refresh your API Key')
                elif err.response.status_code == 504 or err.response.status_code == 503 or err.response.status_code == 500:
                    # 504 happens randomly, wait a couple seconds then try again
                    print('500 Error Happened in Get_All_Summoner_Matches.')
                    retries += 1
                    print(retries)
                    time.sleep(5)
                else:
                    raise

                if len(response) == 0:
                    break

                if len(response) == 100:
                    response
                    index += 100

                #print('Found', len(response), 'to add for Account ID:', account_id)
                return response


def commit_new_games(conn, riot_ids, lol_region, lol_watcher):
    with conn.cursor() as curs:
        for riot_id, riot_puuid in riot_ids:
                        
            vals = get_all_summoner_matches(lol_region, riot_puuid, lol_watcher)
            if vals is None:
                continue
            else:
                new_vals = {}
                curs.execute('''DROP TABLE "yrden".stage_lol_game_data;''')

                curs.execute('''CREATE TABLE "yrden".stage_lol_game_data
                                (puuid varchar,
                                game_id varchar,
                                riot_id varchar);''')
                curs.execute('''SELECT DISTINCT GAME_ID FROM "yrden".LOL_GAME_DATA WHERE RIOT_PUUID = %s;''', (riot_puuid,))
                game_check = curs.fetchall()
                for n in vals:
                    # print(f'Checking {n} for {riot_id}')
                    if n in game_check:
                        continue
                    new_vals.update({'puuid' : riot_puuid,
                                    'game_id' : n,
                                    'riot_id' : riot_id
                                    })

                    curs.execute('''INSERT INTO "yrden".stage_lol_game_data (puuid, game_id, riot_id)
                                    VALUES (%(puuid)s, %(game_id)s, %(riot_id)s);''', new_vals)

                    curs.execute('''INSERT INTO "yrden".lol_game_data (riot_puuid, game_id) 
                                    SELECT DISTINCT gst.puuid, gst.game_id
                                    FROM "yrden".stage_lol_game_data gst
                                    WHERE NOT EXISTS (SELECT game_id
                                    FROM "yrden".lol_game_data gdt
                                    WHERE gst.puuid = gdt.riot_puuid
                                    AND gst.game_id = gdt.game_id);
                                    ''')
                    
                curs.execute(''' SELECT DISTINCT GAME_ID FROM "yrden".LOL_GAME_DATA WHERE WIN IS NULL AND RIOT_PUUID = %s;''', (riot_puuid,))
                print(curs.rowcount, "new games committed for ", riot_id)
            curs.execute('''UPDATE "yrden".lol_game_data lgd
                    SET riot_id = yp.riot_id
                    FROM "yrden".people AS yp
                    WHERE lgd.riot_puuid = yp.riot_puuid
                    AND lgd.win is null;''')
                    
            conn.commit()

def update_lol_game_data(conn, account_res, lol_watcher):
    with conn.cursor() as curs:
        region = 'na1'
        curs.execute('''SELECT riot_id FROM "yrden".people WHERE riot_puuid = %(puuid)s ORDER BY riot_id;''', account_res)
        riot_id = curs.fetchall()
        curs.execute('''SELECT DISTINCT game_id FROM "yrden".lol_game_data WHERE riot_puuid = %(puuid)s AND win IS NULL;''', account_res)
        row_count = curs.rowcount
        game_id = curs.fetchall()
        game_res = [game_id[0] for game_id in game_id]

        for i in game_res:
            try:
                data = collect_match_data(region, account_res, i, lol_watcher)
                if data is None:
                    print(f"Data not found for {game_id[0][0]}, moving to next account.")
                    return

                #Used for debugging and to find types of the data dictionary
                
                values = (data['duration'],
                            data['gameMode'],
                        data['queueId'],
                        data['gameVersion'],
                        data['championId'],
                        data['championName'],
                        data['lane'],
                        data['teamId'],
                        data['win'],
                        data['kills'],
                        data['deaths'],
                        data['assists'],
                        data['doublekills'],
                        data['triplekills'],
                        data['quadrakills'],
                        data['pentakills'],
                        data['gold_earned'],
                        data['champion_damage'],
                        data['objective_damage'],
                        data['damage_healed'],
                        data['vision_score'],
                        data['minions_killed'],
                        data['neutral_monsters_killed'],
                        data['keystone_rune'],
                        data['keystone_rune_var1'],
                        data['keystone_rune_var2'],
                        data['keystone_rune_var3'],
                        data['primary_rune1'],
                        data['primary_rune2'],
                        data['primary_rune3'],
                        data['primary_rune1_var1'],
                        data['primary_rune1_var2'],
                        data['primary_rune1_var3'],
                        data['primary_rune2_var1'],
                        data['primary_rune2_var2'],
                        data['primary_rune2_var3'],
                        data['primary_rune3_var1'],
                        data['primary_rune3_var2'],
                        data['primary_rune3_var3'],
                        data['secondary_rune1'],
                        data['secondary_rune2'],
                        data['secondary_rune1_var1'],
                        data['secondary_rune1_var2'],
                        data['secondary_rune1_var3'],
                        data['secondary_rune2_var1'],
                        data['secondary_rune2_var2'],
                        data['secondary_rune2_var3'],
                        data['largestCriticalStrike'],
                        data['nexusKills'],
                        data['summoner1_id'],
                        data['summoner1_casts'],
                        data['summoner2_id'],
                        data['summoner2_casts'],
                        data['controlwardsbought'],
                        data['wardsKilled'],
                        data['wardsPlaced'],
                        data['game_id'],
                        data['puuid']  
                            )
                # Print the data dictionary
                
                curs.execute(yrden_sql_queries.update_game_data, values)
                #print(f"game {i} is now in for {riot_id[0][0]}")
            except ApiError as err:
                if err.response.status_code == 404:
                #Handling Missing Game data when the games are far too old.
                    break
                elif err.response.status_code == 429:
                    print('API Rate limit reached')
                    time.sleep(5)
                    continue
                else:
                    raise
            
        conn.commit()