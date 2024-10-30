from pandas import DataFrame
import folium


class ToFoliumMap:
    def __init__(self,
                 map_center:list[int] = [55.751244, 37.618423],
                 zoom_start:int = 12):
        self.map = folium.Map(location=map_center, zoom_start=zoom_start)

    def generate_map(self, coordinates:DataFrame, lat_key, lon_key):
        for index, row in coordinates.iterrows():
            lat = row[lat_key]
            lon = row[lon_key]
            folium.Marker(location=[lat, lon]).add_to(self.map)

    def save_map(self, outputfile:str):
        self.map.save(outputfile)




