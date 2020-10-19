from typing import NamedTuple, List, Dict
import bs4
from bs4 import BeautifulSoup
import requests
import re
from time import sleep

from pprint import pprint

# target_uri = 'https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B5%D0%B9_%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D0%B8%D1%87'
target_uri = 'https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BB%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D1%81%D0%BA%D0%B0%D1%8F,_%D0%9C%D0%B0%D1%80%D0%B8%D1%8F_%D0%98%D0%BB%D1%8C%D0%B8%D0%BD%D0%B8%D1%87%D0%BD%D0%B0'
target_links = []
people = []


class Wikipars():
    links = []

    def start(self) -> list:
        self.init_start()
        true_links = list(filter(lambda x: not x['done'], self.links))
        n = 0
        while true_links:
            sleep(2)
            pprint('*** {} ***'.format(n))
            n += 1

            self.parse()
            true_links = list(filter(lambda x: not x['done'], self.links))
    
    def add_link(self, link: Dict) -> None:
        # for l in self.links:
        if not list(filter(lambda x: x['uri'] == link['uri'], self.links)):
            self.links.append(link)

            with open("links.txt", "a") as f:
                f.write('name: {}\nuri: {}\n***\n'.format(link['name'], link['uri']))

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
        pprint(uri)
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

    

    




def start() -> List:
    init_target_links()
    n = 0

    while exists_target_links():
        sleep(2)
        pprint('*** {} ***'.format(n))
        n += 1
        # if n == 13:
        #     break

        data = parse()
        if not data:
            continue            

        update_people(data['person'])
        update_target_links(data['relations'])
    
    pprint('target links: {}'.format(len(target_links)))
    pprint('people: {}'.format(len(people)))

    return people 

def init_target_links() -> None:
    start_item = get_start_item()
    target_links.append(start_item)

def update_people(person) -> Dict:
    people.append(person)

def update_target_links(links) -> None: # : list
    _links = []
    for link in links:
        if filter(lambda x: x != link, _links):
            _links.append({'link': link, 'done': False})
    target_links.extend(_links)

def get_start_item() -> Dict:
    return {
        'link': {
            'uri': target_uri, 
            'name': 'first'
            }, 
        'done': False
        }

def exists_target_links() -> bool:
    # link = filter(lambda where done is False).first   FIRST
    link = list(filter(lambda x: x['done'] == False, target_links))
    if link:
        return True
    return False

def get_next_link() -> Dict:
    link = next(filter(lambda x: x['done'] == False, target_links))
    if link:
        link['done'] = True
        pprint(link['link']['uri'])
        return link['link']
    return None

def parse() -> Dict:
    target_link = get_next_link()
    # _name = target_link['name']
    # if _name:
    #     pprint('select {}'.format(_name))

    target_uri = target_link['uri']
    if target_uri:
        soup = get_soup(target_uri)
        data = get_data(soup)

        if not data:
            return None
        
        return data
    return None

def get_soup(uri: str) -> BeautifulSoup:
    target_html = get_target_html(uri)
    soup = BeautifulSoup(target_html, 'lxml')
    return soup

def get_target_html(uri: str) -> str:
    r = requests.get(uri)
    return r.text

def get_data(soup: BeautifulSoup) -> Dict:
    # AttributeError: 'NoneType' object has no attribute 'find'
    name = soup.find('div', class_='mw-body', id='content').find('h1').text.strip()
    infobox = soup.find('table', class_='infobox')

    if not infobox:
        return None

    cats = ["Отец", "Мать", ["Супруга", "Супруг"], "Дети"]
    # cats = ["Отец", "Мать", ["Супруга", "Супруг"]]
    # cats = [["Отец", "Мать"], ["Супруга", "Супруг"]]
    # cats = [["Отец", "Мать"], ["Супруга", "Супруг"], "Дети"]
    relations = []
    for cat in cats:
        _tag = info_tag(infobox, cat, 'a')
        if not _tag:
            _tag = info_tag(infobox, cat, 'span')

        if not _tag:
            continue

        _ = extract_data(_tag, cat)
        if not _:
            continue

        relations.extend(_)

    return {
        'person': {
            'name': name,
            "parent_id": 0,
            "child_id": 0
            },
        'relations': relations
        }

def info_tag(infobox: bs4.element.ResultSet, cat: str, tag: str) -> bs4.element.ResultSet:
    cat_tag = infobox.find("th", text=cat)
    if cat_tag:
        return infobox.find("th", text=cat).parent.find_all(tag)
    return None

    #return tag.has_attr('class') and not tag.has_attr('id')

def extract_data(datatag: bs4.element.ResultSet, cat: str): # -> List
    host = 'https://ru.wikipedia.org'
    data = []
    for _tag in datatag:


        if _tag.has_attr('href') and not _tag.has_attr('title'):
            continue

        _name = _tag.text.strip()
        
        pattern = '^\[.*'
        x = re.match(pattern, _name)
        if x:
            return None

        pattern = '[\d]+'
        x = re.match(pattern, _name)
        if x:
            return None

        _ = {
            'relation': cat,
            'name': _name,
            'uri': '{}{}'.format(host, _tag['href']) if _tag.has_attr('href') else ''
        }
        data.append(_)        
    return data
