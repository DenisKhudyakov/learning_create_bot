import requests

from config_data.config import KEY_GEOCODER


def get_coordinates(city: str) -> str:
    """Получение координат по городу с использованием Yandex Geocoder"""
    response = requests.get(
        f"https://geocode-maps.yandex.ru/1.x/?apikey={KEY_GEOCODER}&geocode={city}&format=json"
    )
    coordinates_city = response.json()["response"]["GeoObjectCollection"][
        "featureMember"
    ][0]["GeoObject"]["Point"]["pos"]
    return coordinates_city.split(" ")


if __name__ == "__main__":
    print(get_coordinates("Москва"))
