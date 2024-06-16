from celery import Celery

from config_data.config import CITIES, config
from database.database import Connection, UploadBD
from utils.misc.coordinates import get_coordinates
from utils.weather import get_weather

app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task
def update_database():
    """Асинхронная функция обновления данных в БД"""

    with Connection(
        host=config.db.db_host,
        port=config.db.port,
        dbname=config.db.db_name,
        user=config.db.db_user,
        password=config.db.db_password,
    ) as conn:
        with conn.cursor() as cur:  # Создание таблицы
            UploadBD.create_table(cur)
            for city in CITIES:
                lat, lon = get_coordinates(city)
                data = get_weather(lat, lon)
                UploadBD.insert_data(cur, data, city)
                conn.commit()
