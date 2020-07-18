
from enum import Enum


token = '833759691:AAFUGJQ-BYbLohyLxzkXfKe9YRdQG6pebzU'


db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_CHOICE = "1"  # Поиск видео
    S_LAST_SEARCH = "2"  #Последний поиск
    S_TRENDING = "3"  #Видео в тренде