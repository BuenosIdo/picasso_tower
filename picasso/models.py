from enum import Enum, IntEnum


class Floor(IntEnum):
    First = 1
    Second = 2
    Third = 3
    Fourth = 4
    Fifth = 5


class Color(Enum):
    Red = 'Red'
    Green = 'Green'
    Blue = 'Blue'
    Yellow = 'Yellow'
    Orange = 'Orange'


class Animal(Enum):
    Frog = 'Frog'
    Rabbit = 'Rabbit'
    Grasshopper = 'Grasshopper'
    Bird = 'Bird'
    Chicken = 'Chicken'


class AttributeType(Enum):
    Floor = 'Floor'
    Color = 'Color'
    Animal = 'Animal'
