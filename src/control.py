from output import _Output
from user import _User
from operations import _Operations
from datahotel import DataHotel
from connection import _Connection
from hashlib_db import hash_string
from request import Request


class Control(object):
    """ Точка входа в БД """

    def __init__(self):
        self._sql = _Connection()
        self._request = None
        self._chat = None
        self._operation = _Operations(self._sql.conn, self._chat)
        self._hotels = None
        self._output = _Output(self._sql.conn)

    def set_request(self, request):
        self._request = request
        # self._chat = _User(request)
        # self._operation = _Operations(self._sql.conn, self._chat)

    def set_list_hotels(self, list_hotels):
        self._hotels = list_hotels

    # def exist_request(self, reaction):
    #     """
    #         Если запрос существует и reaction=True, то возвращаются данные последнего запроса.
    #         reaction=[True/False]
    #     """
    #     if self._operation.get_is_exist_request and reaction:
    #         return self._operation.select_exist_req()
    #     return None

    def get_info_hotel(self, name_hotel):
        """Вывести данные отеля"""
        return self._operation.get_info_hotel(hash_string(name_hotel))

    def is_exist_hotel(self, hotel):
        """ Существование отеля в бд без зависимости от id chat """
        return self._operation.is_exist_row("hotel", "name", "id_hotel", (hash_string(hotel),))

    def check_favorite(self, id_chat, name_hotel):
        """ Проверить в избранном отель по конкретному чату id_chat """
        return self._operation.is_exist_row("favorite_hotels", "*", "id_chat, id_hotel",
                                            (id_chat, hash_string(name_hotel)))

    def get_favorite_hotels(self, id_chat):
        """ Вернуть список data_hotels из избранного по id_chat """
        try:
            fetch_id_hotels = self._operation.select_in("favorite_hotels", "id_hotel", "id_chat",
                                                        (id_chat,))
            list_hotels = []
            [list_hotels.append(self._operation.get_info_hotel(i[0])) for i in fetch_id_hotels]
            return list_hotels
        except Exception as e:
            raise Exception(e.args[0])

    def add_favorite(self, id_chat, name_hotel):
        check = self.check_favorite(name_hotel)
        if not check:
            self._operation.insert_in("favorite_hotels", "id_chat, id_hotel",
                                      (id_chat, hash_string(name_hotel)))
            self._sql.conn.commit()
            return True
        return False

    def remove_favorite(self, id_chat, name_hotel):
        check = self.check_favorite(name_hotel)
        if check:
            self._operation.remove_in("favorite_hotels", "id_chat, id_hotel",
                                      (id_chat, hash_string(name_hotel)))
            self._sql.conn.commit()
            return True
        return False

    def start_transaction(self, request):
        """Начинает записывать в БД"""
        if self._hotels is None:
            raise Exception("Не установлен лист отелей")
        else:
            self._chat = _User(request)
            self._operation = _Operations(self._sql.conn, self._chat)
            self._operation.insert(self._hotels, request)

    def view_dynamic_of_prices(self, id_chat, name_hotel):
        return self._output.dynamics_of_prices(name_hotel, id_chat)

    def get_past_requests(self, id_chat, limit=10):
        """ Вернуть последние запросы пользователя(лимит по умолчанию 10) """
        fetch = self._operation.select_with_limit("history_requests", "input, href, date", "id_chat",
                                                  (id_chat,), "date", limit)
        if len(fetch) == 0:
            return None
        requests_of_user = []
        try:
            for row in fetch:
                param = row[0].split(' ')
                request = Request(id_chat, param[0], param[1], param[2], param[3],
                                  param[4], param[5], row[1], param[6] if len(param) == 7 else None)
                requests_of_user.append(request)
            return requests_of_user
        except Exception as err:
            raise Exception(err.args[0])

    def view_info_about_tables(self):
        """Выводит данные таблиц в консоль"""
        self._output.output_all()

#
# if __name__ == "__main__":
#     c = Control()
#     # name, star, rating, count_of_review, thumb_up, distance_from_center, link_on_hotel, price = None,
#     # amenities = None, image = None
#     c.set_list_hotels([DataHotel('Super1', 3, 9.7, 1000, 'Палец есть!', 3.7,'https://link1_on_hotel',6524,'басейн фен', 'https://link1.jpg'),
#                  DataHotel('Ast', 5, 9.7, 1000, 'Палец есть!', 3.7, 'https://link1_on_hotel',8124,'басейн фен', 'https://link1.jpg' )])
#     # c.set_request(Request(3, 'Мск', '20.01.2019', '24.01.2019', 1, 0, 1, 'http'))
#     # c.start_transaction()
#     d=c.view_dynamic_of_prices(3,'Super1')
#     c.view_info_about_tables()
#     print()
