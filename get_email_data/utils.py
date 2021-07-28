from os import name
import os
import requests
import json
from credentials import MAPS_TOKEN
import wikipedia
wikipedia.set_lang("pt")


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


def get_obs(bairro, cidade):
    try:
        obs = wikipedia.summary(f"{bairro} - Bairro de {cidade}").split("\n")

        if len(obs) > 1:
            if len(obs[0].split('.')) > 2:
                return obs[0]
            else:
                return obs[0] + ' ' + obs[1]
        else:
            return obs[0]
    except:
        return 'Não foi encontrado nada sobre esse bairro no Wikpedia'
        

#print(get_obs('Jardim Ingá', 'São Paulo'))