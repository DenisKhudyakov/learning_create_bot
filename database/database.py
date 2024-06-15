import psycopg2
from config_data.config import config


class Connection:
    """Класс подключения к базе данных"""

    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
            )
        except psycopg2.OperationalError as e:
            self.conn = psycopg2.connect(
                host=self.host, port=self.port, user=self.user, password=self.password
            )
            self.conn.autocommit = True
            cursor = self.conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {self.dbname}")
            cursor.execute(f"CREATE DATABASE {self.dbname}")

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.commit()
            self.conn.close()
        except TypeError as e:
            print(e)
            return True


class UploadBD:
    """Класс для загрузки данных в БД"""

    @staticmethod
    def create_table(self):
        """Создание таблицы"""
        pass

    def insert_data(self):
        """Запись данных"""
        pass