from math import radians, cos, sin, asin, sqrt


def haversine(site, origin_lon=None, origin_lat=None):
    """
    Calculates distance between coordinates using the haversine formula.
    Args:
        site: object which either has the attributes 'longitude' and 'latitude',
         or which has values for these at index positions 0 and 1.
        origin_lon (float): longitude of location compared against
        origin_lat (float): latitude of location compared against
    Returns:
        A float value for the distance in kilometres
    """
    if hasattr(site, 'longitude') and hasattr(site, 'latitude'):
        lon, lat = [float(getattr(site, s)) for s in ['longitude', 'latitude']]
    else:
        lon, lat = site[:2]
    assert all([lon, lat, origin_lon, origin_lat]), 'Not all params'

    lon1, lat1, lon2, lat2 = map(radians, [lon, lat, origin_lon, origin_lat])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r
