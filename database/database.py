from typing import Any, Optional, Union

from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker

from config_data.config import config
from models.models import Base, User, Weather
from functools import wraps


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


def connect_bd(func):
    """Декоратор подключения к БД, для того чтобы в хендлерах не повторять подключение"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        connection_params = {
            "host": config.db.db_host,
            "port": config.db.port,
            "dbname": config.db.db_name,
            "user": config.db.db_user,
            "password": config.db.db_password,
        }
        with Connection(**connection_params) as conn:
            session = conn.Session()
            result = func(session, *args, **kwargs)
            session.close()
        return result

    return wrapper


@connect_bd
def add_weather(
    session, city: str, temp: float, pressure: int, grnd_level: int, user_id: int | None
) -> None:
    """Функция добавления новой погоды"""
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        weather = Weather(
            city=city,
            temp=temp,
            pressure=pressure,
            grnd_level=grnd_level,
            user_id=user.id,
        )
        session.add(weather)
        session.commit()
    else:
        weather = Weather(
            city=city, temp=temp, pressure=pressure, grnd_level=grnd_level
        )
        session.add(weather)
        session.commit()


@connect_bd
def add_user(session, user_id: int, full_name: str) -> None:
    """Функция добавления нового пользователя"""
    user = User(user_id=user_id, full_name=full_name)
    session.add(user)
    session.commit()


@connect_bd
def get_weather_history(session, user_id: int) -> Union[Weather, list]:
    """Получение погода конкретного пользователя"""
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        return session.query(Weather).filter(Weather.user_id == user.id).all()
    return []


@connect_bd
def max_temp(session) -> float:
    """Получение максимальной температуры"""
    return session.query(func.max(Weather.temp)).scalar()


@connect_bd
def min_temp(session) -> float:
    """Получение минимальной температуры"""
    return session.query(func.min(Weather.temp)).scalar()


@connect_bd
def get_weather_from_db(session, city: str) -> Union[Weather, list]:
    """Получение последней добавленной погоды по городу"""
    return (
        session.query(Weather)
        .filter(Weather.city == city)
        .order_by(Weather.id.desc())
        .first()
    )




