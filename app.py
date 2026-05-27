import streamlit as st
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        "index.html",
        prediction_text=None,
        rent_text=None,
        error=None
    )


@app.route('/predict', methods=['POST'])
def predict():

    try:

        area_type = request.form["area_type"]
        location = request.form["location"]
        house_type = request.form["house_type"]

        sqft = int(request.form["sqft"])
        bedrooms = int(request.form["bedrooms"])
        age = int(request.form["age"])

        # realistic ₹/sqft
        area_price = {
            "Urban": 5500,
            "Semi Urban": 3800,
            "Rural": 2200
        }

        house_factor = {
            "Apartment": 1.00,
            "Independent House": 1.10,
            "Villa": 1.25,
            "Bungalow": 1.30
        }

        location_factor = {
            "Mumbai": 1.40,
            "Pune": 1.20,
            "Kolhapur": 1.00,
            "Ichalkaranji": 0.85,
            "Sangli": 0.80
        }

        base_price = (
            sqft
            * area_price[area_type]
            * house_factor[house_type]
            * location_factor[location]
        )

        bedroom_bonus = bedrooms * 150000
        age_discount = age * 70000

        final_price = (
            base_price
            + bedroom_bonus
            - age_discount
        )

        if final_price < 1000000:
            final_price = 1000000

        monthly_rent = round(final_price * 0.004)

        final_price = round(final_price)

        return render_template(
            "index.html",
            prediction_text=f"{final_price:,}",
            rent_text=f"{monthly_rent:,}",
            error=None
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text=None,
            rent_text=None,
            error=f"Error: {str(e)}"
        )


if __name__ == "__main__":
    app.run()
