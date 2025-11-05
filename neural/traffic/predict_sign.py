import cv2
import numpy as np
from tensorflow.keras.models import load_model

IMG_WIDTH = 30
IMG_HEIGHT = 30

# Load and preprocess the new image
image = cv2.imread("stop_google.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
image = image / 255.0
image = np.expand_dims(image, axis=0)   # shape: (1, width, height, 3)

# Predict
model = load_model("saved_model.keras")
prediction = model.predict(image)
print(prediction[0])
# Get indices of the 3 highest values (sorted descending)
top3_indices = np.argsort(prediction[0])[-3:][::-1]

print("Top 3 predicted labels:")
for i in top3_indices:
    print(f"Label {i}: {prediction[0][i]:.4e}")