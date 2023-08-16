import pandas as pd
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

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

        bmi_category = calculate_bmi_category(height, weight)

        return render_template('results.html',bmi_category=bmi_category)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
