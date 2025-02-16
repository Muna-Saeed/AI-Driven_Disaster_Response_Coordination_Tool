import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load satellite image
print("Loading image...")
image = cv2.imread("satellite_image.jpg")
print("Image loaded.")

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection to identify disaster zones
edges = cv2.Canny(gray_image, 50, 150)

# Display results
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(gray_image, cmap="gray")
plt.title("Grayscale Image")
plt.subplot(1, 2, 2)
plt.imshow(edges, cmap="gray")
plt.title("Detected Disaster Zones")
# plt.show()

# Save the plot to a file
output_path = "disaster_zones.png"
plt.savefig(output_path)
print(f"Plot saved as {output_path}")
