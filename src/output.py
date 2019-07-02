import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import os
from hashlib_db import hash_string

style.use('ggplot')


class _Output(object):
    """Вывод результатов из БД.
    Запросы: 1. Если вводит тот же запрос => возможен вывод динамики цен
             2. Если вводит тот же запрос => возможен вывод прошлого ответа
             3. Избранные отели
    """

    def __init__(self, conn, id_chat):
        self.conn = conn
        self.c = conn.cursor()
        self._id_chat = id_chat

    def output_all(self):
        self._get_pd_tables('SELECT * FROM chat')
        self._get_pd_tables('SELECT * FROM favorite_hotels')
        self._get_pd_tables('SELECT * FROM hotel')
        self._get_pd_tables('SELECT * FROM prices')
        self._get_pd_tables('SELECT * FROM history_requests')
        self._get_pd_tables('SELECT * FROM list_hotels')

    def _get_pd_tables(self, sql):
        df = pd.read_sql(sql, self.conn)
        print(df.head())

    def dynamics_of_prices(self, hotel):
        id_hotel = hash_string(hotel)
        prices = "SELECT date, price from prices where id_hotel = %d" % id_hotel
        self.c.execute(prices)
        fetch = self.c.fetchall()
        if fetch is not None:
            name = str(self._id_chat) + ".png"
            dir = './dynamic_of_price/'
            if not os.path.exists(dir):
                os.makedirs(dir)
            relative_path=os.path.join(dir,name)
            self._graph_data(prices, hotel)
            plt.savefig(relative_path)
            return relative_path
            # plt.show()

    def _graph_data(self, request, hotel):
        self.c.execute(request)
        dates = []
        values = []
        for row in self.c.fetchall():
            dates.append(row[0])
            values.append(row[1])
        fig, ax = plt.subplots()
        ax.plot_date(dates, values, '-')
        fig.autofmt_xdate()
        plt.title('Динамика цен по отелю: %s' % hotel)

    def _is_exist_data(self, table):
        self.c.execute("SELECT * FROM " + str(table))
        rows = self.c.fetchall()
        if len(rows) == 0:
            # print("Нет данных в таблице.")
            return False
        return True
