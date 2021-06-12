from bs4 import BeautifulSoup
from PyQt5 import QtCore
import requests
import html

from json import loads as jsonloads
from os import path
import traceback
import sys


class CourseNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidEmailPasswordException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Scrapper(QtCore.QThread):
    int_progress_signal = QtCore.pyqtSignal(int)
    int_progress_max_signal = QtCore.pyqtSignal(int)
    str_signal = QtCore.pyqtSignal(str)
    down_done_signal = QtCore.pyqtSignal()

    def __init__(self, email, pass_, course_id):
        super().__init__()

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
        self.str_signal.emit('Logging In')
        print('Loggin In.')
        with requests.Session() as session:
            csrf_token = session.get(self.url).cookies['csrftoken']

            HEADERS = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                'Host': 'bux.bracu.ac.bd',
                'Origin': self.url,
                'Referer': 'https://bux.bracu.ac.bd/login?next=%2F',
                'X-CSRFToken': csrf_token
            }
            
            login_payload = {'email': self.__email, 'password': self.__pass_}

            login_req = session.post(self.login_route,headers=HEADERS, data=login_payload)

            if not login_req.ok:
                try:
                    raise InvalidEmailPasswordException("Email or Password is Incorrect")
                except:
                    traceback.print_exc()
                    if __name__ == '__main__':
                        sys.exit()
                    else:
                        self.str_signal.emit('Email or Password is Incorrect')
                        self.down_done_signal.emit()
                        self.terminate()
                        self.wait()
            
            self.str_signal.emit('Successfully Logged In')
            print('Successfully Logged In.')

            response = session.get(self.url+self.request_url)

            course = session.get(self._find_course_link(response))

            content_urls = self._find_course_content_url(course)

            self.total_links = len(content_urls)
            
            self.int_progress_max_signal.emit(self.total_links)
            self.str_signal.emit('Downloading')
            print('Downloading.')

            for section_name, url in content_urls:
                content_response = session.get(url)

                youtube_url_list = self._find_youtube_link(content_response.text)

                if youtube_url_list != []:
                    self.youtube_urls.append((section_name, youtube_url_list))
                
                self.downloaded += 1
                print(f'{self.downloaded}/{self.total_links} Done.')
                self.int_progress_signal.emit(self.downloaded)
            
            with open(f'Output/{self.__course_id}-youtube-videos.csv', 'w') as f:
                f.write('Section Name;Youtube Links\n')

                for section_name, url_list in self.youtube_urls:
                    f.write(section_name)

                    for url in url_list:
                        f.write(';'+url+'\n')
                        
            self.str_signal.emit("Done!")
            self.down_done_signal.emit()
            print('Done!')
    

    def _find_course_link(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        courses = soup.find('ul', class_='listing-courses')

        for course in courses.findAll('div', 'wrapper-course-details'):
            if course.find('div', class_='course-info').find('span', class_='info-course-id').text == self.__course_id:
                print('Course Found.')
                self.str_signal.emit('Course Found')
                return self.url+course.h3.a['href']
         
        try:
            raise CourseNotFoundException("Incorrect course name or You are not enrolled in the course.")
        except:
            traceback.print_exc()
            if __name__ == '__main__':
                sys.exit()
            else:
                self.str_signal.emit('Incorrect course name or You are not enrolled in the course.')
                self.down_done_signal.emit()
                self.terminate()
                self.wait()


    def _find_course_content_url(self, response):
        completed_links = []

        soup = BeautifulSoup(response.text, 'lxml')
        content_block = soup.find('ol', id='course-outline-block-tree')

        for section in content_block.findAll('li', class_='outline-item'):
            sub_section = section.ol
            section_name = section.button.h3.text

            for links in sub_section.findAll('li'):
                completed_links.append((section_name,links.a['href']))
        
        print('Content Links Found.')

        return completed_links


    def _find_youtube_link(self, html_text):
        youtube_urls = []
        base_youtube_url = 'https://www.youtube.com/watch?v='

        html_text = html.unescape(html_text)

        soup = BeautifulSoup(html_text, 'lxml')

        for divs in soup.findAll('div', class_='video closed'):
            try:
                youtube_urls.append(base_youtube_url+self._find_youtube_id(divs['data-metadata']))
            except:
                pass
        
        return youtube_urls


    def _find_youtube_id(self, s):
        parsed_json = jsonloads(s)
        id_ = parsed_json['streams'].split(':')[1]
        return id_


if __name__ == '__main__':
    email = input("Enter buX Email: ")
    pass_ = input("Enter buX Password: ")
    id_ = input("Enter Course ID of the Course You want to Scrap: ")

    scrapper = Scrapper(email, pass_, id_)
    scrapper.run()
