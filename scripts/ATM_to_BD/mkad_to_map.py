"""
простой скрипт по отрисовке всех данных точек МКАДа
из которых потом строится граница для АТМок
"""
import folium
import pandas as pd
from scripts.Utils.OSMutils.mkad_coords import MKAD_1

MKAD_df = pd.DataFrame(MKAD_1, columns=['lon', 'lat'])

output_file = "output_htmls/mkad_dots_on_map.html"
map_center=[55.751244, 37.618423]
zoom_start=12

map_ = folium.Map(location=map_center, zoom_start=zoom_start)

for index, row in MKAD_df.iterrows():

    lat = row['lat']
    lon = row['lon']
    folium.Marker(location=[lat, lon]).add_to(map_)

map_.save(output_file)
print(f"Карта сохранена как {output_file}")