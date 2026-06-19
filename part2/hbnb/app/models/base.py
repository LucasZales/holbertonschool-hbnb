'''Module containing HBNB Base Class'''

import uuid
from datetime import datetime


class Base:
    '''Base Class for HBNB'''

    def __init__(self):
        '''Initialise ID, Created_At and Updated_At'''
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str) -> None:
        '''Set object UUID'''
        if not isinstance(value, str):
            raise TypeError("id must be UUIDv4 of type str")
        if len(value) != 36:
            raise ValueError("id must be a valid UUID string")
        self.__id = value

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @created_at.setter
    def created_at(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError("created_at must be a datetime")
        self.__created_at = value

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError("updated_at must be a datetime")
        self.__updated_at = value

    def save(self) -> None:
        '''Update modification timestamp'''
        self.updated_at = datetime.now()

    def update(self, data: dict) -> None:
        '''Update object attributes'''
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
