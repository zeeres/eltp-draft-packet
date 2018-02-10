#!/usr/bin/env python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from ftplib import FTP
import io
import json

from packet import process_row

print('Loading GSheet keys...')

with open('sheets.json') as f:
    data = json.load(f)
    sheet_packet = data['packet']
    sheet_ratings = data['ratings']
    sheet_comments = data['comments']

print('Authorizing GSheets...')

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(sheet_packet).get_worksheet(0)

print('Opened spreadsheet, creating draft packet...')

rows = sheet.get_all_values()
packet = list(map(process_row, rows[1:]))
raw = json.dumps(packet)

print(f'Draft packet created with {len(packet)} rows')

with open('ftp.json') as f:
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
