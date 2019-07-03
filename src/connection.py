import sqlite3


class _Connection(object):
    """Подключение БД"""

    def __init__(self):
        self.conn = sqlite3.connect("test_booka01.db")  # или :memory: чтобы сохранить в RAM
        self.cursor = self.conn.cursor()
