import types
from unittest import TestCase
from threading import Lock
from typing import TYPE_CHECKING, Annotated, get_args, get_type_hints, Generic
import inspect


class Singleton(type):
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBSession(metaclass=Singleton):

    def __init__(self, db_uri):
        self.db_uri = db_uri
        self._is_connected = False

    def connect(self):
        self._is_connected = True

    @property
    def is_connected(self):
        return self._is_connected


class TestSingleton(TestCase):
    def test_metaclass(self):
        db1 = DBSession('sqlite:///:memory:')
        db2 = DBSession('mongodb://localhost:27017/users')
        print(f"{db1.db_uri}  {db1.is_connected}")
        print(f"{db2.db_uri}  {db2.is_connected}")

    def test_foo(self):
        print(TYPE_CHECKING)
        print(foo.__annotations__)
        for name, ano in foo.__annotations__.items():
            print(f"Name: {name}, Annotation: {ano}")
            for index, arg in enumerate(get_args(ano)):
                print(f"\tIndex: {index}, Value: {arg}")

        params = list(inspect.signature(foo).parameters.values())
        annotated_params = [p for p in params if p.annotation != p.empty]
        print(f"Params: {annotated_params}")
        hints = get_type_hints(foo)
        print(f"Hints: {hints}")
        foo(1, 2, [3])


class FromOptions:
    def __init__(self, name: str):
        self.name = name


class Session:
    pass


def foo(a: 'int', b: 5 + 6, c: Annotated[list, FromOptions("local"), Session]) -> max(2, 9):
    print(a)
    print(b)
    print(c)
