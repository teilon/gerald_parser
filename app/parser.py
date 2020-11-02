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
        start_person = Person(id=number_person, name='Name', uri=start_uri)
        self.people.append(start_person)
        _n = 0
        while self.people.is_have:
            self.pause()
            self.parse()

            print('{} iteration'.format(_n))
            _n = _n + 1
            if _n == 2:
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

        # person update
        name = soup.find('div', class_='mw-body', id='content').find('h1').text.strip()
        person.name = name
        years = self.get_years(soup)
        person.born = years['date_of_born']
        person.deid = years['date_of_deid']

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
        categories = {
            "Отец": 'parent', 
            "Мать": 'parent', 
            "Супруга": 'wifehusband', 
            "Супруг":'wifehusband', 
            "Дети": 'child'
        }
        for _tag in datatag:
            if _tag.has_attr('href') and not _tag.has_attr('title'):
                continue
            
            name = _tag.text.strip()            
            if self.check_name(name):
                continue
            uri = '{}{}'.format(host, _tag['href']) if _tag.has_attr('href') else ''
            sex = self.check_sex(category)

            number_person = self.people.count()
            by_person = self.people.current()
            person = Person(id=number_person, name=name, category=categories[category], uri=uri, relation_id=by_person, sex=sex)
            self.people.append(person)
    
    def check_name(self, name:str) -> bool:
        pattern_square = '^\[.*'
        pattern_digit = '[\d]+'
        return re.match(pattern_square, name) or re.match(pattern_digit, name)
    
    def check_sex(self, category):
        categories = {
            "Отец": 'male',
            "Мать": 'female',
            "Супруга": 'female',
            "Супруг":'male',
            "Дети": 'unknown'
        }
        return categories[category]
    
    def get_years(self, soup):
        a_links = soup.find('div', class_='mw-body', id='content').find('div', class_='mw-parser-output').find('p').find_all(string=True)
        pattern = r'\d{4}'
        _years = []
        for a_text in a_links:
            match = re.search(pattern, a_text)            
            if match:
                _years.append(match.group(0))
        
        if not _years:
            return None

        return {
            'date_of_born': min(_years),
            'date_of_deid': max(_years)
            }

    def get_target_html(self, uri: str) -> str:
        r = requests.get(uri)
        return r.text
