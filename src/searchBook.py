import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
# [A=time, B=name of book, C=name of author, D=link, E=age, F=subject, G=size]
# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "19F0Rmy9IDV1KCfOzSELEPYtgzxLQaM33ikSyKssy-K4"
RANGE = "!A2:G"
LIST = {4: ['תנ"ך', 'תנאים', 'אמוראים', 'גאונים', 'ראשונים', 'אחרונים'],
        5: ['תנ"ך', 'מקורות תנאיים', 'תלמוד ועיון', 'הלכה', 'מחשבה', 'מוסר', 'מנייני מצוות', 'קבלה', 'חסידות', 'ספרות'],
        6: ['לא מותאם', 'A5', 'A6', 'A7', 'A8']}

"""Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())


def getValues():
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=RANGE)
            .execute()
    )
    return result.get("values", [])


def searchBy(name, col):
    if col > 2 or col == 0:
        return
    try:
        values = getValues()
        return [v for v in values if name in v[col]]

    except HttpError as err:
        print(err)


def searchFromList(key, col):
    try:
        values = getValues()
        return [v for v in values if key == v[col]]

    except HttpError as err:
        print(err)


def main():
    print(searchFromList('מוסר', 5))


if __name__ == "__main__":
    main()
