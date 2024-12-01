import math


def get_radius_range(lat: float, long: float, radius: int = 100):
    # Earth's radius in meters
    earth_radius = 6371000
    
    # Convert radius from meters to radians
    radius_rad = radius / earth_radius
    
    # Calculate angular radius in radians
    angular_radius = 2 * math.asin(radius_rad)
    
    # Calculate latitude range
    min_lat = lat - math.degrees(angular_radius)
    max_lat = lat + math.degrees(angular_radius)
    
    # Calculate longitude range
    # Note: This assumes a small radius, so we can use approximation
    lon_range = math.degrees(radius_rad * math.cos(math.radians(lat)))
    
    return {
        'lat_max': max_lat,
        'lat_min': min_lat,
        'long_max': long + lon_range,
        'long_min': long - lon_range
        }