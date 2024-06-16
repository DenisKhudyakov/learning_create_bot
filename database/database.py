from typing import Any, Optional, Union

import psycopg2

from config_data.config import config


class Connection:
    """Класс подключения к базе данных"""

    def __init__(
        self, host: str, port: str, dbname: str, user: str, password: str
    ) -> None:
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

    def __exit__(self, exc_type, exc_val, exc_tb) -> Union[bool, None]:
        try:
            self.conn.commit()
            self.conn.close()
        except TypeError as e:
            print(e)
            return True


class UploadBD:
    """Класс для загрузки данных в БД"""

    @staticmethod
    def create_table(cur: Any) -> None:
        """Создание таблицы"""
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS weather 
            (
            city VARCHAR(255) NOT NULL,
            temp FLOAT,
            pressure INTEGER,
            grnd_level INTEGER
            )
            """
        )

    @staticmethod
    def insert_data(cur: Any, data: dict, city: str) -> None:
        """Запись данных"""
        cur.execute(
            """
        INSERT INTO weather (city, temp, pressure, grnd_level) VALUES (%s, %s, %s, %s)
        """,
            (
                city,
                data["temp"],
                data["pressure"],
                data["grnd_level"],
            ),
        )


def get_weather(city: str) -> Union[dict, None]:
    """Функция получения данных из БД"""
    with Connection(
        host=config.db.db_host,
        port=config.db.port,
        dbname=config.db.db_name,
        user=config.db.db_user,
        password=config.db.db_password,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM weather WHERE city = %s""",
                (city,),
            )
            row = cur.fetchall()
            if row:
                return {
                    "temp": row[0][1],
                    "pressure": row[0][2],
                    "grnd_level": row[0][3],
                }
            else:
                return None


if __name__ == "__main__":
    # Подключение к БД
    with Connection(
        host=config.db.db_host,
        port=config.db.port,
        dbname=config.db.db_name,
        user=config.db.db_user,
        password=config.db.db_password,
    ) as conn:
        with conn.cursor() as cur:  # Создание таблицы
            UploadBD.create_table(cur)
            UploadBD.insert_data(
                cur, {"temp": 10, "pressure": 100, "grnd_level": 1000}, "Moscow"
            )
            UploadBD.insert_data(
                cur, {"temp": 20, "pressure": 200, "grnd_level": 2000}, "London"
            )

            # Успешный тест
    print(get_weather("Москва"))
