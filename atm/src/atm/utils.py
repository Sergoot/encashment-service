import math


def get_radius_range(lat: float, long: float, radius: int = 100) -> dict:
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
    min_long = long - math.degrees(angular_radius / math.cos(math.radians(lat)))
    max_long = long + math.degrees(angular_radius / math.cos(math.radians(lat)))
    
    return {
        'lat_max': max_lat,
        'lat_min': min_lat,
        'long_max': max_long,
        'long_min': min_long
    }