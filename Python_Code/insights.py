import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime
import matplotlib
matplotlib.use('Agg')  # Ensure no GUI is needed for plots

# ✅ Ensure static2 directory exists
INSIGHTS_FOLDER = "static2"
os.makedirs(INSIGHTS_FOLDER, exist_ok=True)

def fetch_data(species_name=None, db_name="WildlifeNew.db"):
    """
    Fetch all species data from the database.
    If a species is provided, filter data for that species.
    """
    conn = sqlite3.connect(db_name)
    query = "SELECT species, confidence, region, date, latitude, longitude FROM species_data"
    
    if species_name:
        query += " WHERE LOWER(species) = ?"
        df = pd.read_sql_query(query, conn, params=(species_name.lower(),))
    else:
        df = pd.read_sql_query(query, conn)
    
    conn.close()
    
    # Ensure proper data types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    return df

def generate_insights(species_name=None):
    """
    Generate insights and save charts.
    """
    df = fetch_data(species_name)

    if df.empty:
        return {"error": f"No data found for {'species: ' + species_name if species_name else 'database'}"}

    insights = {}
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Unique filenames

    # 📈 **Trend Chart**
    trend = df.groupby(df["date"].dt.date).size()
    if not trend.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(trend.index, trend.values, marker="o", linestyle="-", color="b")
        plt.xlabel("Date")
        plt.ylabel("Sightings Count")
        plt.title(f"Sightings Trend {'for ' + species_name if species_name else 'Over Time'}")
        trend_chart = f"trend_{species_name or 'all'}_{timestamp}.png"
        plt.savefig(os.path.join(INSIGHTS_FOLDER, trend_chart))
        plt.close()
        insights["trend_chart"] = trend_chart
    else:
        insights["trend_chart"] = None

    # 🔥 **Heatmap Chart**
    if df[["latitude", "longitude"]].dropna().shape[0] > 1:
        plt.figure(figsize=(8, 5))
        sns.kdeplot(x=df["longitude"], y=df["latitude"], cmap="Reds", fill=True, alpha=0.6)
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title(f"Sightings Heatmap {'for ' + species_name if species_name else ''}")
        heatmap_chart = f"heatmap_{species_name or 'all'}_{timestamp}.png"
        plt.savefig(os.path.join(INSIGHTS_FOLDER, heatmap_chart))
        plt.close()
        insights["heatmap_chart"] = heatmap_chart
    else:
        insights["heatmap_chart"] = None

    return insights
