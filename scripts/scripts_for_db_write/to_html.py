import osmnx as ox
import folium
import pandas as pd
import collections

city_name = 'Moscow, Russia'

gdf = ox.geocode_to_gdf(city_name)

tags = {'amenity': 'atm'}

atms = ox.geometries_from_place(city_name, tags)

atms_points = atms[atms.geometry.type == 'Point']

if atms_points.empty:
    atms_points = atms

atms_points = atms_points.reset_index()

l = list(atms_points['operator'])
print(collections.Counter(l))

atms_points['lat'] = atms_points.geometry.y
atms_points['lon'] = atms_points.geometry.x


print(atms_points)

center_lat = gdf.geometry.centroid.y.values[0]
center_lon = gdf.geometry.centroid.x.values[0]

m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

for idx, row in atms_points.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=row['name'] if pd.notnull(row.get('name')) else "Банкомат",
        icon=folium.Icon(color='blue', icon='credit-card')
    ).add_to(m)

m.save("atms_map.html")


