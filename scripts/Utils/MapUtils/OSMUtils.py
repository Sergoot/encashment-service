from shapely.geometry import Point, Polygon
from .mkad_coords import MKAD_1
import osmnx as ox


class OSMatms:
    def __init__(self, city_name="Moscow, Russia"):
        self.city_name = city_name #"Moscow, Russia"
        self.tags = {'amenity': 'atm'}
        self.mkad_polygon = Polygon([(lon, lat) for lon, lat in MKAD_1])

    def get_city(self):
        atms = ox.geometries_from_place(self.city_name, self.tags)
        atms_points = atms[atms.geometry.type == 'Point']
        if atms_points.empty:
            atms_points = atms
        atms_points = atms_points.reset_index()
        atms_points['lat'] = atms_points.geometry.y
        atms_points['lon'] = atms_points.geometry.x
        atms_points['in_MKAD'] = atms_points.apply(lambda row: self.check_in_MKAD(row['lon'], row['lat']), axis=1)
        return atms_points

    def check_in_MKAD(self, p_lon, p_lat):
        results = self.mkad_polygon.contains(Point(p_lon, p_lat))
        return results

