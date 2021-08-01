from flask import Flask, render_template, request
import pickle
from datetime import date

app = Flask(__name__, template_folder='template')
r_model = pickle.load(open('predict_model.pkl', 'rb'))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=['POST'])
def predict():
    Kilometers_Driven = int(request.form["Kilometers_Driven"])
    Mileage = float(request.form["Mileage"])
    Engine = float(request.form["Engine"])
    Power = float(request.form["Power"])
    Seats = int(request.form["Seats"])
    pyear = int(request.form["pyear"])
    today = date.today()
    Age = today.year - pyear
    Fuel_type = request.form["Fuel_Type"]
    Diesel = 0
    Electric = 0
    LPG = 0
    Petrol = 0
    if Fuel_type == 'Diesel':
        Diesel = 1
    elif Fuel_type == 'Electric':
        Electric = 1
    elif Fuel_type == 'LPG':
        LPG = 1
    elif Fuel_type == 'Petrol':
        Petrol = 1
    Transmission = request.form["Transmission_Type"]
    Manual = 0
    if Transmission == 'Manual':
        Manual = 1
    else:
        Manual = 0
    Owner = request.form["Owner"]
    Four_Above = 0
    sec = 0
    third = 0
    if Owner == 'Second':
        sec = 1
    elif Owner == 'Third':
        third = 1
    elif Owner == 'Fourth&Above':
        Four_Above = 0
    features = [
        [Kilometers_Driven, Mileage, Engine, Power, Seats, Age, Diesel, Electric, LPG, Petrol, Manual, Four_Above, sec,
         third]]
    prediction = r_model.predict(features)
    output = round(prediction[0], 2)
    return render_template("index.html", prediction_text="price for your car:{} Lakh".format(float(output)))


if __name__ == "__main__":
    app.run(debug=True)
