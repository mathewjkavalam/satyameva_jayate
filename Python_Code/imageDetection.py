import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# Load pretrained EfficientNet-B0 model
model = EfficientNetB0(weights="imagenet")

# Function to predict species
def predict_species(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Resize image
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array)
    decoded_preds = decode_predictions(preds, top=3)[0]  # Get top 3 predictions
    
    return decoded_preds
img_path = "2.jpg"  
predictions = predict_species(img_path)

# Print predictions
for rank, (id, species, confidence) in enumerate(predictions, 1):
    print(f"{rank}. {species}: {confidence*100:.2f}%")
