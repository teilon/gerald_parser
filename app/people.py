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
    
    def __init__(self, id: int, name: str, uri: str, relation_id: int = -1, category: str = 'unknown', sex: str = 'unknown', born: str = 'unknown', deid: str = 'unknown') -> None:
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
    
    def json(self):
        # self.send = True
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'uri': self.uri,
            'relation_id': self.relation_id,
            'sex': self.sex,
            'born': self.born,
            'deid': self.deid,

            'done': self.done,
            'send': self.send
            }


class People:
    count_of_ready = 20
    
    def __init__(self):
        self._all = []
        self._ishave = False
        self._tosend = False
        self._count = 0
        self._current = 0

    def append(self, person: Person) -> None:
        if not list(filter(lambda x: x.uri == person.uri, self._all)) or person.uri == '':
            self._count += 1
            self._all.append(person)
        else:
            old_person = list(filter(lambda x: x.uri == person.uri, self._all))[0]
            if old_person.sex != person.sex and person.sex != 'unknown':
                old_person.sex = person.sex
                old_person.send = False
        self._update_people()
    
    def next(self) -> Person:
        person = next(filter(lambda x: not x.done, self._all))
        person.done = True
        self._update_people()        
        self._current = person.id
        return person
    
    def _update_people(self) -> None:
        self._ishave = bool(list(filter(lambda x: not x.done, self._all)))
        self._tosend = len(list(filter(lambda x: not x.send, self._all))) > People.count_of_ready
    
    def ready_tosend(self) -> bool:
        return self._tosend
    
    def is_have(self) -> bool:
        return self._ishave
    
    def current(self) -> int:
        return self._current

    def count(self) -> int:
        return self._count

    def json(self):
        return [x.json() for x in self._all]

    def json_tosend(self):
        self._tosend = False

        ready_list = list(filter(lambda x: not x.send, self._all))
        ready_json = [x.json() for x in ready_list]

        self._all = list(map(self._, self._all))
        # self._all = list(map(lambda x: x.send = True, self._all))

        return ready_json

    def _(self, person):
        person.send = True
        return person 