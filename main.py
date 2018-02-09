#!/usr/bin/env python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import json
import sys

from packet import process_row

if len(sys.argv) < 2:
    print('Provide a sheet key')
    exit()

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(sys.argv[1]).get_worksheet(0)

rows = sheet.get_all_values()
packet = list(map(process_row, rows))

print(json.dumps(packet))
