from typing import NamedTuple, List, Dict
import bs4
from bs4 import BeautifulSoup
import requests
import re
from time import sleep
from random import uniform

target_uri = 'https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BB%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D1%81%D0%BA%D0%B0%D1%8F,_%D0%9C%D0%B0%D1%80%D0%B8%D1%8F_%D0%98%D0%BB%D1%8C%D0%B8%D0%BD%D0%B8%D1%87%D0%BD%D0%B0'

class Wikipars():
    links = []

    def start(self) -> list:
        self.init_start()
        true_links = list(filter(lambda x: not x['done'], self.links))
        while true_links:
            sec = uniform(2, 10)
            sleep(sec)

            self.parse()
            true_links = list(filter(lambda x: not x['done'], self.links))
    
    def add_link(self, link: Dict) -> None:
        if not list(filter(lambda x: x['uri'] == link['uri'], self.links)):
            self.links.append(link)

            # with open("links.txt", "a") as f:
            #     f.write('name: {}\nuri: {}\n***\n'.format(link['name'], link['uri']))

    def init_start(self) -> None:
        first_link = {
            'uri': target_uri, 
            'name': 'first',
            'done': False
        }
        self.add_link(first_link)
    
    def parse(self) -> None:
        target_link = next(filter(lambda x: not x['done'], self.links))
        target_link['done'] = True

        uri = target_link['uri']
        if uri:
            self.parse_data(uri)
    
    def get_target_html(self, uri: str) -> str:
        r = requests.get(uri)
        return r.text
    
    def parse_data(self, uri: str) -> None:
        html = self.get_target_html(uri)
        soup = BeautifulSoup(html, 'lxml')

        name = soup.find('div', class_='mw-body', id='content').find('h1').text.strip()
        infobox = soup.find('table', class_='infobox')

        if not infobox:
            return

        cats = ["Отец", "Мать", ["Супруга", "Супруг"], "Дети"]
        for cat in cats:
            if not infobox.find("th", text=cat):
                continue
            _tags = infobox.find("th", text=cat).parent.find_all('a')
            if not _tags:
                _tags = infobox.find("th", text=cat).parent.find_all('span')
            if not _tags:
                continue

            self.extract_data(_tags, cat)
    
    def extract_data(self, datatag: bs4.element.ResultSet, cat: str) -> None:
        host = 'https://ru.wikipedia.org'
        for _tag in datatag:
            if _tag.has_attr('href') and not _tag.has_attr('title'):
                continue
            
            name = _tag.text.strip()            
            if self.check_name(name):
                continue
            uri = '{}{}'.format(host, _tag['href']) if _tag.has_attr('href') else ''

            link = {
                'uri': uri,
                'name': name,
                'done': False                
            }
            self.add_link(link)
    
    def check_name(self, name:str) -> bool:
        pattern_square = '^\[.*'
        pattern_digit = '[\d]+'
        return re.match(pattern_square, name) or re.match(pattern_digit, name)
