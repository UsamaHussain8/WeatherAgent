import json
import requests

def get_weather(city):
    city_str: str = json.loads(city).get('city')
    url = f"https://wttr.in/{city_str.lower()}?format=%C+%t" 
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather outlook for {city_str} is: {response.text}"

    return f"Something went wrong when fetching weather details for {city_str}"