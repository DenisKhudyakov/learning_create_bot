import requests
<<<<<<< HEAD
import json

id_list = []
url_list = []
url = 'https://www.tesli.com/api/v2/catalog/partnumber'
headers = {'X-Tesli-login': 'snab13@chzmek.ru', 'X-Tesli-password': 'Den!271192', 'X-Tesli-inn': '7450061013'}

get_url = requests.get(url, headers=headers)

for i in get_url.json():
     url_list.append(i['urlFile'])

for i in url_list:
    response = requests.get(i, headers=headers)
    with open('katalog_xml.xml', 'wb') as f:
        f.write(response.content)



# for i in get_url.json():
#     id_list.append(i['id'])
#
# param = {'id': id_list}
#
# url_product = 'https://www.tesli.com/api/v2/catalog/products'
#
# get_product = requests.get(url_product, params=param, headers=headers)
# print(get_product.text)
# print(get_product.json())
=======
from config_data import config

url = "https://hotels4.p.rapidapi.com/v2/get-meta-data"

headers = {
	"X-RapidAPI-Key": config.RAPID_API_KEY,
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())
>>>>>>> e1e2750 (add_apy.py)
