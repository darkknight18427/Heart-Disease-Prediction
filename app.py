from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained Random Forest pipeline
import joblib
import os
from pathlib import Path

# Get the directory where app.py is located
BASE_DIR = Path(__file__).resolve().parent

# Build path to the model
model_path = BASE_DIR / 'Model' / 'model.pkl'

# Load the model
model = joblib.load(model_path)


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    probability = None

    if request.method == "POST":

        # Collect the 12 features used by the final model
        data = {
            "age": float(request.form["age"]),
            "sex": int(request.form["sex"]),
            "cp": int(request.form["cp"]),
            "trestbps": float(request.form["trestbps"]),
            "chol": float(request.form["chol"]),
            "restecg": int(request.form["restecg"]),
            "thalach": float(request.form["thalach"]),
            "exang": int(request.form["exang"]),
            "oldpeak": float(request.form["oldpeak"]),
            "slope": int(request.form["slope"]),
            "ca": int(request.form["ca"]),
            "thal": int(request.form["thal"])
        }

        # Create DataFrame
        input_data = pd.DataFrame([data])

        # Make prediction
        result = model.predict(input_data)[0]

        # Get probability if available
        probability = model.predict_proba(input_data)[0][1] * 100

        if result == 1:
            prediction = "Higher likelihood of heart disease"
        else:
            prediction = "Lower likelihood of heart disease"

    return render_template(
        "index.html",
        prediction=prediction,
        probability=probability
    )


if __name__ == "__main__":
    app.run(debug=True)