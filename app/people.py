from typing import NamedTuple, List, Dict
import json

class Person(object):
    __slots__ = 'id', 'name', 'category', 'uri', 'relation_id', 'sex', 'born', 'deid', 'send', 'done'
    id: int
    name: str
    category: str
    uri: str
    relation_id: int
    sex: str
    born: str
    deid: str
    done: bool
    send: bool
    
    def __init__(self, id: int, name: str, uri: str, relation_id: int = -1, category: str = 'unknown', sex: str = 'unknown', born: str = 'unknown', deid: str = 'unknown'):
        self.id = id
        self.name = name
        self.category = category
        self.uri = uri
        self.relation_id = relation_id
        self.sex = sex
        self.born = born
        self.deid = deid
        self.done = False
        self.send = False


class People:
    
    def __init__(self):
        self._all = []
        self._ishave = False
        self._count = 0
        self._current = 0

    def append(self, person: Person) -> None:
        if not list(filter(lambda x: x['person'].uri == person.uri, self._all)):
            self._count += 1
            self._all.append({'person': person, 'done': False})            
        self._update_people()
    
    def is_have(self) -> bool:
        return _ishave
    
    def next(self) -> Person:
        next_data = next(filter(lambda x: not x['done'], self._all))
        next_data['done'] = True
        person = next_data['person']
        self._update_people()        
        self._current = person.id
        return person
    
    def _update_people(self) -> None:
        self._ishave = bool(list(filter(lambda x: not x['done'], self._all)))
    
    def current(self) -> int:
        return self._current

    def count(self) -> int:
        return self._count

    def json(self):
        return [{
                'id':x['person'].id, 
                'name':x['person'].name, 
                'category':x['person'].category, 
                'uri':x['person'].uri, 
                'relation_id':x['person'].relation_id,
                'sex':x['person'].sex,
                'born':x['person'].born,
                'deid':x['person'].deid
                } for x in self._all]