from geotext import GeoText
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


def extract_city(text):
    """
    TODO: Currently GeoText has very limited support. Items to explore here is
    TODO: using Natural Language Processing to avoid this conditional if statements.
    Another challenge is that few names of Exchanges doesnt have any City names at all.
    :param text: Text containing City name
    :return: returns the City Name
    """
    text = text.replace("Equinix", "")
    if 'New York' in text:
        return "New York"
    elif 'Los Angeles' in text:
        return "Los Angeles"
    elif ('LINX' in text) or ('LONAP' in text):
        return "London"
    elif 'BCIX' in text:
        return "Berlin"
    elif 'HKIX' in text:
        return "Hong Kong"
    elif 'QIX' in text:
        return "Montreal"
    elif 'TorIX' in text:
        return "Toronto"
    elif "Frankfurt" in text:
        return "Frankfurt"
    elif "AMS" in text:
        return "Amsterdam"
    elif "Saint-Petersburg" in text:
        return "Saint Petersburg"
    elif "Stockholm" in text:
        return "Stockholm"
    elif "NWAX" in text:
        return "Portland"
    elif "Thinx" in text:
        return "Warsaw"
    elif "Hong Kong" in text:
        return "Hong Kong"
    elif "Singapore" in text:
        return "Singapore"
    elif "FL-IX" in text:
        return "Miami"
    elif "Madrid" in text:
        return "Madrid"
    elif "KINX" in text:
        return "Seoul"
    elif "VIX" in text:
        return "Vienna"
    elif "MIX-IT" in text:
        return "Milan"
    elif "DATAIX" in text:
        return "Moscow"
    elif "CoreSite - Any2 California" in text:
        return "Los Angeles"
    elif "Peering.cz" in text:
        return "Prague"
    elif "NL-ix: Main" in text:
        return "Amsterdam"
    elif "NIX.CZ" in text:
        return "Prague"

    places = GeoText(text)
    if len(places.cities) > 0:
        city = places.cities[0]
        return city
    else:
        return None


def findGeocode(city):
    try:
        geolocator = Nominatim(user_agent="peeringdb")
        loc = geolocator.geocode(city)
        return loc.latitude, loc.longitude
    except GeocoderTimedOut:
        return None


def build_city_loc_mapping(city_list):
    city_dict = {}
    for city in city_list:
        lat, long = findGeocode(city)
        city_dict[city] = {'lat': lat, 'long': long}
    return city_dict


def extract_long_lat(df, city_dict):
    city = df.city
    long = city_dict.get(city).get('long')
    lat = city_dict.get(city).get('lat')
    return lat, long


