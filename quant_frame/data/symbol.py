import logging
from enum import Enum


class AssetType(Enum):
    EQUITY = 0
    OPTION = 1
    FUTURE = 2
    CRYPTO = 3
    FOREX = 4


class Symbol:

    _name = ""
    marked = ""
    type = None
    min_quantity = 1

    def __init__(self, name):
        self.logger = logging.getLogger(__name__)
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    def __str__(self):
        return f"{self.type}:{self.marked}:{self._name}"

    # unique identifier for every symbol, used as key with hash
    @property
    def uid(self):
        return f"{self.type}{self.marked}{self._name}"

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, other):
        return self.uid == other.uid

    def __str__(self):
        return f"Symbol: {self.type}:{self.marked}:{self._name}"
