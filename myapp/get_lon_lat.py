import requests
import urllib.parse

data = []
data_mapping = {
}

for d in data:
    puesto = d[0]
    direccion = d[1]
    if puesto not in data_mapping:
        data_mapping[puesto] = direccion


for key, value in data_mapping.items():

    address = value
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

    response = requests.get(url).json()
    if response:
        lat = response[0]["lat"]
        lon = response[0]["lon"]
        sep = ';'
        print(key, sep, value, sep, lat, sep, lon)