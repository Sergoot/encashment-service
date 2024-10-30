from shapely.geometry import Point, Polygon
from scripts.Utils.MapUtils.mkad_coords import MKAD_1
import osmnx as ox
import geopy.distance

ox.config(use_cache=True,
          #log_console=True
            )


class OSMatms:
    def __init__(self, city_name="Moscow, Russia"):
        self.city_name = city_name #"Moscow, Russia"
        self.tags = {'amenity': 'atm'}
        self.mkad_polygon = Polygon([(lon, lat) for lon, lat in MKAD_1])
        self.road_graph = None
        self.road_nodes = None
        self.road_edges = None

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
    def init_place_graph(self, city="Moscow, Russia"):
        self.road_graph = ox.graph_from_place(city, network_type='drive')
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


if __name__ == '__main__':
    osm = OSMatms()
    osm.init_place_graph()
    print(osm.nearest_node(37.598474, 55.791857))