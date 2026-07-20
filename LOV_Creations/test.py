import os, pprint
from riotwatcher import LolWatcher

API_KEY = os.environ['API_KEY_SERVICE']
lol_watcher = LolWatcher(API_KEY)

challenges = lol_watcher.challenges.config('na1')
pprint.pp(challenges[0])