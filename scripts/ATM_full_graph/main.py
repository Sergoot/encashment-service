from time import time
import networkx as nx
import osmnx as ox
import random
from config import DB, TableATM
import psycopg2
import pandas as pd


class PSQL():
    def __init__(self):
        self.conn = psycopg2.connect(user=DB.user, password=DB.password, host=DB.host, dbname=DB.dbname)
    def write_atm_to_db(self, osmid, x_lon, y_lat, operator):
        with self.conn.cursor() as cur:
            sql_request = f"""
                    INSERT INTO {TableATM.table_name} (osmid, x_lon, y_lat, operator) 
                    VALUES ({osmid}, {x_lon}, {y_lat}, '{operator}')
                    ON CONFLICT (osmid) DO NOTHING;
                """
            cur.execute(sql_request)
            self.conn.commit()
    def get_all(self):
        with self.conn.cursor() as cur:
            sql_request = f"SELECT * FROM {TableATM.table_name}"
            cur.execute(sql_request)
            return cur.fetchall()
    def close(self):
        self.conn.close()


sql = PSQL()
lol = sql.get_all()
df = pd.DataFrame(lol, columns=['osmid', 'x_lon', 'y_lat', 'operator'])

print(df['osmid'][0])


ox.config(use_cache=True, log_console=True)
G = ox.graph_from_place('Moscow, Russia', network_type='drive')
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)


try:
    x1 = df['x_lon'][100]
    y1 = df['y_lat'][100]
    x2 = df['x_lon'][130]
    y2 = df['y_lat'][130]
    print(x1, y1)
    print(x2, y2)
    n1 = ox.nearest_nodes(G, x1, y1)
    n2 = ox.nearest_nodes(G, x2, y2)

    #print(G[n1])
    #print(dir(n1))
    print(n1, n2)
    #src = df['osmid'][1]
    #dst = df['osmid'][2]
    route = nx.shortest_path(G, n1, n2, 'travel_time')
    route_map = ox.plot_route_folium(G, route)
    #route_map = ox.plot_figure_ground(G, point=(x1,y1))
    route_map.save('test_2_atms.html')
except Exception as e:
    print('путь не найден')
    raise e


