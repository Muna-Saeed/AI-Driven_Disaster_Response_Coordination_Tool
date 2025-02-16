import requests

# NASA API Key (Sign up to get your own key)
API_KEY = "hjdKZb8kzVkcXECbZZoVrmzTpCD3azVEb8rYL9wS"

# Example: Fetch satellite image of a specific location
lat, lon = 37.7749, -122.4194  # San Francisco
date = "2024-02-05"

url = f"https://api.nasa.gov/planetary/earth/assets?lon={lon}&lat={lat}&date={date}&dim=0.1&api_key={API_KEY}"

response = requests.get(url)
data = response.json()
#print("Satellite Image URL:", data["url"])

if "url" in data:
    image_url = data["url"]
    print("Satellite Image URL:", image_url)

    # Download the image
    image_response = requests.get(image_url)

    if image_response.status_code == 200:
        # Save the image to a file
        with open("satellite_image.jpg", "wb") as file:
            file.write(image_response.content)
        print("Satellite image saved as satellite_image.jpg")
    else:
        print("Failed to download the satellite image.")
else:
    print("No image URL found in the response.")

