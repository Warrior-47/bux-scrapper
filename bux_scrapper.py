from json import loads as jsonloads
from bs4 import BeautifulSoup
from os import path
import requests
import pickle
import html

class Scrapper:

    def __init__(self):
        self.url = 'https://bux.bracu.ac.bd'
        self.login_route = 'https://bux.bracu.ac.bd/user_api/v1/account/login_session/'
        self.request_url = '/dashboard'
        self.youtube_urls = []
    

    def start_scrapping(self, course_id):
        COOKIES_PATH = 'cookie_info.pickled'

        with requests.Session() as session:
            if path.exists(COOKIES_PATH):
                with open(COOKIES_PATH, 'rb') as f:
                    session.cookies.update(pickle.load(f))
                
            response = session.get(self.url+self.request_url)

            if response.history != []:
                session.cookies.clear()

                csrf_token = session.get(self.url).cookies['csrftoken']

                HEADERS = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
                    'Host': 'bux.bracu.ac.bd',
                    'Origin': self.url,
                    'Referer': 'https://bux.bracu.ac.bd/login?next=%2F',
                    'X-CSRFToken': csrf_token
                }
                
                login_payload = {'email': input("Enter your buX Email: "), 'password': input('Enter your buX Password: ')}

                login_req = session.post(self.login_route,headers=HEADERS, data=login_payload)
                
                with open(COOKIES_PATH, 'wb') as f:
                    pickle.dump(session.cookies, f)
            
            response = session.get(self.url+self.request_url)

            course = session.get(self.find_course_link(response, course_id))

            content_urls = self.find_course_content_url(course)


            for idx, (section_name, url) in enumerate(content_urls):
                content_response = session.get(url)
                youtube_url_list = self.find_youtube_link(content_response.text)
                if youtube_url_list != []:
                    self.youtube_urls.append((section_name,youtube_url_list))
                
                print(f'{idx+1}/{len(content_urls)} Done.')
            

            with open(f'{course_id}-youtube-videos.csv', 'w') as f:
                f.write('Section Name;Youtube Links\n')
                for section_name, url_list in self.youtube_urls:
                    f.write(section_name)
                    for url in url_list:
                        f.write(';'+url+'\n')
    

    def find_course_link(self, response, course_id):
        soup = BeautifulSoup(response.text, 'lxml')
        courses = soup.find('ul', class_='listing-courses')

        for course in courses.findAll('div', 'wrapper-course-details'):
            if course.find('div', class_='course-info').find('span', class_='info-course-id').text == course_id:
                print('Course Found.')
                return self.url+course.h3.a['href']
        
        raise CourseNotFoundException("Incorrect course name or You are not enrolled in the course.")


    def find_course_content_url(self, response):
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


    def find_youtube_link(self, html_text):
        youtube_urls = []
        base_youtube_url = 'https://www.youtube.com/watch?v='

        html_text = html.unescape(html_text)

        soup = BeautifulSoup(html_text, 'lxml')

        for divs in soup.findAll('div', class_='video closed'):
            try:
                youtube_urls.append(base_youtube_url+self.find_youtube_id(divs['data-metadata']))
            except:
                pass
        
        return youtube_urls


    def find_youtube_id(self, s):
        parsed_json = jsonloads(s)
        id_ = parsed_json['streams'].split(':')[1]
        return id_


class CourseNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.start_scrapping(input("Enter Course ID of the Course You want to Scrap: "))