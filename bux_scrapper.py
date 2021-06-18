from PyQt5.QtCore import QThreadPool
from bs4 import BeautifulSoup
from PyQt5 import QtCore
import requests
import html

from json import loads as jsonloads
import logging
import time


class CourseNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidEmailPasswordException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WorkerSignals(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(tuple)
    exception_signal = QtCore.pyqtSignal(Exception)


class DownloadingWorker(QtCore.QRunnable):

    def __init__(self, index, session, url, section_name):
        super().__init__()
        self.index = index
        self.session = session
        self.url = url
        self.section_name = section_name
        self.emitter = WorkerSignals()

    def run(self):
        try:
            content_response = self.session.get(self.url)

            youtube_url_list = self._find_youtube_link(
                content_response.text)

            self.emitter.data_signal.emit(
                (self.index, self.section_name, youtube_url_list))

        except Exception as e:
            self.emitter.exception_signal.emit(e)

    def _find_youtube_link(self, html_text):
        youtube_urls = []
        base_youtube_url = 'https://www.youtube.com/watch?v='

        html_text = html.unescape(html_text)

        soup = BeautifulSoup(html_text, 'lxml')

        for divs in soup.findAll('div', class_='video closed'):
            try:
                youtube_urls.append(
                    base_youtube_url+self._find_youtube_id(divs['data-metadata']))
            except:
                pass

        return youtube_urls

    def _find_youtube_id(self, s):
        parsed_json = jsonloads(s)
        id_ = parsed_json['streams'].split(':')[1]
        return id_


class Scrapper(QtCore.QThread):
    int_progress_signal = QtCore.pyqtSignal(int)
    int_progress_max_signal = QtCore.pyqtSignal(int)
    str_signal = QtCore.pyqtSignal(str)
    down_done_signal = QtCore.pyqtSignal()

    def __init__(self, email, pass_, course_id):
        super().__init__()
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(4)
        self.shutdown = False

        self.url = 'https://bux.bracu.ac.bd'
        self.login_route = 'https://bux.bracu.ac.bd/user_api/v1/account/login_session/'
        self.request_url = '/dashboard'
        self.youtube_urls = []

        self.total_links = 0
        self.downloaded = 0

        self.__email = email
        self.__pass_ = pass_
        self.__course_id = course_id

    def run(self):
        start_time = time.time()

        self.str_signal.emit('Logging In')
        print('Loggin In.')

        with requests.Session() as session:
            try:
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
                    raise InvalidEmailPasswordException(
                        "Email or Password is Incorrect")

                self.str_signal.emit('Successfully Logged In')
                print('Successfully Logged In.')

                response = session.get(self.url+self.request_url)

                course_link = self._find_course_link(response)

                course = session.get(course_link)

                content_urls = self._find_course_content_url(course)

                self.total_links = len(content_urls)
                self.youtube_urls = [0] * self.total_links

                self.int_progress_max_signal.emit(self.total_links)
                self.str_signal.emit('Downloading')
                print('Downloading.')

                for idx, (section_name, url) in enumerate(content_urls):
                    worker = DownloadingWorker(
                        idx, session, url, section_name)
                    worker.emitter.data_signal.connect(self.update_data)
                    worker.emitter.exception_signal.connect(
                        self.handle_exception)
                    self.pool.start(worker)

                while self.pool.activeThreadCount() != 0:
                    if self.shutdown:
                        self.pool.clear()
                        self.pool.waitForDone()
                        return

                with open(f'Output/{self.__course_id}-youtube-videos.csv', 'w') as f:
                    f.write('Section Name,Youtube Links\n')

                    for section_name, urls in self.youtube_urls:
                        if urls != []:
                            f.write(section_name)

                            for url in urls:
                                f.write(','+url+'\n')

                self.str_signal.emit("Done!")
                self.down_done_signal.emit()
                print('Done!')

            except Exception as e:
                self.handle_exception(e)

            finally:
                end_time = time.time()
                print('Finished In: ', end_time-start_time)

    @QtCore.pyqtSlot()
    def parent_closing(self):
        self.shutdown = True

    @QtCore.pyqtSlot(Exception)
    def handle_exception(self, e):
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
                logger = logger_setup()
                self.str_signal.emit(
                    'An Unknown Fatal Error Occurred. Contact Developer.')
                logger.exception(type(e).__name__)

            self.down_done_signal.emit()

    @QtCore.pyqtSlot(tuple)
    def update_data(self, data):
        self.downloaded += 1
        self.youtube_urls[data[0]] = data[1:]
        print(f'{self.downloaded}/{self.total_links} Done.')
        self.int_progress_signal.emit(self.downloaded)

    def _find_course_link(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        courses = soup.find('ul', class_='listing-courses')

        for course in courses.findAll('div', 'wrapper-course-details'):
            if course.find('div', class_='course-info').find('span', class_='info-course-id').text == self.__course_id:
                print('Course Found.')
                self.str_signal.emit('Course Found')
                return self.url+course.h3.a['href']

        raise CourseNotFoundException(
            "Incorrect course name or You are not enrolled in the course.")

    def _find_course_content_url(self, response):
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


def logger_setup():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '\n%(asctime)s : %(levelname)s : Thread = %(threadName)s : %(message)s')

    handler = logging.FileHandler('errors.log')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
