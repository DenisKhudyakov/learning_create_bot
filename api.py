from config_data import config
import requests

url = "https://hotels4.p.rapidapi.com/v2/get-meta-data"

headers = {
	"X-RapidAPI-Key": config.RAPID_API_KEY,
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())

