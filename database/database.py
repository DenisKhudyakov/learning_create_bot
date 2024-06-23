from typing import Any, Optional, Union

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config_data.config import config
from models.models import User, Weather, Base


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
        self.engine = None
        self.Session = None

    def __enter__(self):
        self.engine = create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}",
            echo=True,
        )
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Session.remove()
        self.engine.dispose()


def add_user(session, user_id: int, full_name: str):
    """Функция добавления нового пользователя"""
    user = User(user_id=user_id, full_name=full_name)
    session.add(user)
    session.commit()


def add_weather(session, city: str, temp: float, pressure: int, grnd_level: int, user_id: int | None):
    """Функция добавления новой погоды"""
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        weather = Weather(city=city, temp=temp, pressure=pressure, grnd_level=grnd_level, user_id=user.id)
        session.add(weather)
        session.commit()
    else:
        weather = Weather(city=city, temp=temp, pressure=pressure, grnd_level=grnd_level)
        session.add(weather)
        session.commit()


def get_weather_history(session, user_id: int) -> Union[Weather, list]:
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        return session.query(Weather).filter(Weather.user_id == user.id).all()
    return []


if __name__ == "__main__":
    connection_params = {
        "host": config.db.db_host,
        "port": config.db.port,
        "dbname": config.db.db_name,
        "user": config.db.db_user,
        "password": config.db.db_password
    }
    # Подключение к БД
    with Connection(**connection_params) as conn:
        session = conn.Session()

        # Добавление нового пользователя
        add_user(session, user_id=12345, full_name="john_doe")

        # Добавление записи о погоде
        add_weather(session, user_id=12345, city="Нижний Новогород", temp=20.5, pressure=1013, grnd_level=1000)

        # Получение истории погоды
        history = get_weather_history(session, user_id=12345)
        for record in history:
            print(
                f"Weather in {record.city}: {record.temp}°C, Pressure: {record.pressure}, Ground Level: {record.grnd_level}")


