"""
тут, по сути, класс отвечающий за красивую отрисовку данных в HTML интерактивной карте
"""

from pandas import DataFrame
import folium

class ToFoliumMap:
    def __init__(self,
                 map_center:list[int] = [55.751244, 37.618423],
                 zoom_start:int = 12):
        self.map = folium.Map(location=map_center, zoom_start=zoom_start)

    def generate_atm_map(self, coordinates:DataFrame, lat_key, lon_key):
        for index, row in coordinates.iterrows():
            lat = row[lat_key]
            lon = row[lon_key]
            folium.Marker(location=[lat, lon]).add_to(self.map)

    def generate_atm_nn_map(self, coordinates:DataFrame,
                            atm_lat_key:str,
                            atm_lon_key:str,
                            nn_lat_key:str,
                            nn_lon_key:str
                            ):
        for index, row in coordinates.iterrows():
            atm_coord = [row[atm_lat_key], row[atm_lon_key]]
            nn_coord = [row[nn_lat_key], row[nn_lon_key]]
            folium.PolyLine(
                locations=[atm_coord, nn_coord],
                color='green',
                weight=2
            ).add_to(self.map)
            folium.Marker(location=atm_coord).add_to(self.map)


    def save_map(self, outputfile:str):
        self.map.save(outputfile)




