from crawler import *
from pathlib import Path
from geopy import GoogleV3
from dotenv import dotenv_values
import os

env_path = str(os.path.dirname(os.path.realpath(__file__))).split(" \ "[1])
env_path = " \ "[1].join(env_path[0:-1]) + " \ "[1] + ".env"


# Secrets
config = dict(dotenv_values(env_path))
MAPS_API_TOKEN = config["MAPS_API_TOKEN"]

# Geolocator
geolocator = GoogleV3(api_key=MAPS_API_TOKEN)


def get_lat_long(address):
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude

    return latitude, longitude


if __name__ == '__main__':
    with open(str(Path(__file__).parent.resolve())+str(r'\file.txt'), 'r') as f:
        informations = f.read().split('\n')
        laudo = informations[0]

        endereco = informations[1]
        numero = informations[2]
        bairro = informations[3]
        municipio = informations[4]
        uf = informations[5]
        cep = informations[6]
        tipo = informations[7]

        try:
            area = int(informations[8])
        except:
            area = int(float(".".join(informations[8].split(","))))

        # Planilha
        print(f'LAUDO: {laudo}')

    search_address = f"{endereco}, {numero} - {bairro}, {municipio} - {uf}, {cep}"
    latitude, longitude = get_lat_long(search_address)
    samples_crawler = Crawler(
        latitude, longitude, bairro, municipio, uf, area, tipo)
    samples_crawler.export_data(laudo)
