import requests

QUEUES_URL = 'https://static.developer.riotgames.com/docs/lol/queues.json'


def queues_lov(connection):
    cur = connection.cursor()

    queues = requests.get(QUEUES_URL).json()

    for q in queues:
        queue_dict = {
            "queueId": q['queueId'],
            "map": q['map'],
            "description": q.get('description'),
            "notes": q.get('notes')
        }

        INSERT_QUERY = '''
        INSERT INTO "lollov".lol_queues (queueid, map, description, notes)
        VALUES (%(queueId)s, %(map)s, %(description)s, %(notes)s)
        ON CONFLICT (queueid) DO UPDATE SET
            map = EXCLUDED.map,
            description = EXCLUDED.description,
            notes = EXCLUDED.notes
        '''
        cur.execute(INSERT_QUERY, queue_dict)

    connection.commit()
    print('Queues processed successfully.')
