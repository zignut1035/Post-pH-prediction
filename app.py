from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load both models
model_1 = joblib.load("first_gradient_no_air_-0.1.pkl")
model_2 = joblib.load("gradient_boost_compatible_2 (1).pkl")

# Define a mapping for fruit types (adjust based on your training data)
fruit_mapping = {
    "Blueberry": 1,
    "Black currant": 2,
    "Lingonberry": 3,
    "Sea buckthorn": 4
}

def predict_pH(model, feature_values):
    # Convert the feature values to a list and remove column names
    feature_values_list = list(feature_values.values())
    feature_df = pd.DataFrame([feature_values_list])
    predicted_pH = model.predict(feature_df)[0]
    return predicted_pH

@app.route("/")
def home():
    return render_template("fermented.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        # Extract input values
        fruit_name = data.get("fruit")
        sugar = data.get("sugar")
        temp = data.get("temperature")
        time_hours = data.get("time")
        ph_before = data.get("ph_before")
        aeration = data.get("aeration")

        # Validate inputs
        if not all([fruit_name, sugar, temp, time_hours, ph_before] if model_1 else [fruit_name, sugar, temp, time_hours, ph_before, aeration]):
            return jsonify({"error": "Missing required input fields."}), 400

        try:
            sugar = float(sugar)
            temp = float(temp)
            time_hours = float(time_hours)
            ph_before = float(ph_before)
            aeration = float(aeration) if aeration is not None else None
        except ValueError:
            return jsonify({"error": "Invalid number format. Please ensure all fields are numeric."}), 400

        if fruit_name not in fruit_mapping:
            return jsonify({"error": "Invalid fruit type. Choose from: Blueberry, Black currant, Lingonberry, Sea buckthorn"}), 400

        fruit_numeric = fruit_mapping[fruit_name]

        # Feature vector for model_1 (without aeration)
        feature_values_model_1 = {
            'Fruit Numeric': fruit_numeric,
            'Sugar g/L': sugar,
            'Temp C': temp,
            'Time hours': time_hours,
            'Numerical pH before ferm': ph_before
        }

        # Feature vector for model_2 (with aeration)
        feature_values_model_2 = {
            'Fruit Numeric': fruit_numeric,
            'Sugar g/L': sugar,
            'Temp C': temp,
            'Time hours': time_hours,
            'Numerical pH before ferm': ph_before,
            'Aeration': aeration
        }

        # Get predictions from both models
        prediction_1 = predict_pH(model_1, feature_values_model_1)
        prediction_2 = predict_pH(model_2, feature_values_model_2)

        # Round results for readability
        return jsonify({
            "predicted_pH_linear": round(prediction_1, 3),
            "predicted_pH_boost": round(prediction_2, 3)
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
