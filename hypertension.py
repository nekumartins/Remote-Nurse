import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
import joblib

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.secret_key = secret_key


model = joblib.load('./models/hypertension_model.pkl') 

def detect_hypertension(age, cp, trestbps, chol, fbs, thalach, exang, oldpeak, thal):
    # Create a feature array for prediction
    features = [[age, cp, trestbps, chol, fbs, thalach, exang, oldpeak, thal]]
    prediction = model.predict(features)
    return prediction[0]

def calculate_bmi_category(height, weight):
    bmi = weight / (height / 100) ** 2

    if bmi < 18.5:
        bmi_category = 'Underweight'
    elif 18.5 <= bmi <= 24.9:
        bmi_category = 'Normal'
    elif 25.0 <= bmi <= 29.9:
        bmi_category = 'Overweight'
    elif 30.0 <= bmi <= 34.9:
        bmi_category = 'Obese class I'
    elif 35.0 <= bmi <= 39.9:
        bmi_category = 'Obese class II'
    else:
        bmi_category = 'Obese class III'


    return bmi_category




if __name__ == '__main__':
    app.run(debug=True)
