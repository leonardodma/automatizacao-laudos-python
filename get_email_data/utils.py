from os import name
import os
import requests
import json
from credentials import MAPS_TOKEN
import wikipedia
wikipedia.set_lang("pt")


def get_bairro_correios(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    result = requests.get(url).json()
    return result['bairro']


def get_bairro(cep):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?parameters'

    params = {
        'key': MAPS_TOKEN,
        'input': f'CEP: {cep}, Brasil',
        'inputtype': 'textquery',
        'fields': 'place_id,formatted_address',
    }

    try:
        return get_bairro_correios(cep)
    except:
        try:
            result = requests.post(url, params=params).json()['candidates'][0]
            infos = result['formatted_address'].split(',')

            if len(infos) == 4:
                return infos[0]
            elif len(infos) == 5:
                return infos[1]
            else:
                return ""
        except:
            return ""


def get_obs(bairro, cidade):
    if len(bairro) > 0:
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
    else:
        return ""
    