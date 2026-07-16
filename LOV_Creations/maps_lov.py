import requests

MAPS_URL = 'https://static.developer.riotgames.com/docs/lol/maps.json'


def maps_lov(connection):
    cur = connection.cursor()

    maps = requests.get(MAPS_URL).json()

    for m in maps:
        map_dict = {
            "mapId": m['mapId'],
            "mapName": m['mapName'],
            "notes": m.get('notes')
        }

        INSERT_QUERY = '''
        INSERT INTO "lollov".maps (mapid, mapname, notes)
        VALUES (%(mapId)s, %(mapName)s, %(notes)s)
        ON CONFLICT (mapid) DO UPDATE SET
            mapname = EXCLUDED.mapname,
            notes = EXCLUDED.notes
        '''
        cur.execute(INSERT_QUERY, map_dict)

    connection.commit()
    print('Maps processed successfully.')
