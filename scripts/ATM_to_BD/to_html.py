try:
    gdf = ox.geocode_to_gdf(city_name)
except Exception as e:
    print(f"Ошибка при получении геометрии города: {e}")

# Определение тега для банкоматов
tags = {'amenity': 'atm'}

# Загрузка объектов из OSM
try:
    atms = ox.geometries_from_place(city_name, tags)
except Exception as e:
    print(f"Ошибка при загрузке данных из OSM: {e}")

# Фильтрация точечных объектов (если есть)
atms_points = atms[atms.geometry.type == 'Point']

# Если нет точечных объектов, используем все банкоматы
if atms_points.empty:
    atms_points = atms

# Сброс индексов для удобства
atms_points = atms_points.reset_index()
#print(dict(atms_points.loc[1962]))

l = list(atms_points['operator'])
print(collections.Counter(l))
#print(list(atms_points['operator']))


# Получение координат банкоматов
atms_points['lat'] = atms_points.geometry.y
atms_points['lon'] = atms_points.geometry.x


print(atms_points)

# Определение центра карты (центр геометрии города)
center_lat = gdf.geometry.centroid.y.values[0]
center_lon = gdf.geometry.centroid.x.values[0]

# Создание карты с помощью folium
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Добавление маркеров для каждого банкомата
for idx, row in atms_points.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=row['name'] if pd.notnull(row.get('name')) else "Банкомат",
        icon=folium.Icon(color='blue', icon='credit-card')
    ).add_to(m)

# Сохранение карты в файл HTML
m.save("atms_map.html")

print("Карта сохранена в файл 'atms_map.html'. Откройте его в браузере для просмотра.")

