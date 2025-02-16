import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load cleaned weather data
try:
    df_weather = pd.read_csv("cleaned_weather_data.csv")
except FileNotFoundError:
    print("Error: 'cleaned_weather_data.csv' not found. Ensure the file exists.")
    exit()

# Encode categorical data
df_weather["Weather"] = df_weather["Weather"].astype("category").cat.codes

# Define features & labels
#X = df_weather[["Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)", "Weather"]]
#y = df_weather["Disaster Severity"]  # Assume severity is labeled as Low, Medium, High


# Define features & labels
X = df_weather[[
    "Temperature (°C)",
    "Humidity (%)",
    "Wind Speed (m/s)",
    "Rainfall (mm)",
    "Weather"
]]
y = df_weather["Disaster Severity"]



# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RandomForest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict & Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, "disaster_severity_model.pkl")
print("Model saved as 'disaster_severity_model.pkl'.")

