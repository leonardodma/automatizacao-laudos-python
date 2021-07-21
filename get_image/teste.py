from credentials import MAPS_TOKEN
import geopy
from geopy import Nominatim, GoogleV3
import folium
from folium.plugins import MarkerCluster


geolocator = GoogleV3(api_key=MAPS_TOKEN)

imovel = "Rua Casa do Ator 90, São Paulo, Brazil"

addresses =  ["Rua Professor Vahia de Abreu 41, São Paulo, Brazil", 
              "Rua Alvorada 303, São Paulo, Brazil",
              "Rua Doutor Fadlo Haidar 165, São Paulo, Brazil",
              "Avenida Doutor Cardoso de Melo 122, São Paulo, Brazil",
              "Rua Gomes de Carvalho 1146, São Paulo, Brazil"]


def get_coordinates(addresses):
    coordinates = []

    for i in range(len(addresses)):
        x = geolocator.geocode(addresses[i])
        try:
            coordinates.append((x.latitude, x.longitude))
        except:
            print(f'Não foi encontrado o seguinte erdereço: {addresses[i]}')
    
    return coordinates


def get_map_center():
    x = geolocator.geocode(imovel)

    return (x.latitude, x.longitude)


if __name__ == '__main__':
    coordinates =  get_coordinates(addresses)
    m = folium.Map(get_map_center())
    folium.CircleMarker(location=get_map_center(), radius=20, weight=5).add_to(m)

    marker_cluster = MarkerCluster()

    n = 1
    for point in coordinates:
        print(point)
        folium.Marker(location=point, popup = n, tooltip = n).add_to(marker_cluster)
        n += 1
    
    marker_cluster.add_to(m)

    m.fit_bounds(m.get_bounds())

    m.save("folium_map.html")