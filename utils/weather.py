from utils.misc.coordinates import get_coordinates
from config_data.config import API_WEATHER_TOKEN
import requests


def get_weather(lat, lon):
    """Получение погоды по координатам"""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_WEATHER_TOKEN}&units=metric"
    response = requests.get(url)
    return response.json()["main"]


if __name__ == "__main__":
    lat, lon = get_coordinates("Челябинск")
    print(get_weather(lat, lon))
