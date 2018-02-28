#!/usr/bin/env python3

from ftplib import FTP
from datetime import datetime
from datetime import timezone
import io
import json
import os
import sys

if len(sys.argv) < 2:
    print("""
usage: python3 draft.py [command]

command:
    set_date <%Y-%m-%d %H:%M:%S> - set the start date of the draft (UTC)
    start                        - start the draft
    stop                         - stop the draft
    pick <player> <team>         - pick a player by name and team abbreviation
    show <n>                     - show the n last picks, defaults to all picks
    remove <player>              - remove a pick
    go_back <n>                  - revert n picks, defaults to 1
    reset                        - reset everything
""")
    exit()


dirname = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dirname, 'ftp.json')) as f:
    data = json.load(f)
    ftphost = data['host']
    ftpuser = data['user']
    ftppwd = data['pass']
    ftppath = data['path']


def save():
    data = {
        'draft': draft,
        'start': int(start.replace(tzinfo=timezone.utc).timestamp())
    }
    raw = json.dumps(data, separators=(',', ':'))

    with open(os.path.join(dirname, 'draft.json'), 'w') as f:
        f.write(raw)

    print('Connecting to FTP...')
    ftp = FTP(ftphost, ftpuser, ftppwd)
    ftp.cwd(ftppath)

    print('Uploading...')
    bio = io.BytesIO(bytes(raw, 'utf-8'))
    ftp.storbinary('STOR draft.json', bio)
    ftp.close()
    print('Done!')


try:
    with open(os.path.join(dirname, 'draft.json')) as f:
        data = json.load(f)
        draft = data.get('draft', [])
        start = datetime.utcfromtimestamp(data.get('start', 0))
except FileNotFoundError:
    print('Draft data not found, creating...')
    draft = []
    start = datetime.utcfromtimestamp(0)
    save()
