import sqlite3
from datetime import datetime as dt
from hashlib_db import hash_string
from datahotel import DataHotel


class _Operations(object):
    """Операции над БД: создание таблиц, вставка элементов, выборка"""

    def __init__(self, conn, input,href):
        self.conn = conn
        self.c = conn.cursor()
        self._create_table()
        self._input = input
        self._href=href

    @property
    def get_is_exist_request(self):
        return self.is_exist_row("history_requests", "id_request", "id_chat, input",
                                 (self._input.get_id_chat, self._input.get_input))

    def _create_table(self):
        # SQLite поддерживает только пять типов данных: null, integer, real, text и blob.
        create_chat = """CREATE TABLE if not exists chat(id_chat integer primary key)"""
        create_history = """CREATE TABLE if not exists history_requests(
                                                                id_request integer primary key autoincrement, 
                                                                id_chat integer not null, 
                                                                input text not null,
                                                                date text not null, 
                                                                href text,
                                                                FOREIGN KEY(id_chat) REFERENCES chat(id_chat)
                                                                )"""
        create_list_hotels = """CREATE TABLE if not exists list_hotels(
                                                        id_list integer primary key autoincrement,
                                                        id_request integer not null, 
                                                        id_hotel integer not null,
                                                        FOREIGN KEY(id_request) REFERENCES history_requests(id_request),
                                                        FOREIGN KEY(id_hotel) REFERENCES hotel(id_hotel)
                                                        )"""
        create_favorite_hotel = """CREATE TABLE if not exists favorite_hotels(
                                                                id_favorite integer primary key autoincrement,
                                                                id_chat integer not null, 
                                                                id_hotel integer not null,
                                                                FOREIGN KEY(id_chat) REFERENCES chat(id_chat),
                                                                FOREIGN KEY(id_hotel) REFERENCES hotel(id_hotel)
                                                                )"""
        create_hotel = """CREATE TABLE if not exists hotel(
                                            id_hotel integer primary key, 
                                            name text not null unique,
                                            star integer check(star<6), 
                                            rating real check(rating<=10),
                                            count_recom integer,
                                            thumb_up text check(thumb_up=='Палец есть!' or thumb_up=='Увы, пальца нет :('), 
                                            distance real,
                                            amenities text,
                                            image text,
                                            link text
                                            )"""
        create_prices = """CREATE TABLE if not exists prices(
                                                        id_price integer primary key autoincrement, 
                                                        id_hotel integer not null,
                                                        price integer,
                                                        date text not null,
                                                        FOREIGN KEY(id_hotel) REFERENCES hotel(id_hotel)
                                                        )"""
        # Создание таблиц
        self.c.execute(create_chat)
        self.c.execute(create_history)
        self.c.execute(create_hotel)
        self.c.execute(create_list_hotels)
        self.c.execute(create_favorite_hotel)
        self.c.execute(create_prices)
        self.conn.commit()

    def select_exist_req(self):
        id_request = self.select_in("history_requests", "id_request", " id_chat,input",
                                    (self._input.get_id_chat, self._input.get_input))
        id_hotels = self.select_in("list_hotels", "id_hotel", "id_request", (id_request[len(id_request) - 1]))
        list_ = []
        for row in id_hotels:
            list_.append(self.get_info_hotel(row[0]))
        return list_

    def get_info_hotel(self, id):
        hotel = self.select_in("hotel", "name,star,rating,count_recom,thumb_up,distance,amenities,image,link",
                               "id_hotel", (id,))

        for info in hotel:
            price = "SELECT price FROM prices WHERE id_hotel = %d ORDER BY id_price DESC LIMIT 1" % id
            self.c.execute(price)
            info = info + self.c.fetchone()
        # 0-name, 1-star, 2-rating, 3-count_of_review, 4-thumb_up, 5-distance_from_center,
        # 6-link_on_hotel, 7-price=None,8-amenities=None, 9-image=None
        data = DataHotel(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9])
        return data

    def insert(self, hotels):
        try:
            check = self.select_in("chat", "*", "id_chat", (self._input.get_id_chat,))
            if len(check) == 0:
                self.insert_in("chat", "id_chat", (self._input.get_id_chat,))
            date = dt.today().strftime('%Y-%m-%d %H:%M')
            self.insert_in("history_requests", "id_chat, input, date, href",
                           (self._input.get_id_chat, self._input.get_input, date, self._href))
            id_request = self.c.lastrowid
            for i in hotels:
                hash = hash_string(i.get_name)
                hotel = "SELECT id_hotel FROM hotel WHERE name = '%s'" % i.get_name
                self.c.execute(hotel)
                id_hotel = self.c.fetchone()
                if id_hotel is None:
                    self.insert_in("hotel",
                                   "id_hotel, name,star,rating,count_recom,thumb_up,distance,amenities,image,link",
                                   (hash, i.get_name, i.get_star, i.get_rating,
                                    i.get_count_of_review, i.get_thumb_up, i.get_distance_from_center,
                                    i.get_amenities, i.get_image, i.get_link_on_hotel))
                    id_hotel = self.c.lastrowid
                self.insert_in("prices", "id_hotel,price,date",
                               (hash, i.get_price, date))
                self.insert_in("list_hotels", "id_request, id_hotel",
                               (id_request, hash))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception('SQLite error, method - insert: ', e.args[0])

    def insert_in(self, table, columns_str, tuple):
        try:
            values = _Operations._get_count_values(columns_str)
            sql_insert = "INSERT INTO " + str(table) + " (" + str(columns_str) + ") VALUES " + str(values)
            self.c.execute(sql_insert, tuple)
        except Exception as e:
            raise Exception("Возможно ожидается '(переменная,)' - %s" % e.args[0])

    @staticmethod
    def _get_count_values(columns_str):
        count_clm = columns_str.split(',').__len__()
        values = "("
        for count in range(0, count_clm):
            if count == count_clm - 1:
                values += "?)"
                break
            values += "?,"
        return values

    def is_exist_row(self, table, columns_for_select, where=None, tuple=None):
        rows = self.select_in(table, columns_for_select, where, tuple)
        if len(rows) == 0:
            return False
        return True

    def select_in(self, table, columns, where=None, tuple=None):
        """tuple=(int,string) если 2 агрумента, либо (int,int)"""
        try:
            request = "SELECT " + str(columns) + " FROM " + str(table)
            if len(tuple) == 1 and where is not None:
                request += " WHERE " + str(where) + " = (?)"
            elif len(tuple) == 2:
                list = where.split(',')
                request += " WHERE {} = {} AND {} = {}" \
                    .format(list[0], tuple[0], list[1], tuple[1] if not isinstance(tuple[1], str) else "'{}'"
                            .format(tuple[1]))
                self.c.execute(request)
                return self.c.fetchall()
            self.c.execute(request, tuple)
            fetch = self.c.fetchall()
            return fetch
        except Exception as err:
            raise Exception(err.args[0])

    def select_with_limit(self, table, columns, where=None, tuple=None, orderby=None, limit=1):
        if orderby is None:
            return self.select_in(table, columns, where, tuple)
        request = "SELECT " + str(columns) + " FROM " + str(table) + " WHERE " + str(where) \
                  + " = (?)" + " ORDER BY " + str(orderby) + " DESC LIMIT %d" % limit
        self.c.execute(request, tuple)
        fetch = self.c.fetchall()
        return fetch

    def remove_in(self, table, columns, what):
        try:
            request = "DELETE FROM " + str(table)
            list_clm = columns.split(',')
            len_clm = list_clm.__len__()
            if len_clm == 1:
                request += " WHERE " + str(columns) + " = {}" \
                    .format(what if not isinstance(what, str) else "'{}'".format(what))
            elif len_clm == 2:
                request += " WHERE " + str(list_clm[0]) + " = {}".format(what[0]) \
                           + " AND " + str(list_clm[1]) \
                           + " = {}".format(what[1])
            else:
                raise
            self.c.execute("vacuum")
            self.c.execute(request)

            return True
        except Exception as err:
            return False
