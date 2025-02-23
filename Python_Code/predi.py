import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# Load Pretrained Model
model = EfficientNetB0(weights="imagenet")

def predict_species(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        preds = model.predict(img_array)
        decoded_preds = decode_predictions(preds, top=1)[0]  # Get Top 1 Prediction

        species, confidence = decoded_preds[0][1], decoded_preds[0][2] * 100
        return species, confidence  # Returns species name & confidence score
    except Exception as e:
        print(f"Error predicting species: {e}")
        return "Unknown", 0.0