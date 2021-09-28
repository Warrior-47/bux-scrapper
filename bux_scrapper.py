from PyQt5.QtCore import QThreadPool
from bs4 import BeautifulSoup
from PyQt5 import QtCore
import requests
import html

from helpers import logger_setup

from json import loads as jsonloads
import time


class CourseNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        """
        The Exception thrown if the user is not enrolled in the course
        or if the course does not exist

        """
        super().__init__(*args, **kwargs)


class InvalidEmailPasswordException(Exception):
    def __init__(self, *args, **kwargs):
        """
        The Exception thrown if the user inputs invalid Email or Password

        """
        super().__init__(*args, **kwargs)


class WorkerSignals(QtCore.QObject):
    """
    Signals sent to the parent scrapper thread about updating data or
    if an exception occurs

    """
    data_signal = QtCore.pyqtSignal(tuple)
    exception_signal = QtCore.pyqtSignal(Exception)


class DownloadingWorker(QtCore.QRunnable):

    def __init__(self, index, session, url, section_name):
        """The Runnable thread that finds the youtube video IDs from
        the content pages

        Args:
            index (int): ID of the thread for sorting
            session (requests.sessions.Session): The persistent HTTP connection thats logged into buX
            url (str): Hyperlink text for the content page that contains the youtube IDs
            section_name (str): Name of the section videos belong to
        """
        super().__init__()
        self.index = index
        self.session = session
        self.url = url
        self.section_name = section_name
        self.emitter = WorkerSignals()

    def run(self):
        try:
            # Requesting for the content page
            content_response = self.session.get(self.url)

            # Making a list of all the youtube video links
            youtube_url_list = self._find_youtube_link(
                content_response.text)

            # Passing the youtube link data to the parent thread
            self.emitter.data_signal.emit(
                (self.index, self.section_name, youtube_url_list))

        except Exception as e:
            # In case application is closed or connection error occurs
            self.emitter.exception_signal.emit(e)

    def _find_youtube_link(self, html_text):
        """Scrapes the json object that contains the youtube IDs of the page

        Args:
            html_text (str): HTML code of the content page as a string

        Returns:
            list: A list of youtube links created using the youtube video IDs
        """
        youtube_urls = []
        base_youtube_url = 'https://www.youtube.com/watch?v='

        # Converting html entities to utf-8
        html_text = html.unescape(html_text)

        # Parsing the html text
        soup = BeautifulSoup(html_text, 'lxml')

        for divs in soup.findAll('div', class_='video closed'):
            # Finding the youtube ID location and taking the json object as string
            # then making the youtube link and creating a list
            # Try catch block in case the page does not contain any video
            try:
                youtube_urls.append(
                    base_youtube_url+self._find_youtube_id(divs['data-metadata']))
            except:
                pass

        return youtube_urls

    def _find_youtube_id(self, s):
        """Extracts the youtube ID from the json object passed
        as parameter

        Args:
            s (str): The json object as a string

        Returns:
            str: the youtube ID of the video
        """
        parsed_json = jsonloads(s)
        id_ = parsed_json['streams'].split(':')[1]
        return id_


