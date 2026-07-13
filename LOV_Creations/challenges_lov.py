# This will be made for an LOV.
import os
import pprint
from datetime import datetime

from riotwatcher import LolWatcher, ValWatcher, ApiError, RiotWatcher

def challenge_lov (connection, lol_watcher):
    cur = connection.cursor()
    
    challenges = lol_watcher.challenges.config('na1')

    for ch in challenges:
        pprint.pp(ch)
        localized_us = ch['localizedNames']['en_US']
        thresholds = ch['thresholds']
        challenges_dict = {
            "id" : ch['id'],
            "name" : localized_us['name'],
            "description" : localized_us['description'],
            "shortDescription" : localized_us['shortDescription'],
            "state" : ch['state'],
            "leaderboard" : ch['leaderboard'],
            "iron" : thresholds.get('IRON'),
            "bronze" : thresholds.get('BRONZE'),
            "silver" : thresholds.get('SILVER'),
            "gold" : thresholds.get('GOLD'),
            "platinum" : thresholds.get('PLATINUM'),
            "diamond" : thresholds.get('DIAMOND'),
            "master" : thresholds.get('MASTER'),
            "grandmaster" : thresholds.get('GRANDMASTER'),
            "challenger" : thresholds.get('CHALLENGER')
        }

        INSERT_QUERY = '''
        INSERT INTO "lollov".challenges
        (challenge_id, name, description, shortdescription, state, leaderboard,
        iron, bronze, silver, gold, platinum, diamond, master, grandmaster, challenger)
        VALUES
        (%(id)s, %(name)s, %(description)s, %(shortDescription)s, %(state)s, %(leaderboard)s,
        %(iron)s, %(bronze)s, %(silver)s, %(gold)s, %(platinum)s, %(diamond)s,
        %(master)s, %(grandmaster)s, %(challenger)s)
        ON CONFLICT (challenge_id) DO UPDATE SET
            name = EXCLUDED.name,
            description = EXCLUDED.description,
            shortdescription = EXCLUDED.shortdescription,
            state = EXCLUDED.state,
            leaderboard = EXCLUDED.leaderboard,
            iron = EXCLUDED.iron,
            bronze = EXCLUDED.bronze,
            silver = EXCLUDED.silver,
            gold = EXCLUDED.gold,
            platinum = EXCLUDED.platinum,
            diamond = EXCLUDED.diamond,
            master = EXCLUDED.master,
            grandmaster = EXCLUDED.grandmaster,
            challenger = EXCLUDED.challenger
        '''
        cur.execute(INSERT_QUERY, challenges_dict)
        connection.commit()