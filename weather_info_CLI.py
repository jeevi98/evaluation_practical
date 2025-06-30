import requests
import json
import os

API_KEY = 'your_openweathermap_api_key' 
API_URL = 'http://api.openweathermap.org/data/2.5/weather'
HISTORY_FILE = 'weather_history.json'


def fetch_weather(city):
    try:
        params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
        response = requests.get(API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        weather = {
            'City': data['name'],
            'Temperature (°C)': data['main']['temp'],
            'Humidity (%)': data['main']['humidity'],
            'Sky': data['weather'][0]['description'].title()
        }
        return weather

    except requests.exceptions.ConnectionError:
        print(" No internet connection.")
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            print(" City not found.")
        else:
            print(f" Error: {response.status_code}")
    except Exception as e:
        print(f" Unexpected error: {e}")


def save_to_history(entry):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    history.insert(0, entry)
    history = history[:5] 
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)


def show_history():
    if not os.path.exists(HISTORY_FILE):
        print(" No history yet.")
        return
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)
    print("\n Last 5 Queries:")
    for entry in history:
        print(f"{entry['City']} - {entry['Temperature (°C)']}°C, {entry['Sky']}")


def main():
    print(" Welcome to Weather Info CLI ")

    while True:
        city = input("\nEnter city name (or type 'history' / 'exit'): ").strip()
        if city.lower() == 'exit':
            print(" Goodbye!")
            break
        elif city.lower() == 'history':
            show_history()
        elif city:
            weather = fetch_weather(city)
            if weather:
                print("\n Weather Report:")
                for key, value in weather.items():
                    print(f"{key}: {value}")
                save_to_history(weather)
        else:
            print(" Please enter a city name.")

if __name__ == "__main__":
    main()
