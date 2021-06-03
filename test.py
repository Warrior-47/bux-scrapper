import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=[
                                                 'https://www.googleapis.com/auth/youtube.force-ssl'])

flow.run_local_server(port=8181, prompt='consent')

credentials = flow.credentials

print(credentials.to_json())