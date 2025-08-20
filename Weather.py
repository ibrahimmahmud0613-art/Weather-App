# weather.py
# Simple Weather CLI using Open-Meteo (no API key needed)

import sys
import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def geocode(city: str):
    r = requests.get(GEOCODE_URL, params={"name": city, "count": 1})
    r.raise_for_status()
    data = r.json()
    if not data.get("results"):
        raise ValueError(f"City not found: {city}")
    top = data["results"][0]
    return {"name": top["name"], "country": top.get("country", ""),
            "lat": top["latitude"], "lon": top["longitude"]}

def get_current_weather(lat: float, lon: float):
    r = requests.get(FORECAST_URL, params={
        "latitude": lat, "longitude": lon, "current_weather": True
    })
    r.raise_for_status()
    cw = r.json().get("current_weather")
    if not cw:
        raise RuntimeError("Weather data unavailable.")
    return cw

def main():
    if len(sys.argv) < 2:
        print("Usage: python weather.py <city name>")
        sys.exit(1)
    city = " ".join(sys.argv[1:])
    try:
        loc = geocode(city)
        cw = get_current_weather(loc["lat"], loc["lon"])
        print(f"🌦  Weather — {loc['name']}, {loc['country']}")
        print(f"Temperature : {cw['temperature']}°C")
        print(f"Windspeed   : {cw['windspeed']} m/s")
        print(f"Time        : {cw['time']}")
    except Exception as e:
        print("Error:", e); sys.exit(2)

if __name__ == "__main__":
    main()
