import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def fetch_species_data(species_name, db_name="WildlifeNew.db"):
    """
    Fetch species data from the database based on species name.
    """
    conn = sqlite3.connect(db_name)
    query = """
        SELECT species, confidence, region, date, time, latitude, longitude 
        FROM species_data WHERE species = ?
    """
    df = pd.read_sql_query(query, conn, params=(species_name,))
    conn.close()
    return df

def plot_trends(df, species_name):
    """
    Plot trends of species sightings over time.
    """
    df = df[df['date'] != "Not Provided"].copy()
    
    if df.empty:
        print(f"No valid date data available for {species_name}. Skipping trend plot.")
        return
    
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df_trend = df.groupby(df['date'].dt.date).size()
    
    plt.figure(figsize=(10, 5))
    plt.plot(df_trend.index, df_trend.values, marker='o', linestyle='-', color='b')
    plt.xlabel('Date')
    plt.ylabel('Sightings Count')
    plt.title(f'Trends for {species_name}')
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

def plot_heatmap(df, species_name):
    """
    Plot a heatmap of species sightings based on latitude and longitude.
    """
    plt.figure(figsize=(8, 6))
    sns.kdeplot(x=df['longitude'], y=df['latitude'], cmap='Reds', fill=True)
    plt.scatter(df['longitude'], df['latitude'], c='blue', s=10, label='Sightings')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Heatmap of {species_name} Sightings')
    plt.legend()
    plt.show()

def plot_migration_clusters(df, species_name):
    """
    Cluster species movement using K-Means clustering.
    """
    df = df.dropna(subset=['latitude', 'longitude']).copy()
    if df.empty:
        print(f"No valid location data available for {species_name}. Skipping clustering.")
        return
    
    coords = df[['latitude', 'longitude']]
    kmeans = KMeans(n_clusters=3, random_state=0, n_init=10).fit(coords)
    df['cluster'] = kmeans.labels_
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df['longitude'], y=df['latitude'], hue=df['cluster'], palette='viridis', s=50)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Migration Pattern Clustering for {species_name}')
    plt.show()

def predict_species_sightings(df, species_name):
    """
    Predict future species sightings using Exponential Smoothing.
    """
    df = df[df['date'] != "Not Provided"].copy()
    if df.empty:
        print(f"No valid date data available for {species_name}. Skipping prediction.")
        return
    
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df_trend = df.groupby(df['date'].dt.date).size()
    
    model = ExponentialSmoothing(df_trend, trend='add', seasonal=None, seasonal_periods=None)
    model_fit = model.fit()
    forecast = model_fit.forecast(10)
    
    plt.figure(figsize=(10, 5))
    plt.plot(df_trend.index, df_trend.values, marker='o', linestyle='-', color='b', label='Actual')
    plt.plot(forecast.index, forecast.values, marker='o', linestyle='--', color='r', label='Predicted')
    plt.xlabel('Date')
    plt.ylabel('Sightings Count')
    plt.title(f'Predicted Species Sightings for {species_name}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

def main():
    species_name = input("Enter species name: ")
    df = fetch_species_data(species_name)
    
    if df.empty:
        print(f"No data found for species: {species_name}")
    else:
        print(df.head())  # Show a preview of data
        plot_trends(df, species_name)
        plot_heatmap(df, species_name)
        plot_migration_clusters(df, species_name)
        predict_species_sightings(df, species_name)

if __name__ == "__main__":
    main()
