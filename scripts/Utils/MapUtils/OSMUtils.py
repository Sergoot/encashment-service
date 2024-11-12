"""
класс отвечающий за работу с графами местности
просчет маршрута, выгрузка АТМов и тд
"""

from shapely.geometry import Point, Polygon
from scripts.Utils.MapUtils.mkad_coords import MKAD_1
import osmnx as ox
import geopy.distance
import networkx as nx
from time import time

ox.config(use_cache=True,
          #log_console=True
            )


class OSMatms:
    def __init__(self, city_name="Moscow, Russia"):
        self.city_name = city_name #"Moscow, Russia"
        self.tags = {'amenity': 'atm'}
        self.mkad_polygon = Polygon([(lon, lat) for lon, lat in MKAD_1])
        self.MAI_coord = (37.502668, 55.812432)
        self.MAI_nn = 266729320
        self.road_graph = None
        self.road_nodes = None
        self.road_edges = None
        self.debug = False

    def get_city(self):
        atms = ox.geometries_from_place(self.city_name, self.tags)
        atms_points = atms[atms.geometry.type == 'Point']
        if atms_points.empty:
            atms_points = atms
        atms_points = atms_points.reset_index()
        atms_points['lat'] = atms_points.geometry.y
        atms_points['lon'] = atms_points.geometry.x
        atms_points['in_mkad'] = atms_points.apply(lambda row: self.check_in_MKAD(row['lon'], row['lat']), axis=1)
        return atms_points

    def check_in_MKAD(self, p_lon, p_lat):
        results = self.mkad_polygon.contains(Point(p_lon, p_lat))
        return results

        #отдельно потому что очень долго думает
    def init_place_graph(self, city="Moscow, Russia", network_type='drive_service'):
        if not self.road_graph:
            self.road_graph = ox.graph_from_place(city, network_type=network_type)
            self.road_graph = ox.add_edge_speeds(self.road_graph)
            self.road_graph = ox.add_edge_travel_times(self.road_graph)
        self.road_nodes, self.road_edges = ox.graph_to_gdfs(self.road_graph)

    def nearest_node(self,lon,lat):
        nn_osmid = ox.nearest_nodes(self.road_graph, lon, lat)
        nn_coord = self.road_nodes.loc[nn_osmid]
        nn_lat = nn_coord['y']
        nn_lon = nn_coord['x']
        distance_to_atm = geopy.distance.geodesic([nn_lat, nn_lon], [lat, lon]).m
        distance_to_atm = int(distance_to_atm)
        return {
                'osmid':nn_osmid,
                'lon':nn_lon,
                'lat':nn_lat,
                'distance_to_atm':distance_to_atm,
                'in_mkad':self.check_in_MKAD(nn_lon, nn_lat)
                }

    def nearest_node(self, lon, lat):
        while True:
            try:
                nn_osmid = ox.nearest_nodes(self.road_graph, lon, lat)
                self.get_shortest_route(nn_osmid, self.MAI_nn)
                self.get_shortest_route(self.MAI_nn, nn_osmid)
                break
            except Exception as e:
                self.road_graph.remove_node(nn_osmid)
                self.init_place_graph()
                #raise e

        #if error == 9:
        #    raise 'слишком много ошибок'

        nn_coord = self.road_nodes.loc[nn_osmid]
        nn_lat = nn_coord['y']
        nn_lon = nn_coord['x']
        distance_to_atm = geopy.distance.geodesic([nn_lat, nn_lon], [lat, lon]).m
        distance_to_atm = int(distance_to_atm)
        return {
            'osmid': nn_osmid,
            'lon': nn_lon,
            'lat': nn_lat,
            'distance_to_atm': distance_to_atm,
            'in_mkad': self.check_in_MKAD(nn_lon, nn_lat)
            }



    def check_is_connected(self):
        return nx.is_weakly_connected(self.road_graph)

    def get_shortest_route(self, src:int, dst:int):
        route = nx.shortest_path(self.road_graph, src, dst, 'travel_time')
        return route

    def get_travel_time(self, route):
        travel_time = sum(
            self.road_graph[u][v][0]['travel_time']
            for u, v in zip(route[:-1], route[1:])
        )
        return travel_time
    def get_total_distance(self, route):
        total_distance = sum(
            self.road_graph[u][v][0]['length']  # Длина ребра от u к v в метрах
            for u, v in zip(route[:-1], route[1:]))
        return total_distance




if __name__ == '__main__':
    osm = OSMatms()
    osm.debug = True
    city = osm.get_city()
    start = time()
    osm.init_place_graph(network_type='drive')
    #print('mai nn: ',osm.nearest_node(37.510478, 55.808175))
    print('инициализировал графф:', time() - start)
    nn = osm.nearest_node(37.510478, 55.808175)
    #10700489641 #37.6647837,55.6782474
    #7319552029 #37.6356077, 'lat': 55.7050998
    #
    #print(nn)
    src = 10700489641#2616240395
    dst = 7319552029#1885509144

    #баганные корды
    #"10580917887";"1885292148"
    src = 10580917887
    dst = 1885292148
    start = time()
    #route = osm.get_shortest_route(src,dst)
    #travel_time = osm.get_travel_time(route)
    #total_distance = osm.get_total_distance(route)
    #print('считал маршрут,время,расстояние:', time() - start)

    #print('travel_time= ', travel_time)
    #print('total_distance= ', total_distance)
    #route_map = ox.plot_route_folium(osm.road_graph, route)

    #route_map.save('test_road.html')
    #print(city[nn])
