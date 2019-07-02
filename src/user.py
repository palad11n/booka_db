class _User(object):
    """Сведения о запросе"""

    def __init__(self, id_chat, input):
        self._input = input
        self._id_chat = id_chat

    @property
    def get_input(self):
        return self._input

    @property
    def get_id_chat(self):
        return self._id_chat
