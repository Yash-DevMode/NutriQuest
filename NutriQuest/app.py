import random
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Load Excel data
def load_food_data():
    df = pd.read_excel("food_data.xlsx")  # Load Excel file
    return dict(zip(df["Food"].str.lower(), df["GramsPerUnit"]))  # Convert to dictionary

@app.route("/", methods=["GET", "POST"])
def index():
    food_data = load_food_data()  # Load data from Excel
    if request.method == "POST":
        try:
            food = request.form.get("food").lower()  # Get selected food item
            quantity = int(request.form.get("quantity", "1"))  # Convert quantity to int
            
            if food in food_data:
                weight_in_grams = quantity * food_data[food]  # Calculate weight
                return redirect(url_for("result", food=food, weight=weight_in_grams))
            else:
                return "Invalid food selection."

        except ValueError:
            return "Invalid input. Please enter a valid quantity."

    return render_template("index.html", food_items=food_data.keys())

@app.route("/result")
def result():
    food = request.args.get("food", "Unknown")
    weight = request.args.get("weight", "0")
    return render_template("result.html", food=food, weight=weight)

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/quiz")
def quiz():
    random_food = df.sample(1)  # Pick a random food
    food_name = random_food["Food Item"].values[0]
    correct_answer = random_food["Calories per Gram"].values[0]

    return render_template("quiz.html", food=food_name, answer=correct_answer)
