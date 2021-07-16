import requests
import json


def get_photoreference(address):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?parameters'

    params = {
        'key': 'AIzaSyCyLcS8hGD3OhWKfj0Lqscs4NjL4Si_Voo',
        'input': address,
        'inputtype': 'textquery',
        'fields': 'place_id,formatted_address,photos',
    }
    result = requests.post(url, params=params).json()['candidates'][0]
    
    #place_id = result['place_id']
    photoreference = result['photos'][0]['photo_reference']
    
    return photoreference


def get_image(address):
    
    url = 'https://maps.googleapis.com/maps/api/place/photo?parameters'
    
    try:
        params = {
            'key': 'AIzaSyCyLcS8hGD3OhWKfj0Lqscs4NjL4Si_Voo',
            'photoreference': get_photoreference(address),
            'maxwidth': 700,
        }

        result = requests.post(url, params=params)

        file = open("sample_image.png", "wb")
        file.write(result.content)
        file.close()
    except:
        print('Não existe fotos desse imóvel no Google')

ad1 = 'Avanida Brg. Faria Lima 1800, São Paulo'
ad2 = 'Avanida Paulista 1811, São Paulo'
ad3 = 'Oracle do Brasil Sistemas'
#print(get_photoreference('140 George St, The Rocks NSW 2000, Austrália'))
#print('\n\n')
get_image(ad3)