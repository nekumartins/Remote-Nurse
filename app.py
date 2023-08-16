from flask import Flask, render_template, request, redirect, url_for, flash
from hypertension import calculate_bmi_category, detect_hypertension
import pandas as pd 
import secrets
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


hypertension_df = pd.read_csv("hypertension_data.csv")

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    gender = Column(Integer)
    cp = Column(Integer)
    trestbps = Column(Integer)
    chol = Column(Integer)
    fbs = Column(Integer)
    thalach = Column(Integer)
    exang = Column(Integer)
    oldpeak = Column(Float)
    thal = Column(Integer)
    hypertension_risk = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)

engine = create_engine("sqlite:///hypertension.db")
db = scoped_session(sessionmaker(bind=engine))

Base.metadata.create_all(engine)

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get user input from the form
        age = int(request.form.get("age"))
        gender = int(request.form.get("gender"))
        cp = int(request.form.get("cp"))
        trestbps = int(request.form.get("trestbps"))
        chol = int(request.form.get("chol"))
        fbs = int(request.form.get("fbs"))
        thalach = int(request.form.get("thalach"))
        exang = int(request.form.get("exang"))
        oldpeak = float(request.form.get("oldpeak"))
        thal = int(request.form.get("thal"))
        height = int(request.form.get("height"))
        weight = int(request.form.get("weight"))

        # Validate user input
        if age < 0 or age > 120 or trestbps < 0 or chol < 0:
            flash("Please enter data within a reasonable range.", "error")
            return redirect(url_for("home"))

        # Calculate hypertension risk based on user input
        hypertension_risk = detect_hypertension(age, cp, trestbps, chol, fbs, thalach, exang, oldpeak, thal)

        # Store user input and hypertension risk in the database
        db.execute("""
    INSERT INTO users (age, gender, cp, trestbps, chol, fbs, thalach, exang, oldpeak, thal, hypertension_risk, height, weight)
    VALUES (:age, :gender, :cp, :trestbps, :chol, :fbs, :thalach, :exang, :oldpeak, :thal, :hypertension_risk, :height, :weight)
    """,
    {"age": age, "gender": gender, "cp": cp, "trestbps": trestbps, "chol": chol,
     "fbs": fbs, "thalach": thalach, "exang": exang, "oldpeak": oldpeak, "thal": thal,
     "hypertension_risk": hypertension_risk, "height": height, "weight": weight}
)
        db.commit()

        # Redirect to results page
        return redirect(url_for("results"))

    return render_template("home.html")

@app.route("/results")
def results():
    # Retrieve user data from the database
    user_data = db.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1").fetchone()

    if user_data is None:
        flash("No user data found.", "error")
        return redirect(url_for("home"))

    # Get individual features from the user data
    age = user_data.age
    gender = "Male" if user_data.gender == 0 else "Female"
    cp = user_data.cp
    trestbps = user_data.trestbps
    chol = user_data.chol
    fbs = "Yes" if user_data.fbs == 1 else "No"
    thalach = user_data.thalach
    exang = "Yes" if user_data.exang == 1 else "No"
    oldpeak = user_data.oldpeak
    thal = user_data.thal

    # Get hypertension risk prediction
    hypertension_risk = user_data.hypertension_risk

    height = user_data.height
    weight = user_data.weight

    # Get BMI category
    bmi_category = calculate_bmi_category(height, weight) 

    return render_template("results.html", age=age, gender=gender, cp=cp, trestbps=trestbps, chol=chol,
                           fbs=fbs, thalach=thalach, exang=exang, oldpeak=oldpeak, thal=thal,
                           hypertension_risk=hypertension_risk, bmi_category=bmi_category)



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

    for i in range(50):
        if predictions[i] == 1: 
            person = hypertension.iloc[i]  # Access the row using iloc
            hypertensions.append({"age": person['age'], "sex": person['sex'], "cp": person['cp'], "trestbps": person['trestbps'], "chol": person['chol'], "thalach": person['thalach']})

    return render_template("index.html", hypertensions=hypertensions)      



if __name__ == "__main__":
    app.run(debug=True)
