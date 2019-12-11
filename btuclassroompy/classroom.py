import re
import requests
from bs4 import BeautifulSoup

x = lambda x: re.sub('\s+', ' ', x).strip()

class Message:

    message_id = 1

    def __init__(self, classroom_id, sender, title, date):
        self.classroom_id = classroom_id
        self.id = Message.message_id
        self.sender = sender
        self.title = title
        self.date = date

        Message.message_id += 1

    def __repr__(self):
        return f'[{self.id}] | {self.sender} | {self.title} | {self.date}'

    @classmethod
    def reset(cls):
        cls.message_id = 1

class Course:

    course_id = 1

    def __init__(self, code, course_url, course_name, total_points, student_credits, total_credits):
        self.id = Course.course_id
        self.code = code
        self.course_url = course_url
        self.course_name = course_name
        self.total_points = total_points
        self.student_credits = student_credits
        self.total_credits = total_credits
        self.course_points = []

        Course.course_id += 1

    def get_course_points(self, classroom):
        s = classroom._login()
        course_id = self.course_url.split("/")[-1]
        r = s.get(f"https://classroom.btu.edu.ge/ge/student/me/course/scores/{course_id}/32")
        if len(self.course_points) != 0:
            self.course_points.clear()
        soup = BeautifulSoup(r.text, 'html.parser')
        for i in soup.find_all('tr'):
            try:
                criterium = x(i.find_all('td')[0].text)
                student_points = x(i.find_all('td')[1].text)
                self.course_points.append(CoursePoints(criterium, student_points))
            except IndexError:
                pass
        return ''



    def __repr__(self):
        return f'[{self.id}] | {self.code} | {self.course_name} | {self.total_points} | {self.student_credits} | {self.total_credits}'

    @classmethod
    def reset(cls):
        cls.course_id = 1



class CoursePoints:

    def __init__(self, criterium, student_points):
        self.criterium = criterium
        self.student_points = student_points

    def __repr__(self):
        return f'[+] {self.criterium} | {self.student_points}'



class Classroom:

    login_page_url = "https://classroom.btu.edu.ge/ge/login"
    login_request_url = "https://classroom.btu.edu.ge/ge/login/trylogin"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.messages = []
        self.courses = []

    def _login(self):
        data = {
            'username':self.username,
            'password':self.password
        }
        s = requests.Session()
        r = s.post(self.login_request_url, data=data)
        return s

    def get_balance(self):
        s = self._login()
        r = s.get("https://classroom.btu.edu.ge/ge/student/me/courses")
        soup = BeautifulSoup(r.text, 'html.parser')
        balance = soup.find_all('span', class_='badge')[0].getText().lstrip()
        return balance

    def _get_messages(self):
        if len(self.messages) != 0:
            self.messages.clear()
            Message.reset()
        s = self._login()
        r = s.get("https://classroom.btu.edu.ge/ge/messages")
        soup = BeautifulSoup(r.text, 'html.parser')
        for i in soup.find_all('tr'):
            try:
                classroom_id = i.find_all('td')[0].find('input').get('value')
                sender = x(i.find_all('td')[1].text)
                title = i.find_all('td')[2].text
                date = i.find_all('td')[3].text
                self.messages.append(Message(classroom_id, sender, title, date))
            except IndexError:
                pass
        return self.messages

    def list_messages(self):
        print('''
-----------------------------------
| გამომგზავნი | სათაური | თარიღი  |
___________________________________
''')
        self._get_messages()
        for message in self.messages:
            print(message)
        return ''

    def read_message(self, message_id):
        self._get_messages()
        s = self._login()
        message = [i for i in self.messages if str(i.id) == message_id][0]
        r = s.get(f"https://classroom.btu.edu.ge/ge/messages/view/{message.classroom_id}/32")
        soup = BeautifulSoup(r.text, 'html.parser')
        message = soup.find('div', id="message_body").text
        return message

    def _get_courses(self):
        if len(self.courses) != 0:
            self.courses.clear()
            Course.reset()
        s = self._login()
        r = s.get("https://classroom.btu.edu.ge/ge/student/me/courses")
        soup = BeautifulSoup(r.text, 'html.parser')
        for i in soup.find_all('tr'):
            try:
                code = x(i.find_all('td')[1].text)
                course_url = i.find_all('td')[2].find('a')['href']
                course_name = x(i.find_all('td')[2].text)
                total_points = x(i.find_all('td')[3].text)
                student_credits = x(i.find_all('td')[4].text)
                total_credits = x(i.find_all('td')[5].text)
                self.courses.append(Course(code, course_url, course_name, total_points, student_credits, total_credits))
            except Exception:
                pass
        return self.courses


    def list_courses(self):
        print('''
-------------------------------------------------------------------------------------
| ID | კოდი | კურსის დასახელება | დაგროვებული ქულები | დაგროვებული კრედიტი | კრედიტი |
_____________________________________________________________________________________
''')
        self._get_courses()
        for i in self.courses:
            print(i)
        return ''


    def list_course_points(self, course_id, classroom):
        print('''
----------------------------------
| შეფასების კრიტერიუმი | შეფასება |
_________________________________
''')
        self._get_courses()
        course = [i for i in self.courses if str(i.id) == course_id][0]
        course.get_course_points(classroom)
        for i in course.course_points:
            print(i)
        return ''
