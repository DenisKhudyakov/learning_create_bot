import os
from dataclasses import dataclass

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_WEATHER_TOKEN = os.getenv("API_WEATHER_TOKEN")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("weather <Город>", "Показать прогноз погоды по городу"),
    ("max", "Показать максимальную температуру"),
    ("min", "Показать минимальную температуру"),
    ("history", "Показать историю запросов"),
)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
PORT = os.getenv("PORT")
KEY_GEOCODER = os.getenv("KEY_GEOCODER")
# добавьте необходимые города
CITIES = [
    "Челябинск",
    "Москва",
    "Миасс",
]  # Избранные города, по которым заполняется база данных, при желании можно добавить вручную


@dataclass
class DataBaseConfig:
    """Конфигурация базы данных"""

    db_host: str
    db_user: str
    db_password: str
    db_name: str
    port: str


@dataclass
class TgBotConfig:
    """Конфигурация бота"""

    token: str


@dataclass
class Config:
    """Конфигурация проекта"""

    tg_bot: TgBotConfig
    db: DataBaseConfig


config = Config(
    tg_bot=TgBotConfig(token=BOT_TOKEN),
    db=DataBaseConfig(
        db_host=DB_HOST,
        db_user=DB_USER,
        db_password=DB_PASSWORD,
        db_name=DB_NAME,
        port=PORT,
    ),
)
