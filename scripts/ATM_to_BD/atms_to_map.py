import folium
import pandas as pd
from scripts.Utils.PSQLutils import PSQL

sql = PSQL()
lol = sql.get_atms_from_db(in_MKAD = True)
ATM_df = pd.DataFrame(lol, columns=['osmid', 'lon', 'lat', 'operator', 'in_MKAD'])


output_file = "output_htmls/atms_on_map.html"
map_center=[55.751244, 37.618423]
zoom_start=12

map_ = folium.Map(location=map_center, zoom_start=zoom_start)

for index, row in ATM_df.iterrows():

    lat = row['lat']
    lon = row['lon']
    folium.Marker(location=[lat, lon]).add_to(map_)

map_.save(output_file)
print(f"Карта сохранена как {output_file}")