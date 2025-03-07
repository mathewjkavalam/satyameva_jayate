import streamlit as st
import pydeck as pdk
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

def plot_3d_location(latitude, longitude):
    if latitude and longitude:
        view_state = pdk.ViewState(latitude=latitude, longitude=longitude, zoom=11, pitch=60)
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=[{'lat': latitude, 'lon': longitude}],
            get_position='[lon, lat]',
            get_radius=10000,
            get_color=[0, 123, 255, 160],
            pickable=True
        )
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "Uploaded Image Location"},
            map_style='mapbox://styles/mapbox/outdoors-v11',
            api_keys={'mapbox': 'YOUR_MAPBOX_ACCESS_TOKEN'}
        )
        st.pydeck_chart(r)

# Dictionary for predicting habitat and region based on object class
habitat_region_dict = {
    "cat": {"Habitat": "Domestic", "Region": "Worldwide"},
    "dog": {"Habitat": "Domestic", "Region": "Worldwide"},
    "tiger": {"Habitat": "Wild", "Region": "Asia"},
    "lion": {"Habitat": "Wild", "Region": "Africa"},
    "elephant": {"Habitat": "Wild", "Region": "Africa, Asia"},
}

def get_habitat_and_region(predicted_class):
    if predicted_class in habitat_region_dict:
        return habitat_region_dict[predicted_class]
    else:
        return {"Habitat": "Unknown", "Region": "Unknown"}

st.title("EfficientNetB0 Image Classifier :camera:")
tabs = st.tabs(["Upload Image", "Habitat & Region"])

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
        
        plot_3d_location(latitude, longitude)

with tabs[1]:
    st.subheader("Predicted Habitat and Region")
    if upload:
        habitat_region = get_habitat_and_region(labels[0])
        st.write(f"**Predicted Class:** {labels[0]}")
        st.write(f"**Habitat:** {habitat_region['Habitat']}")
        st.write(f"**Region:** {habitat_region['Region']}")

init_db()
