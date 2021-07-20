import requests
import json
from credentials import MAPS_TOKEN


def get_bairro(cep):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?parameters'

    params = {
        'key': MAPS_TOKEN,
        'input': f'Brazil, CEP:{cep}',
        'inputtype': 'textquery',
        'fields': 'place_id,formatted_address,photos',
    }
    result = requests.post(url, params=params).json()['candidates'][0]
    
    return result['formatted_address'].split(',')[0]


#print(bairro('5415011'))