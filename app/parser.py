from typing import NamedTuple, List, Dict
import bs4
from bs4 import BeautifulSoup
import requests
import re
from time import sleep
from random import uniform

import json

from people import People, Person


class Wikipars():

    def __init__(self):
        self.people = People()

    def start(self, start_uri: str) -> None:
        number_person = self.people.count()
        start_person = Person(id=number_person, name='Name', category='Self', uri=start_uri, relation_id=-1)
        self.people.append(start_person)
        _n = 0
        while self.people.is_have:
            self.pause()
            self.parse()

            print('{} iteration'.format(_n))
            _n = _n + 1
            if _n == 1:
                break
        self.send()
    
    def send(self):
        with open('tmp.txt', 'w') as f:
            json.dump(self.people.json(), f, indent=4)

    def pause(self) -> None:
        sec = uniform(2, 10)
        sleep(sec)
    
    def parse(self) -> None:
        person = self.people.next()
        if not person.uri:
            return
        html = self.get_target_html(person.uri)

        soup = BeautifulSoup(html, 'lxml')
        name = soup.find('div', class_='mw-body', id='content').find('h1').text.strip()
        infobox = soup.find('table', class_='infobox')
        if not infobox:
            return

        categories = ["Отец", "Мать", "Супруга", "Супруг", "Дети"]
        for category in categories:
            if not infobox.find("th", text=category):
                continue
            _tags = infobox.find("th", text=category).parent.find_all('a')
            if not _tags:
                _tags = infobox.find("th", text=category).parent.find_all('span')
            if not _tags:
                continue

            self.extract_data(_tags, category)
    
    def extract_data(self, datatag: bs4.element.ResultSet, category: str) -> None:
        host = 'https://ru.wikipedia.org'
        for _tag in datatag:
            if _tag.has_attr('href') and not _tag.has_attr('title'):
                continue
            
            name = _tag.text.strip()            
            if self.check_name(name):
                continue
            uri = '{}{}'.format(host, _tag['href']) if _tag.has_attr('href') else ''

            number_person = self.people.count()
            by_person = self.people.current()
            person = Person(id=number_person, name=name, category=category, uri=uri, relation_id=by_person)
            self.people.append(person)
    
    def check_name(self, name:str) -> bool:
        pattern_square = '^\[.*'
        pattern_digit = '[\d]+'
        return re.match(pattern_square, name) or re.match(pattern_digit, name)

    def get_target_html(self, uri: str) -> str:
        r = requests.get(uri)
        return r.text
