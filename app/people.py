from typing import NamedTuple, List, Dict
import json

class Person(NamedTuple):
    id: int
    name: str
    category: str
    uri: str
    relation_id: int
    # done: bool


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
                'relation_id':x['person'].relation_id
                } for x in self._all]