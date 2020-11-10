
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import re
from apiclient.discovery import build
from apiclient.http import MediaFileUpload


def validate_google_api():
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.


    
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

            
  service = build('drive', 'v3', credentials=creds)
  return service

def upload_observation():

  service = validate_google_api()
  file_metadata = {'name': 'current_photo.jpg'}
  media = MediaFileUpload('images/current_photo.jpg', mimetype='image/jpeg')
  file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
  print(file.get('id'))
  
upload_observation()