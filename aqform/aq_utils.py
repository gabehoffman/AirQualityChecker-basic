import requests

def geocode_location(city, state, country):
    """
    Use Nominatim to convert location to latitude and longitude.
    Returns (lat, lon, display_name) or (None, None, None) if not found.
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'city': city,
        'state': state,
        'country': country,
        'format': 'json',
        'limit': 1
    }
    headers = {'User-Agent': 'AirQualityChecker/1.0'}
    try:
        resp = requests.get(base_url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data:
            return data[0]['lat'], data[0]['lon'], data[0]['display_name']
    except Exception:
        pass
    return None, None, None

def fetch_air_quality(lat, lon):
    """
    Use Open-Meteo Air Quality API to fetch AQI and details for given coordinates.
    Returns a dict with AQI info or None if failed.
    """
    base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi_pm2_5,us_aqi_pm10,us_aqi_o3,us_aqi_no2,us_aqi_so2,us_aqi_co',
        'timezone': 'auto',
        'forecast_days': 1
    }
    try:
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None
