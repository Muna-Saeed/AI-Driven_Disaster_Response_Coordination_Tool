import requests
import pandas as pd
import json
import datetime

# OpenWeatherMap API Key
API_KEY = "b9343e1b7c6b1fa2f3e09b347938d232"

# List of cities to process
cities = ["Los Angeles", "San Francisco", "New York", "London"]

# Initialize an empty list to store weather data
weather_data = []

for city in cities:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract relevant fields
        weather_info = {
            "City": data["name"],
            "Temperature (°C)": data["main"]["temp"],
            "Humidity (%)": data["main"]["humidity"],
            "Wind Speed (m/s)": data["wind"]["speed"],
            "Weather": data["weather"][0]["description"],
            "Rainfall (mm)": data.get("rain", {}).get("1h", 0.0),  # Rainfall in the last 1 hour (default to 0.0 if not available)
            "Timestamp": datetime.datetime.utcfromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S')  # Convert UNIX timestamp to readable UTC time
        }
        weather_data.append(weather_info)
    else:
        print(f"Failed to fetch weather data for {city}. Error code: {response.status_code}")

# Convert the data to a Pandas DataFrame
df_weather = pd.DataFrame(weather_data)

# Add a 'Disaster Severity' column based on thresholds (example logic)
def classify_severity(row):
    if row["Rainfall (mm)"] > 50 or row["Wind Speed (m/s)"] > 20:
        return "High"
    elif row["Rainfall (mm)"] > 20 or row["Wind Speed (m/s)"] > 10:
        return "Medium"
    else:
        return "Low"

df_weather["Disaster Severity"] = df_weather.apply(classify_severity, axis=1)

# Add a 'Disaster Type' column based on thresholds
def assign_disaster_type(row):
    if row["Rainfall (mm)"] > 50 or row["Wind Speed (m/s)"] > 20:
        return "Severe Storm"
    elif row["Rainfall (mm)"] > 20:
        return "Moderate Rain"
    elif row["Wind Speed (m/s)"] > 10:
        return "Strong Winds"
    else:
        return "Normal"

df_weather["Disaster Type"] = df_weather.apply(assign_disaster_type, axis=1)

# Print the DataFrame to verify
print(df_weather)

# Save the updated DataFrame to a CSV file
df_weather.to_csv("cleaned_weather_data.csv", index=False)
print("Weather data saved to 'cleaned_weather_data.csv' with 'Disaster Severity' and 'Disaster Type' column.")

