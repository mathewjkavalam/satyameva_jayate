import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib
matplotlib.use('Agg')  # Prevents GUI issues in headless environments

# ✅ Folder to store generated insights
INSIGHTS_FOLDER = "insights"
os.makedirs(INSIGHTS_FOLDER, exist_ok=True)

DB_NAME = "WildlifeNew.db"

def fetch_all_data():
    """Fetch all wildlife observations from the database."""
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT species, confidence, region, date, latitude, longitude FROM species_data"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert columns to correct formats
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    return df

def plot_species_distribution(df):
    """📊 Top 10 Most Sighted Species."""
    plt.figure(figsize=(10, 5))
    species_counts = df["species"].value_counts().head(10)
    sns.barplot(y=species_counts.index, x=species_counts.values, palette="viridis")
    plt.xlabel("Number of Sightings")
    plt.ylabel("Species")
    plt.title("📊 Top 10 Most Sighted Species")

    species_chart = os.path.join(INSIGHTS_FOLDER, "species_distribution.png")
    plt.savefig(species_chart)
    plt.close()
    print(f"✅ Species Distribution Saved: {species_chart}")

def plot_sightings_trend(df):
    """📈 Wildlife Sightings Trend Over Time."""
    trend = df.groupby(df["date"].dt.date).size()

    plt.figure(figsize=(10, 5))
    plt.plot(trend.index, trend.values, marker="o", linestyle="-", color="b")
    plt.xlabel("Date")
    plt.ylabel("Sightings Count")
    plt.title("📈 Sightings Trend Over Time")

    trend_chart = os.path.join(INSIGHTS_FOLDER, "sightings_trend.png")
    plt.savefig(trend_chart)
    plt.close()
    print(f"✅ Sightings Trend Saved: {trend_chart}")

def plot_sightings_heatmap(df):
    """🔥 Heatmap of Wildlife Sightings."""
    if df[["latitude", "longitude"]].dropna().shape[0] > 1:
        plt.figure(figsize=(8, 5))
        sns.kdeplot(x=df["longitude"], y=df["latitude"], cmap="Reds", fill=True, alpha=0.6)
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("🔥 Sightings Heatmap")

        heatmap_chart = os.path.join(INSIGHTS_FOLDER, "sightings_heatmap.png")
        plt.savefig(heatmap_chart)
        plt.close()
        print(f"✅ Sightings Heatmap Saved: {heatmap_chart}")

def analyze_database():
    """Main function to analyze the database and generate insights."""
    df = fetch_all_data()

    if df.empty:
        print("❌ No data available in the database.")
        return

    plot_species_distribution(df)
    plot_sightings_trend(df)
    plot_sightings_heatmap(df)

    print("✅ Data Analysis Completed! Check the 'insights/' folder for charts.")

if __name__ == "__main__":
    analyze_database()
