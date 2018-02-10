import requests


def load_profiles(packet):
    ids = list(map(lambda x: x['profile'], packet))
    i = 0

    print(f'Loading {len(packet)} profiles...')

    while i < len(ids):
        current = ids[i:i+100]
        url = 'http://tagpro-chord.koalabeast.com/profiles/' +\
              ','.join(current)
        res = requests.get(url)

        indices = dict(map(lambda x: (x[1], x[0]), enumerate(current)))

        if res.status_code != 200:
            print('Error: /profiles responded with'
                  f'status code {res.status_code}')
            exit()

        for x in res.json():
            j = indices[x['_id']]
            out = packet[i + j]
            out['flair'] = x['selectedFlair'].replace('.', '-')
            out['stats'] = {
                'rolling': {
                    'current': x['stats']['rollingCache']['winRate'],
                    'best':    x['stats']['rollingCache']['bestWinRate'],
                    'games':   x['stats']['rollingCache']['games']
                }
            }

        i += 100
