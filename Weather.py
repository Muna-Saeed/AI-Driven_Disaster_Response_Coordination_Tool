import requests
import json

# OpenWeatherMap API Key
API_KEY = "b9343e1b7c6b1fa2f3e09b347938d232"

# Prompt the user for a city name
#CITY = input("Enter the name of the city: ")
CITY = "Los Angeles"

# Construct the API URL
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Fetch data from the API
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Extract and display weather details
    print(f"City: {data['name']}")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Weather: {data['weather'][0]['description']}")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind Speed: {data['wind']['speed']} m/s")

    # Save the data to a JSON file
    with open("weather_data.json", "w") as file:
        json.dump(data, file)
        print("Weather data saved to 'weather_data.json'.")
else:
    print(f"Failed to fetch weather data. Error code: {response.status_code}")

