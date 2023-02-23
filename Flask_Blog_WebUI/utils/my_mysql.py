import pymysql
from setting import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_DB


class Mysql:
    def init(self, host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT, db=MYSQL_DB):
        self.db = pymysql.connect(host=host, user=user, password=password, port=port)
        self.cursor = self.db.cursor()

    def select(self, sql):
        self.cursor.execute(sql)

    def get_data(self):
        return self.cursor.fetchone()
