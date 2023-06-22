from __future__ import print_function
from flask import Flask

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello!,World.."



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '19-_AM85_-k7SMplw9Rsp3XWGN6Jatfnl8nGHX3S2JpY'
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Sheet1!A1:B'

"""Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
with open('token.json', 'w') as token:
            token.write(creds.to_json())

@app.route('/sheets')
def main():
    

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not result:
            print('No data found.')
            return 'No data found.'

        return values 
    except HttpError as err:
        print(err)

@app.route('/update',methods=['PUT'])
def update():
    service = build('sheets','v4',credentials=creds)
    sheet = service.spreadsheets()
    valueInput = ''
    value = {
         'majorDimension':'COLUMNS',
         'values':[["Chef Damu","Chef Bhat","Chef John"]]
    }
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='Sheet1!B1',valueInputOption='USER_ENTERED',body=value).execute()
    return result

@app.route('/delete',methods=['POST'])
def delete():
     service = build('sheets','v4',credentials=creds)
     sheet = service.spreadsheets()
     result = sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='Sheet1!A:B',body={}).execute()
     return result

if __name__ == '__main__':
    main()