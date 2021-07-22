# Imports 
from folium.map import Marker
from credentials import MAPS_TOKEN
from geopy import GoogleV3
import folium
from folium.plugins import MarkerCluster
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path


# Chrome Driver 
chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver_win32\chromedriver.exe')
options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

geolocator = GoogleV3(api_key=MAPS_TOKEN)
current_path = str(Path(__file__).parent.resolve())


def get_informatios():
    addresses = []

    with open(current_path+str(r'\file.txt'), 'r') as f:
        informations = f.read().split('\n')[:-1]
        laudo_path = informations[0]
        imovel = informations[1] + ', Brazil'
        
        for i in range(2, len(informations)):
            x = informations[i].split(',')
            address = " ".join([x[0].strip(), x[1].strip()]) + ', ' + x[2] + ', ' + x[3] + ', Brazil' 
            addresses.append(address)

    
    return laudo_path, imovel, addresses


laudo_path, imovel, addresses = get_informatios()


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


def export_map_html():
    coordinates =  get_coordinates(addresses)
    m = folium.Map(get_main_location())
    folium.Marker(location=get_main_location(), tooltip = imovel, icon=folium.Icon(color='red', icon='fas fa-home', prefix='fa')).add_to(m)

    n = 1
    for point in coordinates:
        icon_path = current_path+f'\\icons\\number-{n}.png'
        icon = folium.CustomIcon(icon_image=icon_path, icon_size=30)
        folium.Marker(location=point, tooltip = n, icon=icon).add_to(m)
        n += 1

    m.fit_bounds(m.get_bounds())
    m.save(current_path+str(r'\map.html'))


def export_map_png():
    driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
    html_file = current_path + str(r"\map.html")
    driver.get("file:///" + html_file)
    time.sleep(4)
    driver.get_screenshot_as_file(current_path+str(r'\map.png'))
    driver.quit()


if __name__ == '__main__':
    export_map_html()
    export_map_png()