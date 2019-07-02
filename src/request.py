class Request:
    def __init__(self, chat_id, city, attrival_date, departure_date, n_adults, n_children, n_rooms,href=None, order_sorting=None):
        self._chat_id = chat_id
        self._city = city
        self._attrival_date = attrival_date
        self._departure_date = departure_date
        self._n_adults = n_adults
        self._n_children = n_children
        self._n_rooms = n_rooms
        self._order_sorting = order_sorting
        self._href = href

    @property
    def get_chat_id(self):
        """Получить id чата"""
        return self._chat_id

    @property
    def get_city(self):
        """Получить название города"""
        return self._city

    @property
    def get_attrival_date(self):
        """Получить дату заезда в отель"""
        return self._attrival_date

    @property
    def get_departure_date(self):
        """Получить дату выезда из отеля"""
        return self._departure_date

    @property
    def get_n_adults(self):
        """Получить количество взрослых"""
        return self._n_adults

    @property
    def get_n_children(self):
        """Получить количество детей"""
        return self._n_children

    @property
    def get_n_rooms(self):
        """Получить количество номеров"""
        return self._n_rooms

    @property
    def get_order_sorting(self):
        """Получить то как должны оортироваться отели"""
        return self._order_sorting

    @property
    def get_href(self):
        """Получить ссылку на страницу всех отелей"""
        return self._href