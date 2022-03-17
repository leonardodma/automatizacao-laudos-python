# Imports 
from folium.map import Marker
from numpy import number
from credentials import MAPS_TOKEN
from geopy import GoogleV3
import folium
from folium.plugins import MarkerCluster
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path


# Chrome Driver 
options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

geolocator = GoogleV3(api_key=MAPS_TOKEN)
current_path = str(Path(__file__).parent.resolve())


def get_save_path(laudo_path):
    planilha = laudo_path.split('/')
    barra = str(r" \ ")[1]
    pyhon_file_path = str(Path(__file__).parent.resolve()).split(barra)
    user_path = barra.join(pyhon_file_path[:3])
    img_path = barra + barra.join(planilha[7:-1]) + barra + 'img'
    file_name = f'\\map.png'

    if img_path == str(r'\\img'):
        save_path = barra.join(laudo_path.split(barra)[:-1]) + '\img' + file_name
        folder = barra.join(laudo_path.split(barra)[:-1]) + '\img'
    else:
        save_path = user_path + str(r'\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis') + img_path + file_name
        folder = user_path + str(r'\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis') + img_path


    return save_path, folder 


def get_informatios():
    addresses = []

    with open(current_path+str(r'\file.txt'), 'r') as f:
        informations = f.read().split('\n')[:-1]
        laudo_path = informations[0]
        save_path, folder = get_save_path(laudo_path)
        imovel = informations[1] + ', Brazil'
        
        for i in range(2, len(informations)):
            x = informations[i].split(',')
            try:
                address = " ".join([x[0].strip(), x[1].strip()]) + ', ' + x[2] + ', ' + x[3] + ', Brazil' 
            except:
                address = x[0].strip() + x[1] + x[2] + ', Brazil' 

            addresses.append(address)

    
    return save_path, folder, imovel, addresses


save_path, folder, imovel, addresses = get_informatios()


def get_coordinates(addresses):
    coordinates = []

    for i in range(len(addresses)):
        x = geolocator.geocode(addresses[i])
        try:
            coordinates.append((x.latitude, x.longitude))
        except:
            print(f'Não foi encontrado o seguinte erdereço: {addresses[i]}')
    
    return coordinates


def get_main_location():
    x = geolocator.geocode(imovel)

    return (x.latitude, x.longitude)


def split_duplicates(addresses):
    l = addresses
    return list(set([x for x in l if l.count(x) > 1]))


def export_map_html():
    coordinates =  get_coordinates(addresses)
    duplicates = split_duplicates(coordinates)
    print(f'Itens duplicados: {duplicates}')

    m = folium.Map(get_main_location())
    folium.Marker(location=get_main_location(), tooltip = imovel, icon=folium.Icon(color='red', icon='fas fa-home', prefix='fa')).add_to(m)
    marker_cluster = MarkerCluster()

    n = 1
    for point in coordinates:
        icon_path = current_path+f'\\icons\\number-{n}.png'
        icon = folium.CustomIcon(icon_image=icon_path, icon_size=30)
        if point in duplicates:
            folium.Marker(location=point, tooltip = n, icon=icon).add_to(marker_cluster)
        else:
            folium.Marker(location=point, tooltip = n, icon=icon).add_to(m)

        n += 1
        
    marker_cluster.add_to(m)
    m.fit_bounds(m.get_bounds())
    m.save(current_path+str(r'\map.html'))


def export_map_png():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    html_file = current_path + str(r"\map.html")
    driver.get("file:///" + html_file)
    time.sleep(4)

    Path(folder).mkdir(parents=True, exist_ok=True)

    input('APERTE ENTER PARA FINALIZAR O PRINT: ')
    driver.get_screenshot_as_file(save_path)
    driver.quit()


if __name__ == '__main__':
    export_map_html()
    export_map_png()