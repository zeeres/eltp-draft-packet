# eltp-draft-packet

A light-weight Angular front-end for the ELTP draft packet.

If you wanna use this, feel free to send me a message on [reddit](https://reddit.com/u/Arfie99).

The program is currently based on the signup format for season 11, so will probably have to be changed if future commissioners are to use this.

## how it works

1. Python program connects to a Google Spreadsheet with responses and generates a JSON draft packet
2. The draft packet is uploaded to a web server using FTP
3. The front-end loads the JSON packet to populate itself

## requirements

python >=3.6, with the following packages (all can be installed using pip3):

* pycountry
* gspread
* requests
* oauth2client

To install the front-end, you will need nodejs and bower to install the dependencies.

## how to set up

You will need:

* one spreadsheet with sign-ups
* any amount of spreadsheets (but at least 3 to see it) with ratings; these ratings should appear in the first column (excluding the top row) and be in the same order as the signups on the first sheet
* one spreadsheet with comments, following the same format as the ratings sheets
* google dev credentials that can use google drive and access your responses sheet
* a web server with FTP store access

### installing the frontend

Simply go into the `web` folder and install the dependencies:

    cd web
    bower install

This may take a while. Once that's finished, transfer the entire contents of `web` (that is, including `bower_components`) to your web server.

### setting up the backend

The Python backend needs three files not present in this repo: `credentials.json`, `ftp.json` and `sheets.json`. Put these in the same folder as `main.py`, `packet.py` and `profiles.py`.

`credentials.json` is the JSON OAuth2 credentials file you can download from the Google dev console, which looks something like this:

    {
      "type": "service_account",
      "project_id": "...",
      "private_key_id": "...",
      "private_key": "...",
      "client_email": "draft-packet@eltp-xxxxxx.iam.gserviceaccount.com",
      "client_id": "...",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/draft-packet%40eltp-xxxxxx.iam.gserviceaccount.com"
    }

Make sure you share all relevant spreadsheets (in google drive) with the `client_email`. Doesn't matter if the sheet is public, it won't work unless you share it.

`ftp.json` contains credentials and a file path, something like this:

    {
        "host": "ftp.eltp.com.gov.edu.net",
        "user": "username",
        "pass": "hunter2",
        "path": "/var/www/html/"
    }

Make sure the `path` is the same place your static website already exists in.

`sheets.json` contains google spreadsheets keys (eg. XXXXX in https://docs.google.com/spreadsheets/d/XXXXX/edit) for responses, ratings and comments:

    {
        "packet": "key1",
        "ratings": [
            "key2",
            "key3"
        ],
        "comments": "key4"
    }

If all these files are present, you can try running the script:

    ./main.py

This may take a minute, depending on how many ratings sheets you have. If everything goes correctly, you'll see some debug output and the script will finish. Open your browser and go to the place you have uploaded the front-end to - the draft packet should be there!

If you want to set this up to run automagically every 15 minutes, you'll want to set up a cron job to do it. Create a file, anywhere, and name it `cron.txt` (or whatever). Put the following line in it:

    0,15,30,45 * * * * /usr/local/bin/python3 /path/to/eltp-draft-packet/main.py >/dev/null

Note that the `python3` path may also vary. You can find out by running `which python3` in your shell. Next, enable your cron job:

    crontab cron.txt

and that's it!
