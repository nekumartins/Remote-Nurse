from flask import Flask, render_template, request, redirect, url_for, flash
from cs50 import SQL
from hypertension import detect_hypertension, calculate_hypertension_risk
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
    # Get hypertension risk from database
     #= db.execute("SELECT hypertension_risk FROM users ORDER BY id DESC LIMIT 1")[0]["hypertension_risk"]
     
    bmi_category, hypertension_risk = calculate_hypertension_risk(age, gender, height, weight, med_history, systolic_bp, diastolic_bp)
    return render_template("results.html", hypertension_risk=hypertension_risk, bmi_category=bmi_category)





@app.route('/')
def index():
    # Identify individuals at risk of hypertension
    hypertension = []

    for i in range(n_individuals):
        if systolic_bp[i] > hypertension_risk_threshold or diastolic_bp[i] > hypertension_risk_threshold:
            hypertension.append({"age": age[i], "gender": gender[i], "med_history": med_history[i], "systolic_bp": systolic_bp[i], "diastolic_bp": diastolic_bp[i], "heart_rate": heart_rate[i]})

    return render_template("index.html", hypertension=hypertension)



if __name__ == "__main__":
    app.run(debug=True)
