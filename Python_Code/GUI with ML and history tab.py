import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
import sqlite3
import geocoder
import datetime
import pandas as pd

# Database setup
def init_db():
    conn = sqlite3.connect("image_classification.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 timestamp TEXT, 
                 latitude REAL, 
                 longitude REAL, 
                 predicted_class TEXT)''')
    conn.commit()
    conn.close()

@st.cache_resource
def load_model():
    model = EfficientNetB0(weights='imagenet')
    return model

def preprocess_image(img):
    img = img.convert("RGB")
    img = img.resize((224, 224))  # Resize image to EfficientNetB0 input size
    img = np.array(img, dtype=np.float32)
    img = preprocess_input(img)  # Preprocess using EfficientNetB0 function
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def make_prediction(model, processed_img):
    preds = model.predict(processed_img)
    decoded_preds = decode_predictions(preds, top=5)[0]  # Get top 5 predictions
    labels = [pred[1] for pred in decoded_preds]
    scores = [pred[2] for pred in decoded_preds]
    return labels, scores

def get_location():
    g = geocoder.ip('me')  # Fetch approximate GPS location
    return g.latlng if g.latlng else (None, None)

def save_to_db(timestamp, latitude, longitude, predicted_class):
    conn = sqlite3.connect("image_classification.db")
    c = conn.cursor()
    c.execute("INSERT INTO history (timestamp, latitude, longitude, predicted_class) VALUES (?, ?, ?, ?)",
              (timestamp, latitude, longitude, predicted_class))
    conn.commit()
    conn.close()

st.title("EfficientNetB0 Image Classifier :camera:")
tabs = st.tabs(["Upload Image", "History"])

with tabs[0]:
    upload = st.file_uploader("Upload Image:", type=["png", "jpg", "jpeg"])
    if upload:
        img = Image.open(upload)
        processed_img = preprocess_image(img)
        model = load_model()
        labels, scores = make_prediction(model, processed_img)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latitude, longitude = get_location()
        save_to_db(timestamp, latitude, longitude, labels[0])
        
        # Visualization
        prob_fig = plt.figure(figsize=(12, 2.5))
        ax = prob_fig.add_subplot(111)
        plt.barh(y=labels[::-1], width=scores[::-1], color=["dodgerblue"] * 4 + ["tomato"])
        plt.title("Top 5 Probabilities", fontsize=15)
        st.pyplot(prob_fig, use_container_width=True)

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            main_fig = plt.figure(figsize=(6, 6))
            ax = main_fig.add_subplot(111)
            plt.imshow(img)
            plt.xticks([])
            plt.yticks([])
            st.pyplot(main_fig, use_container_width=True)

        with col2:
            st.write("Interpretation visualization not available for TensorFlow EfficientNetB0 model.")

# In the "History" tab
with tabs[1]:
    st.subheader("Classification History")
    conn = sqlite3.connect("image_classification.db")
    c = conn.cursor()
    c.execute("SELECT timestamp, latitude, longitude, predicted_class FROM history ORDER BY id DESC")
    data = c.fetchall()
    conn.close()

    if data:
        # Convert to DataFrame for better handling
        df = pd.DataFrame(data, columns=["Timestamp", "Latitude", "Longitude", "Predicted Class"])
        st.table(df)  # Display the data in a table with custom column names
    else:
        st.write("No history available.")

# Initialize the database
init_db()
