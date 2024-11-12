import osmnx as ox
import folium
import pandas as pd
import collections
from charset_normalizer.utils import range_scan
from config import DB, TableATM
import psycopg2

#conn.rollback()


class PSQL:
    def __init__(self):
        print(DB.dbname)
        self.conn = psycopg2.connect(user=DB.user, password=DB.password, host=DB.host, dbname=DB.dbname)
        with self.conn.cursor() as cur:
            sql_request = f"CREATE TABLE IF NOT EXISTS {TableATM.table_name} (osmid BIGSERIAL PRIMARY KEY, x_lon float8, y_lat float8, operator text);"
            cur.execute(sql_request)
        self.conn.commit()
    def write_atm_to_db(self, osmid, x_lon, y_lat, operator):
        with self.conn.cursor() as cur:
            sql_request = f"""
                    INSERT INTO {TableATM.table_name} (osmid, x_lon, y_lat, operator) 
                    VALUES ({osmid}, {x_lon}, {y_lat}, '{operator}')
                    ON CONFLICT (osmid) DO NOTHING;
                """
            cur.execute(sql_request)
            self.conn.commit()
    def close(self):
        self.conn.close()

class OSMatms:
    def __init__(self, city_name="Moscow, Russia"):
        self.city_name = city_name #"Moscow, Russia"
        self.tags = {'amenity': 'atm'}

    def get_city(self):
        atms = ox.geometries_from_place(self.city_name, self.tags)
        atms_points = atms[atms.geometry.type == 'Point']
        if atms_points.empty:
            atms_points = atms
        atms_points = atms_points.reset_index()
        atms_points['lat'] = atms_points.geometry.y
        atms_points['lon'] = atms_points.geometry.x
        return atms_points

sql = PSQL()
os = OSMatms()

atms = os.get_city()
atms = pd.DataFrame(atms)
atms = atms.fillna('Неизвестно')
for index, atm in atms.iterrows():
    sql.write_atm_to_db(atm['osmid'], atm['lon'], atm['lat'], atm['operator'])
sql.close()




