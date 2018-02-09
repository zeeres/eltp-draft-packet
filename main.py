#!/usr/bin/env python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import json
import sys
from itertools import count

if len(sys.argv) < 2:
    print('Provide a sheet key')
    exit()

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(sys.argv[1]).get_worksheet(0)

packet = []

for i in count(2):
    row = sheet.row_values(i)

    if not any(row):  # empty row will just be empty strings
        break

    (
        timestamp,
        player_name,
        old_name,
        tagpro_id,
        reddit_name,

        country,
        ping_orbit,
        ping_chord,

        w1,
        w2,
        w3,
        w4,
        w5,
        w6,
        w7,
        w8,
        w9,
        w10,
        w11,
        w12,
        w13,
        w14,

        monday,
        tuesday,
        wednesday,
        thursday,
        friday,
        saturday,
        sunday,

        comment_availability,

        position,
        position_preference,

        microphone,

        comment,

        *_
    ) = row

    packet.append({
        'name': player_name,
        'old_name': old_name,
        'reddit': reddit_name,
        'profile': tagpro_id,
        'country': country,
        'ping': {
            'chord': ping_chord,
            'orbit': ping_orbit
        },

        'availability': {
            'weekly': [w1, w2, w3, w4, w5, w6, w7,
                       w8, w9, w10, w11, w12, w13, w14],
            'daily': [monday, tuesday, wednesday, thursday,
                      friday, saturday, sunday],
            'comment': comment_availability
        },

        'position': {
            'primary': position,
            'preference': position_preference
        },

        'microphone': microphone,

        'comment': 'comment'
    })

print(json.dumps(packet))
