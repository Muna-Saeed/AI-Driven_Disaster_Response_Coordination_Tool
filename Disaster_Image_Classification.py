import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import pandas as pd
from collections import Counter

# Load pre-trained ResNet model
model = models.resnet50(pretrained=True)
model.eval()

# Define preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Load and preprocess the image
image_path = "disaster_zones.png"
image = Image.open(image_path).convert("RGB")
input_tensor = transform(image).unsqueeze(0)

# Perform prediction
output = model(input_tensor)
_, predicted_class = output.max(1)

# Disaster class mapping (example labels)
disaster_labels = {0: "Fire", 1: "Flood", 2: "Hurricane", 3: "Landslide"}
detected_disaster_type = disaster_labels.get(predicted_class.item(), "Unknown")

print(f"Detected Disaster Type: {detected_disaster_type}")

# Simulated multiple classifications for demonstration (can be adapted this for multiple zones or images)
detected_disasters = [detected_disaster_type] * 10

# Count disaster types
disaster_counts = Counter(detected_disasters)

# Create a DataFrame
df_disasters = pd.DataFrame(list(disaster_counts.items()), columns=["Type", "Count"])

# Save to CSV
output_csv_path = "classified_disasters.csv"
df_disasters.to_csv(output_csv_path, index=False)

print(f"Disaster classifications saved to {output_csv_path}")

