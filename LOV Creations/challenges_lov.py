# This will be made for an LOV.

import constants
import psycopg
import time
import json
from datetime import datetime

from riotwatcher import LolWatcher, ValWatcher, ApiError, RiotWatcher

API_KEY = constants.API_KEY_SERVICE
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)
lol_region = 'na1'

db_pass = constants.db_password
db_ip = constants.db_ip

db_connection = f'dbname=yrden user=postgres password={db_pass} host={db_ip}'

conn = psycopg.connect(db_connection)
curs = conn.cursor()
patch_no = '14.1.1' # input('Enter the new patch number:')

#Thresholds key houses information on amount of points needed for each breakpoint of the tiers.

#Challenge IDS that end in 000 seem to be groups.
# Seasonal challenges begin with the year. 2022, 2023, 2024 etc.

'''
Split gathering information on challenges into 3 queries to maintain some data structure. 
Query 1 = Challenge Trees. 0-5
        index 0 has a length of 9. the rest have lengths of 7. Perfectly fine. Just needs to be accounted for in the code.
Query 2 = Challenge Categories within Trees. Those challenge IDs that end in 000
        Categories are all length 7. Easy to deal with.
Query 3 = actual challenges. Those challenge IDS that have some identifier for the last 3. All of their description/name etc is of length 3. 
        Challenges are of dynamic length for their thresholds.

    Now that I have seen the data structure, splitting into multiple queries is not needed for the localized names. Just put the damn data in there. ez pz.
    Thresholds are slightly different and will need to be adjusted. Let's see how.

    THE JOIN METHOD HERE IS INCREDIBLY EFFECTIVE FOR GENERATING QUERIES WITH PARAMETERS OF DYNAMIC LENGTH
'''

'''
Notes on the challenge ids:
    0 = the total points of all challenges
    1 = imagination
    2 = Expertise
    3 = Veterancy
    4 = Teamwork
    5 = Collection
'''
tree_query = '''SELECT DISTINCT CHALLENGE_ID FROM "yrden".LOL_CHALLENGES;'''
# category_query = '''SELECT DISTINCT CHALLENGE_ID FROM "YRDEN".LOL_CHALLENGES WHERE CAST(CHALLENGE_ID AS TEXT) LIKE '%000' '''
# challenge_query ='''SELECT DISTINCT CHALLENGE_ID FROM "YRDEN".LOL_CHALLENGES WHERE CAST(CHALLENGE_ID AS TEXT) NOT LIKE '%000' AND CHALLENGE_ID >10 '''

# Tree ID query
curs.execute(tree_query)
tree_ids = curs.fetchall()
tree_ids = [n[0] for n in tree_ids]

tree_ids.sort()

with conn.cursor() as curs:
    for index, ids in enumerate(tree_ids):
        id_dict = {'challenge_id' : ids}
        try:
            test = lol_watcher.challenges.challenge_config(lol_region, ids)
        except ApiError as err:
            if err.response.status_code == 429:
                time.sleep(30)
                test = lol_watcher.challenges.challenge_config(lol_region, ids)
            else:
                raise
        name_columns = ', '.join(test['localizedNames']['en_US'])

        name_values = ', '.join([f"%({key})s" for key in test['localizedNames']['en_US'].keys()])

        tier_columns = ', '.join(test['thresholds'])

        tier_values = ', '.join([f"%({key})s" for key in test['thresholds'].keys()])
        query_params_dict = {**id_dict, **test['localizedNames']['en_US'], **test['thresholds']}

        trees_query = f'''INSERT INTO "lollov".LOL_CHALLENGES (CHALLENGE_ID, {name_columns}, {tier_columns}) VALUES (%(challenge_id)s, {name_values}, {tier_values})'''
        # print(trees_query)
        # print(trees_query)
        # print(query_params_dict)
        curs.execute(trees_query, query_params_dict)
        # us_test = test['localizedNames']['en_US']
        # print(test.keys())
        # print(sorted(test['thresholds']))
        # print(len(test['thresholds']))
        # print(us_test)
    conn.commit()

print('End of program run.')


conn.close()
print('The database connection has closed.')

