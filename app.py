from flask import Flask, render_template, request, redirect, url_for, flash
from cs50 import SQL
from hypertension import calculate_bmi_category
import pandas as pd 
import secrets


hypertension_df = pd.read_csv("hypertension.csv")

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
db = SQL("sqlite:///hypertension.db")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get user input from the form
        age = request.form.get("age")
        gender = request.form.get("gender")
        med_history = request.form.get("med_history")
        systolic_bp = request.form.get("systolic_bp")
        diastolic_bp = request.form.get("diastolic_bp")
        weight = request.form.get("weight")
        height = request.form.get("height")

        # Validate user input
        if not age or not gender or not med_history or not systolic_bp or not diastolic_bp:
            flash("Please fill out all fields.", "error")
            return redirect(url_for("home"))

        if not age.isdigit() or not systolic_bp.isdigit() or not diastolic_bp.isdigit():
            flash("Please enter valid numeric data.", "error")
            return redirect(url_for("home"))

        if int(age) < 0 or int(age) > 120 or int(systolic_bp) < 0 or int(diastolic_bp) < 0:
            flash("Please enter data within a reasonable range.", "error")
            return redirect(url_for("home"))

        # Calculate hypertension risk based on user input
        hypertension_risk_threshold = (130, 80)
        hypertension_risk = detect_hypertension(med_history, systolic_bp, diastolic_bp, hypertension_risk_threshold)

        # Store user input and hypertension risk in database
        db.execute("INSERT INTO users (age, gender, med_history, systolic_bp, diastolic_bp, hypertension_risk) VALUES (?, ?, ?, ?, ?, ?)", 
                   age, gender, med_history, systolic_bp, diastolic_bp, hypertension_risk)

        # Redirect to results page
        return redirect(url_for("results"))

    return render_template("home.html")

@app.route("/results")
def results():
    if request.method == 'POST':
        height = float(request.form['height'])
        weight = float(request.form['weight'])

    bmi_category = calculate_bmi_category(height, weight)

    return render_template('results.html',bmi_category=bmi_category)





@app.route('/')
def index():
    hypertension = pd.read_csv('hypertension_data.csv') 


    import joblib
    model = joblib.load('./models/hypertension_model.pkl') 

    # Use the model to predict hypertension
    features = ['age', 'cp', 'trestbps', 'chol', 'fbs', 'thalach', 'exang', 'oldpeak', 'thal']
    X = hypertension[features].values
    predictions = model.predict(X)

    # Identify individuals at risk of hypertension
    hypertensions = []

    for i in range(len(hypertension)):
        if predictions[i] == 1: 
            person = hypertension.iloc[i]  # Access the row using iloc
            hypertensions.append({"age": person['age'], "sex": person['sex'], "cp": person['cp'], "trestbps": person['trestbps'], "chol": person['chol'], "thalach": person['thalach']})

    return render_template("index.html", hypertensions=hypertensions)      



if __name__ == "__main__":
    app.run(debug=True)
