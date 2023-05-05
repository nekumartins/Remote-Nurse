import numpy as np
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
secret_key = secrets.token_hex(16) # generates a 32-character random string
app.secret_key = secret_key

def detect_hypertension(family_history, systolic_bp, diastolic_bp, hypertension_risk_threshold=(0, 0)):
    # Check if the individual has a family history of hypertension
    if family_history.lower() == "yes":
        family_history_int = 2
    else:
        family_history_int = 0

    # Check if the individual's blood pressure is above the hypertension risk threshold
    if int(systolic_bp) > hypertension_risk_threshold[0] and int(diastolic_bp) > hypertension_risk_threshold[1]:
        return True

    if family_history_int >= 2:
        return True

    # Otherwise, the individual is not at risk of hypertension
    return False


def calculate_hypertension_risk(age, gender, height, weight, family_history, systolic_bp, diastolic_bp):
    # Define the hypertension risk threshold based on age and gender
    if gender == 'male':
        if age <= 64:
            hypertension_risk_threshold = (130, 80)
        else:
            hypertension_risk_threshold = (140, 90)
    else:
        if age <= 64:
            hypertension_risk_threshold = (125, 80)
        else:
            hypertension_risk_threshold = (135, 90)

    hypertension_risk = 0

    # Calculate the body mass index (BMI) using height and weight
    bmi = weight / (height / 100) ** 2

    # Calculate the hypertension risk using the BMI and other factors
    if bmi < 18.5:
        bmi_category = 'Underweight'
    elif 18.5 <= bmi <= 24.9:
        bmi_category = 'Normal'
    elif 25.0 <= bmi <= 29.9:
        bmi_category = 'Overweight'
        hypertension_risk = 1
    elif 30.0 <= bmi <= 34.9:
        bmi_category = 'Obese class I'
        hypertension_risk = 1
    elif 35.0 <= bmi <= 39.9:
        bmi_category = 'Obese class II'
        hypertension_risk = 2
    else:
        bmi_category = 'Obese class III'
        hypertension_risk = 2

    # Check if the individual is at risk of hypertension based on family history and blood pressure
    if detect_hypertension(family_history, systolic_bp, diastolic_bp, hypertension_risk_threshold):
        hypertension_risk += 1

    return bmi_category, hypertension_risk



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        age = int(request.form['age'])
        gender = request.form['gender']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        med_history = request.form['med_history']
        systolic_bp = int(request.form['systolic_bp'])
        diastolic_bp = int(request.form['diastolic_bp'])

        hypertension_risk = calculate_hypertension_risk(age, gender, height, weight, med_history, systolic_bp, diastolic_bp)

        return render_template('results.html', hypertension_risk=hypertension_risk)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
