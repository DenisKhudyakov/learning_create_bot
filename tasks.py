from celery import Celery

from config_data.config import CITIES, config
from database.database import Connection, add_weather
from utils.misc.coordinates import get_coordinates
from utils.weather import get_weather

app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task
def update_database():
    """Асинхронная функция обновления данных в БД"""
    connection_params = {
        "host": config.db.db_host,
        "port": config.db.port,
        "dbname": config.db.db_name,
        "user": config.db.db_user,
        "password": config.db.db_password
    }

    with Connection(**connection_params) as conn:
        session = conn.Session()
        for city in CITIES:
            lat, lon = get_coordinates(city)
            data = get_weather(lat, lon)
            add_weather(session, city=city, temp=data['temp'], pressure=data['pressure'], grnd_level=data['grnd_level'], user_id=None)

