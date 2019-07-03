class _User(object):
    """Сведения о запросе"""

    def __init__(self, request):
        self._request = request
        input = self._get_string()
        self._input = input
        self._id_chat = request.get_chat_id
        self._href = request.get_href

    @property
    def get_href(self):
        return self._href

    @property
    def get_input(self):
        return self._input

    @property
    def get_id_chat(self):
        return self._id_chat

    def _get_string(self):
        text = "{} {} {} {} {} {}".format(self._request.get_city, self._request.get_attrival_date,
                                          self._request.get_departure_date, self._request.get_n_adults,
                                          self._request.get_n_children, self._request.get_n_rooms)
        order = self._request.get_order_sorting
        if order is not None:
            text += ' ' + str(order)
        return text
