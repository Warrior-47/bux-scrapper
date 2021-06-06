from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os


def authenticator():
    CREDENTIALS_PATH = 'youtube-credentials.pickled'
    if os.path.exists(CREDENTIALS_PATH):
        with open(CREDENTIALS_PATH, 'rb') as f:
            credentials = pickle.load(f)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json')

            flow.run_local_server(port=8181, prompt='consent')

            credentials = flow.credentials

            with open(CREDENTIALS_PATH, 'wb') as f:
                pickle.dump(credentials, f)

    return build('youtube', 'v3', credentials=credentials)


def create_playlist(service, title):
    part = "snippet,status"
    body = {
        "snippet": {
            "title": "Did it Work?",
            "description": "No Description",
            "tags": [
                str(title)+" playlist",
                "API call"
            ],
            "defaultLanguage": "en"
        },
        "status": {
            "privacyStatus": "unlisted"
        }
    }

    req = service.playlists().insert(part=part, body=body)

    return req.execute()


def add_playlistItem(service, playlistId, position, videoId):
    part = "snippet"
    body = {
        "snippet": {
            "playlistId": playlistId,
            "position": position,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": videoId
            }
        }
    }

    req = service.playlistItems().insert(part=part, body=body)

    return req.execute()
