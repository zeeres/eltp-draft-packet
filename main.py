#!/usr/bin/env python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from ftplib import FTP
import io
import json
import sys

from packet import process_row

if len(sys.argv) < 2:
    print('Provide a sheet key')
    exit()

print('Authorizing GSheets...')

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(sys.argv[1]).get_worksheet(0)

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
    filename = data['filename']

print('Connecting to FTP...')
ftp = FTP(host, user, pwd)
ftp.cwd(path)

print('Uploading draft packet...')
bio = io.BytesIO(bytes(raw, "utf-8"))
ftp.storbinary(f'STOR {filename}', bio)
ftp.close()
print('Done!')
