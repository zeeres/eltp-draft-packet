# eltp-draft-packet

A light-weight Angular front-end for the ELTP draft packet.

If you wanna use this, feel free to send me a message on [reddit](https://reddit.com/u/Arfie99).

The program is currently based on the signup format for season 11, so will probably have to be changed if future commissioners are to use this.

## how it works

1. Python program connects to a Google Spreadsheet with responses and generates a JSON draft packet
2. The draft packet is uploaded to a web server using FTP
3. The front-end loads the JSON packet to populate itself

## requirements

python3, with the following packages (can be installed using pip3):

* pycountry
* gspread
* gdata (i think)

## how to set up

You will need:

* google dev credentials that can use google drive and access your responses sheet
* a web server with FTP store access

First, upload the contents of the `web` folder to your web server.

The Python backend needs two files not present in this repo: `credentials.json` and `ftp.json`.

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

Make sure you share your responses spreadsheet (in google drive) with the `client_email`. Doesn't matter if the sheet is public, it won't work unless you share it.

`ftp.json` contains credentials and a file path, something like this:

    {
        "host": "ftp.eltp.com.gov.edu.net",
        "user": "username",
        "pass": "hunter2",
        "path": "/var/www/html/"
    }

Make sure the `path` is the same place your static website already exists in.

Run the script with a google spreadsheet key. The spreadsheet key can be found in the sheet URL (eg. http://docs.google.com/spreadsheets/d/XXXXX/edit where XXXXX is the key).

    ./main.py <spreadsheet key>

If everything goes correctly, this will generate the JSON packet and upload it to your web server in the place you chose.

You'll want to set this up to run automagically every so often. TBA.
