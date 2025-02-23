from flask import Flask, request, jsonify, send_from_directory
import os
from databasework import Database  # ✅ Ensure this is correct
from species_prediction import predict_species  # ✅ Ensure this file exists and is named correctly
from insights import generate_database_insights
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
db = Database()  # ✅ Ensure this correctly connects to SQLite

# ✅ Serve Frontend HTML Page
@app.route("/")
def home():
    return send_from_directory(".", "page.html")

# ✅ Predict Species & Store Data in Database
@app.route("/predi", methods=["POST"])
def upload_and_predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    # ✅ Get additional data from the request (handle missing values)
    region = request.form.get("region", "Unknown")
    date = request.form.get("date", "Not Provided")
    time = request.form.get("time", "Not Provided")
    latitude = request.form.get("latitude", "0.0")
    longitude = request.form.get("longitude", "0.0")

    # ✅ Ensure Prediction Model Works
    try:
        species, confidence = predict_species(image_path)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    # ✅ Store Data in SQLite (WITHOUT IMAGE PATH)
    try:
        db.insert_data(species, confidence, region, date, time, latitude, longitude)
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({
        "message": "Prediction stored successfully!",
        "species": species,
        "confidence": f"{confidence:.2f}%",
        "region": region,
        "date": date,
        "time": time,
        "latitude": latitude,
        "longitude": longitude
    })
@app.route("/insights", methods=["GET"])
def get_database_insights():
    insights = generate_database_insights()
    return jsonify(insights)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
