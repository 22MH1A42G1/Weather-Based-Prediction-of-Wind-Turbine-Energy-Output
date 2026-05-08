import numpy as np
import joblib
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained model
model = joblib.load("power_prediction.sav")

# ---------- LANDING PAGE ----------
@app.route('/')
def intro():
    """Render the introduction/landing page"""
    return render_template("intro.html")

# ---------- PREDICT PAGE ----------
@app.route('/predict')
def predict_page():
    """Render the prediction page"""
    return render_template("predict.html")

# ---------- WEATHER API ----------
@app.route('/windapi', methods=['POST'])
def windapi():
    """Fetch real-time weather data from OpenWeatherMap API"""
    city = request.form.get('city')
    api_key = "2d8ade70e9d0038838d19578f27e04db"

    try:
        url = "http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_key
        data = requests.get(url)
        data = data.json()

        # Extract weather information
        temp = str(data['main']['temp'])+" °C"
        humid = str(data['main']['humidity'])+" %"
        pressure = str(data['main']['pressure'])+" mmHG"
        speed = str(data['wind']['speed'])+" m/s"

        return render_template(
            "predict.html",
            temp=temp,
            humid=humid,
            pressure=pressure,
            speed=speed
        )
    except Exception as e:
        return render_template(
            "predict.html",
            error="Error fetching weather data. Please check the city name and try again."
        )

# ---------- PREDICTION RESULT PAGE ----------
@app.route('/result', methods=['POST'])
def result():
    """Make energy prediction based on input features"""
    try:
        x_test = [[float(x) for x in request.form.values()]]
        prediction = model.predict(x_test)
        output = prediction[0]
        
        return render_template(
            "predict.html",
            prediction_text="The energy predicted is {:.2f} kW".format(output)
        )
    except Exception as e:
        return render_template(
            "predict.html",
            error="Error in prediction. Please check your input values."
        )

# ---------- SERVER STARTUP ----------
if __name__ == "__main__":
    print("Starting Wind Energy Prediction Application...")
    print("Navigate to http://localhost:5000 in your browser")
    app.run(debug=True)

