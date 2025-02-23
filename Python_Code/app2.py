from flask import Flask, request, jsonify, send_from_directory, render_template_string
import os
import sqlite3
from species_prediction import predict_species
from insights import generate_insights  # Ensure `generate_insights()` is defined

# ✅ Set the correct static folder path
STATIC_FOLDER = r"C:\Users\Hp\Desktop\rguhack25\static2"
UPLOAD_FOLDER = "uploads"

# ✅ Ensure directories exist
os.makedirs(STATIC_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder=STATIC_FOLDER)

# ✅ Serve Frontend Page
@app.route("/")
def home():
    return send_from_directory(".", "page.html")

# ✅ Predict Species & Store Data
@app.route("/predi", methods=["POST"])
def upload_and_predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    # ✅ Predict Species
    species, confidence = predict_species(image_path)

    # ✅ Store Prediction in Database
    conn = sqlite3.connect("WildlifeNew.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO species_data (species, confidence, region, date, time, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (species.lower(), confidence, "Unknown", "Not Provided", "Not Provided", "0.0", "0.0"))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Prediction stored!",
        "species": species,
        "confidence": f"{confidence:.2f}%",
        "insight_url": f"/insights?species={species}"
    })

# ✅ Generate Database & Species Insights
@app.route("/insights")
def get_insights():
    species_name = request.args.get("species", "").strip().lower()
    insights = generate_insights(species_name if species_name else None)

    if "error" in insights:
        return jsonify({"error": insights["error"]}), 404

    return render_template_string('''
        <h1>📊 Wildlife Insights</h1>
        
        {% if insights['trend_chart'] %}
            <h2>📈 Sightings Trend {{ 'for ' + species if species else 'Over Time' }}</h2>
            <img src="{{ url_for('serve_static', filename=insights['trend_chart']) }}" width="600">
        {% else %}
            <p>No trend data available.</p>
        {% endif %}

        {% if insights['heatmap_chart'] %}
            <h2>🔥 Sightings Heatmap {{ 'for ' + species if species else '' }}</h2>
            <img src="{{ url_for('serve_static', filename=insights['heatmap_chart']) }}" width="600">
        {% else %}
            <p>No heatmap data available.</p>
        {% endif %}

        <br><br>
        <a href="/">⬅️ Back to Upload</a>
    ''', insights=insights, species=species_name)

# ✅ Serve Static Images from `static2`
@app.route("/static2/<path:filename>")
def serve_static(filename):
    return send_from_directory(STATIC_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
