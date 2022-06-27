from googleplaces import GooglePlaces, types
from geopy import GoogleV3, distance
import pandas as pd
from pathlib import Path

from credentials import MAPS_API_TOKEN
geolocator = GoogleV3(api_key=MAPS_API_TOKEN)
google_places = GooglePlaces(MAPS_API_TOKEN)


def get_lat_long(address):
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude

    return latitude, longitude


def export_places(address, report_path):
    radius = 2000
    places = []
    latitude, longitude = get_lat_long(address)

    query_result = google_places.nearby_search(
            lat_lng={'lat': latitude, 'lng': longitude},
            radius=radius,
            types= [types.TYPE_HOSPITAL, types.TYPE_BANK, types.TYPE_GYM])

    if query_result.has_attributions:
        print(query_result.html_attributions)

    for place in query_result.places:
        coords_1 = (latitude, longitude)
        coords_2 = (float(place.geo_location["lat"]), float(place.geo_location["lng"]))
        distance_km = round(distance.geodesic(coords_1, coords_2).m, 2)
        places.append((place.name, distance_km))

    # Criando Dataframe
    df = pd.DataFrame(places, columns =['Local', 'Distância do Avaliado'])
    df = df.sort_values(by='Distância do Avaliado', ascending=True)

    if df.shape[0] >= 10:
        df = df[0:10]

    df = df.reset_index(drop=True)

    # Exportando Dataframe
    planilha = report_path.split('/')
    barra = str(r" \ ")[1]
    pyhon_file_path = str(Path(__file__).parent.resolve()).split(barra)
    user_path = barra.join(pyhon_file_path[:3])
    planilha_path = barra + barra.join(planilha[7:-1])
    file_name = r'\locais_coletados.xlsx'

    save_path = user_path + \
                str(r'\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis') + \
                planilha_path + file_name

    df.to_excel(save_path, sheet_name='Sheet1')
    print(df)
    print(f'Dados coletados foram salvos em: {save_path}')
        

if __name__ == '__main__':
    with open(str(Path(__file__).parent.resolve())+str(r'\file.txt'), 'r') as f:
        informations = f.read().split('\n')
        laudo = informations[0]
        endereco = informations[1]
        print(endereco)
        export_places(endereco, laudo)
