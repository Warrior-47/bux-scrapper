from google.auth.exceptions import RefreshError, TransportError
from googleapiclient.discovery import build_from_document
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from PyQt5 import QtCore

from helpers import logger_setup

from concurrent.futures import TimeoutError
from pebble import concurrent
import pickle
import json
import time
import csv
import os

class Playlister(QtCore.QThread):
    int_progress_signal = QtCore.pyqtSignal(int)
    int_progress_max_signal = QtCore.pyqtSignal(int)
    str_signal = QtCore.pyqtSignal(str)
    down_done_signal = QtCore.pyqtSignal(int)


    def __init__(self, playlist_title):
        super().__init__()
        self.shutdown = False

        self.ids = self.extract_ids(playlist_title)

        self.progress = 0
        self.total_progress = len(self.ids)

        self.title = playlist_title
    

    def run(self):
        try:
            start_time = time.time()
            self.int_progress_max_signal.emit(self.total_progress)

            # Authenticating User
            self.str_signal.emit('Authenticate Using GSuite\nAuthenticating...')
            service = self.authenticate()

            # Updating GUI
            self.str_signal.emit('Authentication Successful')
            print('Authentication Successful.')

            # Creating the Required Playlist
            self.str_signal.emit('Creating Playlist')
            try:
                playlist_response = self.create_playlist(service)
            except HttpError as e:
                if e.status_code == 429:
                    # Rate Limit Exceeded
                    time.sleep(1)
                    counter = 0
                    while True:
                        try:
                            counter += 1
                            playlist_response = self.create_playlist(service)
                            break
                        except HttpError as e:
                            if e.status_code == 429:
                                time.sleep(2 ** counter)
                            else:
                                raise e
                else:
                    raise e

            playlist_id = playlist_response['id']

            print('Playlist Created.')

            # Updating GUI
            self.str_signal.emit('Adding Videos to Playlist')
            print('Adding Videos to Playlist.')

            # Adding videos to the playlist just created
            for i, id in enumerate(self.ids):
                if not self.shutdown:
                    try:
                        self.add_playlistItem(service, playlist_id, i, id)
                    except HttpError as e:
                        if e.status_code == 403:
                            # Exceeded Youtube Quota Limit
                            self.str_signal.emit('Exceeded Youtube Limit. Try Again Tomorrow.')
                            self.shutdown = True
                            self.down_done_signal.emit(0)
                            return

                        elif e.status_code == 404:
                            # Video No longer available
                            self.str_signal.emit('A Video is Unavailable. Skipping it')
                            print('A Video is Unavailable. Skipping it')
                            time.sleep(1)
                            self.str_signal.emit('Adding Videos to Playlist')
                            print('Adding Videos to Playlist')

                        elif e.status_code == 429:
                            # Rate Limit Exceeded
                            time.sleep(1)
                            counter = 0
                            while True:
                                try:
                                    counter += 1
                                    self.add_playlistItem(service, playlist_id, i, id)
                                    break
                                except HttpError as e:
                                    if e.status_code == 429:
                                        time.sleep(2 ** counter)
                                    else:
                                        raise e

                        else:
                            # As the exception thrown is unknown, passing to default handler
                            raise e

                    # Updating GUI
                    self.progress += 1
                    self.int_progress_signal.emit(self.progress)
                    print(f'{self.progress}/{self.total_progress} Done.')
                else:
                    # If main thread is closing, stop work
                    return
            
            # Updating GUI
            self.str_signal.emit('Done!')
            self.down_done_signal.emit(0)
        
        except Exception as e:
            self.handle_exceptions(e)
        
        finally:
            end_time = time.time()
            print('Finished In: ', end_time-start_time)
    

    @QtCore.pyqtSlot()
    def parent_closing(self):
        """Method used by main thread to notify
        Playlister to stop everything
        """
        self.shutdown = True


    def authenticate(self):
        """Creates an authenticated resource that can be used
        to make playlists for the account

        Returns:
            googleapiclient.discovery.Resource: Resource required to access user account
        """
        credentials = None

        # create new credentials.
        # Asking user for permission
        process = user_consent()
        credentials = process.result()

        with open('rest.json', 'rb') as f:
            service = json.loads(f.read())
        return build_from_document(service, credentials=credentials)


    def create_playlist(self, service):
        """Given a google service resource and a title, creates a
        youtube playlist in the account of the authenticated user

        Args:
            service (googleapiclient.discovery.Resource): Resource required to access user account
            title (str): Title of the Playlist

        Returns:
            dict: Dictionary that contains the playlist information
        """
        
        # Setting up the request parameters
        part = "snippet,status"
        body = {
            "snippet": {
                "title": self.title,
                "description": "No Description",
                "tags": [
                    str(self.title)+" playlist",
                    "API call"
                ],
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "unlisted"
            }
        }

        # Creating the request object
        req = service.playlists().insert(part=part, body=body)

        return req.execute()
    

    def add_playlistItem(self, service, playlistId, position, videoId):
        """Given a google service resource, playlist ID, and video ID, adds 
        a video to the playlist specified, in the account of the resource

        Args:
            service (googleapiclient.discovery.Resource): Resource required to access user account
            playlistId (str): ID of the playlist to add item to
            position (int): Position of the video in the playlist
            videoId (str): ID of the video

        Returns:
            dict: Dictionary that contains information about the playlistItem
        """

        # Setting up the request parameters
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

        # Creating the request object
        req = service.playlistItems().insert(part=part, body=body)

        return req.execute()
    

    def extract_ids(self, title):
        """Given the title, extracts the youtube ids from
        that title's .csv file

        Args:
            title (str): Usually the course ID

        Returns:
            list: A list containing all youtube IDs
        """
        try:
            with open(f'Output/{title}-youtube-videos.csv') as f:
                reader = csv.reader(f)
                next(reader, None)
                ids = [ i[1].split('=')[1] for i in reader ]

        except Exception as e:
            self.handle_exceptions(e)
        
        return ids
    

    def handle_exceptions(self, e):
        """Handles every possible exception thrown by app. Default Handler

        Args:
            e (Exception): the exception object that was thrown
        """
        if not self.shutdown:
            self.shutdown = True

            logger = logger_setup('Playlisting Logger')

            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print(message)

            if isinstance(e, TransportError):
                self.str_signal.emit(
                    'Check Your Internet Connection and Try Again')
            elif isinstance(e, HttpError):
                if e.status_code == 403:
                    self.str_signal.emit('Exceeded Youtube Limit. Try Again Tomorrow.')
                else:
                    # As the exception thrown is unknown, logging it in a file for debugging.
                    self.str_signal.emit(
                        'An Unknown Fatal Error Occurred. Contact Developer.')
                    logger.exception(type(e).__name__)
            elif isinstance(e, TimeoutError):
                # If the user takes too long or fails to authenticate.
                self.str_signal.emit('Authentication Timed out. Try Again.')
            else:
                # As the exception thrown is unknown, logging it in a file for debugging.
                self.str_signal.emit(
                    'An Unknown Fatal Error Occurred. Contact Developer.')
                logger.exception(type(e).__name__)

            self.down_done_signal.emit(0)

@concurrent.process(timeout=60)
def user_consent():
    """Asks user for permission to access account.
    Times out after 60 seconds.
    """
    with open('info.pickled', 'rb') as f1:
        # Done to store api secret somewhat private
        data = pickle.load(f1)
        with open('secrets.json', 'w') as f2:
            f2.write(data)

    flow = InstalledAppFlow.from_client_secrets_file(
        'secrets.json', scopes=["https://www.googleapis.com/auth/youtube"])
    
    os.remove('secrets.json')

    # Asking user for permission
    flow.run_local_server(port=8181, prompt='consent',
                        success_message="Authentication Complete. You may close the tab.",
                        open_browser=True)
    credentials = flow.credentials
    
    return credentials