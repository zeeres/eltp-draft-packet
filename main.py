#!/usr/bin/env python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from collections import defaultdict
from ftplib import FTP
import io
import json
import os

from packet import process_row
from profiles import load_profiles

dirname = os.path.dirname(os.path.realpath(__file__))

print('Loading GSheet keys...')

with open(os.path.join(dirname, 'sheets.json')) as f:
    data = json.load(f)
    sheet_packet = data['packet']
    sheet_ratings = data['ratings']
    sheet_comments = data['comments']

print('Authorizing GSheets...')

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    os.path.join(dirname, 'credentials.json'), scope)
gc = gspread.authorize(credentials)


# Aggregate ratings

class Rating:
    def __init__(self):
        self.ratings = []

    def add(self, rating):
        if 0 <= rating <= 10:
            self.ratings.append(rating)
        else:
            print(f'Rating {rating} is outside of range')

    def get_rating(self):
        if len(self.ratings) < 3:
            return 0

        s = sorted(self.ratings)[1:-1]
        return sum(s) / len(s)


ratings = defaultdict(Rating)

print(f'Reading {len(sheet_ratings)} ratings sheets...')

for s in sheet_ratings:
    sheet = gc.open_by_key(s).get_worksheet(0)
    column = sheet.col_values(1)[1:]
    for i, x in enumerate(column):
        try:
            if isinstance(x, str):
                x = x.replace(',', '.')
            r = float(x)
            ratings[i].add(r)
        except ValueError:
            if x != '':
                print(f'Invalid rating {x}')

print('Finished reading ratings.')

# Create packet

sheet = gc.open_by_key(sheet_packet).get_worksheet(0)

print('Opened draft packet spreadsheet, creating draft packet...')

rows = sheet.get_all_values()
packet = []
for i, r in enumerate(rows[1:]):
    packet.append(process_row(r, ratings[i]))

print(f'{len(packet)} signups processed.')

print('Reading player comments...')
sheet = gc.open_by_key(sheet_comments).get_worksheet(0)
for i, x in enumerate(sheet.col_values(1)[1:]):
    if x:
        packet[i]['rating_comment'] = x

print('Sorting the packet...')
packet = sorted(packet, key=lambda r: -r['rating'])
load_profiles(packet)

print('Removing removed signups...')

packet = list(filter(lambda x: not x['removed'], packet))
for x in packet:
    del x['removed']

raw = json.dumps(packet, separators=(',', ':'))
print(f'Draft packet created with {len(packet)} rows')

with open(os.path.join(dirname, 'ftp.json')) as f:
    data = json.load(f)
    host = data['host']
    user = data['user']
    pwd = data['pass']
    path = data['path']

print('Connecting to FTP...')
ftp = FTP(host, user, pwd)
ftp.cwd(path)

print('Uploading draft packet...')
bio = io.BytesIO(bytes(raw, "utf-8"))
ftp.storbinary('STOR packet.json', bio)
ftp.close()
print('Done!')