class Scrapper(QtCore.QThread):
    int_progress_signal = QtCore.pyqtSignal(int)
    int_progress_max_signal = QtCore.pyqtSignal(int)
    str_signal = QtCore.pyqtSignal(str)
    down_done_signal = QtCore.pyqtSignal(int)

    def __init__(self, email, pass_, course_id):
        """The main scrapper class. Given the email, password and
        course ID of an enrolled course, it searches buX for the course
        and scraps all of its youtube videos IDs and creates valid
        youtube links out of them.

        Args:
            email (str): user's buX email
            pass_ (str): user's buX password
            course_id (str): ID of the course user wants to scrap
        """
        super().__init__()
        # To manage a pool of workers to request and find multiple
        # youtube ids concurrently
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(8)
        self.shutdown = False # Flag to notify if the GUI is closed by user

        # Information required for login
        self.url = 'https://bux.bracu.ac.bd'
        self.login_route = 'https://bux.bracu.ac.bd/user_api/v1/account/login_session/'
        self.request_url = '/dashboard'
        self.youtube_urls = []

        self.__email = email
        self.__pass_ = pass_
        self.__course_id = course_id

        # Tracking progress to update GUI real-time
        self.total_links = 0
        self.downloaded = 0

    def run(self):
        start_time = time.time()

        # Updating GUI
        self.str_signal.emit('Logging In')
        print('Loggin In.')

        # Starting a persistent HTTP connection
        with requests.Session() as session:
            try:
                # All nescessary info for successfully logging in
                csrf_token = session.get(self.url).cookies['csrftoken']

                HEADERS = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                    'Host': 'bux.bracu.ac.bd',
                    'Origin': self.url,
                    'Referer': 'https://bux.bracu.ac.bd/login?next=%2F',
                    'X-CSRFToken': csrf_token
                }

                login_payload = {
                    'email': self.__email,
                    'password': self.__pass_
                }

                login_req = session.post(
                    self.login_route, headers=HEADERS, data=login_payload)

                if not login_req.ok:
                    # Incorrect email or password given
                    raise InvalidEmailPasswordException(
                        "Email or Password is Incorrect")

                # Updating GUI
                self.str_signal.emit('Successfully Logged In')
                print('Successfully Logged In.')

                # Requesting buX student dashboard page
                response = session.get(self.url+self.request_url)

                # Getting the desired course hyperlink
                course_link = self._find_course_link(response)

                # Requesting the course page
                course = session.get(course_link)

                # Getting a list of hyperlinks of all pages that contain
                # the youtube videos. (Sub sections)
                content_urls = self._find_course_content_url(course)

                self.total_links = len(content_urls)
                self.youtube_urls = [0] * self.total_links

                # Updating GUI
                self.int_progress_max_signal.emit(self.total_links)
                self.str_signal.emit('Downloading')
                print('Downloading.')

                # Starting 4 worker threads at a time to concurrently request
                # 4 different subsections links to scrap youtube IDs concurrently
                for idx, (section_name, url) in enumerate(content_urls):
                    worker = DownloadingWorker(
                        idx, session, url, section_name)
                    worker.emitter.data_signal.connect(self.update_data)
                    worker.emitter.exception_signal.connect(
                        self.handle_exception)
                    self.pool.start(worker)

                # Waiting for all worker threads to finish working
                while self.pool.activeThreadCount() != 0:
                    if self.shutdown:
                        # If GUI is closed while working, stops all workers
                        self.pool.clear()
                        self.pool.waitForDone()
                        return
                
                # Saving the youtube links in a .csv file
                with open(f'Output/{self.__course_id}-youtube-videos.csv', 'w') as f:
                    f.write('Section Name,Youtube Links\n')

                    for section_name, urls in self.youtube_urls:
                        section_name = section_name.replace(',', '')
                        if urls != []:
                            f.write(section_name)

                            for url in urls:
                                f.write(','+url+'\n')

                # Updating GUI
                self.str_signal.emit("Done!")
                self.down_done_signal.emit(1)
                print('Done!')

            except Exception as e:
                self.handle_exception(e)

            finally:
                end_time = time.time()
                print('Finished In: ', end_time-start_time)

    @QtCore.pyqtSlot()
    def parent_closing(self):
        """Method used by main thread to notify
        scrapper to stop everything
        """
        self.shutdown = True

    @QtCore.pyqtSlot(Exception)
    def handle_exception(self, e):
        """Handles every possible exception thrown by app

        Args:
            e (Exception): the exception object that was thrown
        """
        if not self.shutdown:
            self.shutdown = True

            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print(message)

            if isinstance(e, InvalidEmailPasswordException):
                self.str_signal.emit('Email or Password is Incorrect')

            elif isinstance(e, requests.ConnectionError):
                self.str_signal.emit(
                    'Check Your Internet Connection and Try Again')

            elif isinstance(e, CourseNotFoundException):
                self.str_signal.emit(
                    'Incorrect course name or You are not enrolled in the course.')

            else:
                # If the exception thrown is unknown, logging it in a file for debugging.
                logger = logger_setup('Scrapping Logger')
                self.str_signal.emit(
                    'An Unknown Fatal Error Occurred. Contact Developer.')
                logger.exception(type(e).__name__)

            self.down_done_signal.emit(0)

    @QtCore.pyqtSlot(tuple)
    def update_data(self, data):
        """Stores the data sent by worker threads and updates GUI

        Args:
            data (tuple): a tuple containing the index of the worker,
            the section name and youtube link
        """
        self.downloaded += 1

        # Storing the youtube link and section name
        self.youtube_urls[data[0]] = data[1:]

        # Updating GUI
        print(f'{self.downloaded}/{self.total_links} Done.')
        self.int_progress_signal.emit(self.downloaded)

    def _find_course_link(self, response):
        """Scraps the hyperlink of the pages that contain the
        youtube IDs

        Args:
            response (requests.models.Response): HTTP response object of the student dashboard

        Raises:
            CourseNotFoundException: If the user is not enrolled in the desired course
            or the course ID is invalid

        Returns:
            str: Hyperlink of the course
        """
        soup = BeautifulSoup(response.text, 'lxml')
        courses = soup.find('ul', class_='listing-courses')

        for course in courses.findAll('div', 'wrapper-course-details'):
            # Looking for the desired course in the student dashboard
            if course.find('div', class_='course-info').find('span', class_='info-course-id').text == self.__course_id:
                print('Course Found.')

                # Updating GUI
                self.str_signal.emit('Course Found')
                return self.url+course.h3.a['href']

        raise CourseNotFoundException(
            "Incorrect course name or You are not enrolled in the course.")

    def _find_course_content_url(self, response):
        """Creates a list of hyperlinks of pages that might have youtube videos

        Args:
            response (requests.models.Response): HTTP response object of the desired course

        Returns:
            list: A list of youtube links
        """
        completed_links = []

        soup = BeautifulSoup(response.text, 'lxml')
        content_block = soup.find('ol', id='course-outline-block-tree')

        for section in content_block.findAll('li', class_='outline-item'):
            sub_section = section.ol
            section_name = section.button.h3.text

            for links in sub_section.findAll('li'):
                completed_links.append((section_name, links.a['href']))

        print('Content Links Found.')

        return completed_links
