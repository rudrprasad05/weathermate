import os
import requests
from datetime import datetime
from git import Repo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
GIT_REPO_PATH = os.getenv("GIT_REPO_PATH")
LOG_FILE = os.path.join(GIT_REPO_PATH, "weatherlogs.txt")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
LOCATION = "Fiji"

def fetch_weather():
    params = {"q": LOCATION, "appid": API_KEY, "units": "metric"}
    response = requests.get(WEATHER_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    return weather, temp, humidity

def append_weather_to_file(weather, temp, humidity):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as file:
        file.write(f"{now}, {LOCATION}, {weather}, {temp}°C, {humidity}%\n")

def commit_and_push():
    repo = Repo(GIT_REPO_PATH)
    repo.git.add(LOG_FILE)
    repo.index.commit("Update weather logs")
    origin = repo.remote(name="origin")
    origin.push()

def main():
    try:
        weather, temp, humidity = fetch_weather()
        append_weather_to_file(weather, temp, humidity)
        commit_and_push()
        print("Weather data fetched and pushed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
