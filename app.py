# Lotus Holiday Resort - Flask Application

from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os

from graph_generator import generate_graphs


# Flask App

app = Flask(__name__)


# Configuration

MODEL_FILE = "best_model.pkl"
DATASET_FILE = "dataset.csv"

EXTRA_GUEST_PRICE = 800

RESORT_WEBSITE = "https://lotusholidayresort.com/"


# Load Model

model = None

try:

    model = joblib.load(
        MODEL_FILE
    )

    print(
        "Best model loaded successfully."
    )

except Exception as error:

    print(
        "Model loading error:",
        error
    )


# Load Dataset

df = None

try:

    df = pd.read_csv(
        DATASET_FILE
    )

    print(
        "Dataset loaded successfully."
    )

except Exception as error:

    print(
        "Dataset loading error:",
        error
    )


# Generate Graphs Once

try:

    generate_graphs()

except Exception as error:

    print(
        "Graph generation error:",
        error
    )


# Home Page

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# Prediction

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        if model is None:

            return jsonify({
                "success": False,
                "error": "Best model is not available."
            }), 500


        # Get Form Data

        data = request.get_json()

        room_type = data.get(
            "Room_Type"
        )

        day_type = data.get(
            "Day_Type"
        )

        season = data.get(
            "Season"
        )

        guests = int(
            data.get(
                "Guests",
                1
            )
        )

        extra_guests = int(
            data.get(
                "Extra_Guests",
                0
            )
        )


        # Validate Room Type

        valid_rooms = [
            "AC Cottage",
            "AC Suite Room With Jacuzzi",
            "AC Executive Suite Room",
            "AC Deluxe Cottage",
            "AC Executive Rooms"
        ]

        if room_type not in valid_rooms:

            return jsonify({
                "success": False,
                "error": "Invalid room type."
            }), 400


        # Validate Day

        valid_days = [
            "Weekday",
            "Weekend"
        ]

        if day_type not in valid_days:

            return jsonify({
                "success": False,
                "error": "Invalid day type."
            }), 400


        # Validate Season

        valid_seasons = [
            "Normal",
            "Summer",
            "Monsoon",
            "Festival",
            "New Year"
        ]

        if season not in valid_seasons:

            return jsonify({
                "success": False,
                "error": "Invalid season."
            }), 400


        # Validate Guests

        if guests < 1:

            return jsonify({
                "success": False,
                "error": "Guests must be at least 1."
            }), 400


        # Validate Extra Guests

        if extra_guests < 0:

            return jsonify({
                "success": False,
                "error": "Extra guests cannot be negative."
            }), 400


        # Create Input DataFrame

        input_data = pd.DataFrame([
            {
                "Room_Type": room_type,
                "Day_Type": day_type,
                "Season": season,
                "Guests": guests,
                "Extra_Guests": extra_guests
            }
        ])


        # Predict Base Price

        prediction = model.predict(
            input_data
        )

        base_price = float(
            prediction[0]
        )


        # Extra Guest Charge

        extra_guest_charge = (
            extra_guests
            * EXTRA_GUEST_PRICE
        )


        # Final Estimated Total

        total_price = (
            base_price
            + extra_guest_charge
        )


        # Round Values

        base_price = round(
            base_price
        )

        extra_guest_charge = round(
            extra_guest_charge
        )

        total_price = round(
            total_price
        )


        # Return Result

        return jsonify({

            "success": True,

            "room_type": room_type,

            "day_type": day_type,

            "season": season,

            "guests": guests,

            "extra_guests": extra_guests,

            "base_price": base_price,

            "extra_guest_charge":
                extra_guest_charge,

            "total_price":
                total_price,

            "extra_guest_rate":
                EXTRA_GUEST_PRICE,

            "website":
                RESORT_WEBSITE
        })


    except Exception as error:

        print(
            "Prediction Error:",
            error
        )

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


# Dataset Information

@app.route(
    "/dataset-info"
)
def dataset_info():

    try:

        if df is None:

            return jsonify({
                "success": False,
                "error": "Dataset not found."
            }), 404


        return jsonify({

            "success": True,

            "rows": int(
                len(df)
            ),

            "columns": int(
                len(df.columns)
            ),

            "room_types":
                int(
                    df["Room_Type"]
                    .nunique()
                ),

            "day_types":
                int(
                    df["Day_Type"]
                    .nunique()
                ),

            "seasons":
                int(
                    df["Season"]
                    .nunique()
                ),

            "average_price":
                round(
                    float(
                        df["Base_Price"]
                        .mean()
                    ),
                    2
                ),

            "minimum_price":
                round(
                    float(
                        df["Base_Price"]
                        .min()
                    ),
                    2
                ),

            "maximum_price":
                round(
                    float(
                        df["Base_Price"]
                        .max()
                    ),
                    2
                )

        })


    except Exception as error:

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


# ML Summary

@app.route(
    "/ml-summary"
)
def ml_summary():

    try:

        comparison = pd.read_csv(
            "model_comparison.csv"
        )

        cross_validation = pd.read_csv(
            "cross_validation.csv"
        )

        gridsearch = pd.read_csv(
            "gridsearch_result.csv"
        )

        eda = pd.read_csv(
            "eda_summary.csv"
        )

        summary = {

            "success": True,

            "comparison":
                comparison.to_dict(
                    orient="records"
                ),

            "cross_validation":
                cross_validation.to_dict(
                    orient="records"
                ),

            "gridsearch":
                gridsearch.to_dict(
                    orient="records"
                ),

            "eda":
                eda.to_dict(
                    orient="records"
                )

        }

        return jsonify(
            summary
        )


    except Exception as error:

        print(
            "ML Summary Error:",
            error
        )

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


# Resort Information

@app.route(
    "/resort-info"
)
def resort_info():

    return jsonify({

        "name":
            "Lotus Holiday Resort",

        "location":
            "Diveagar, Maharashtra",

        "website":
            RESORT_WEBSITE,

        "rooms":
            22,

        "restaurant":
            True,

        "extra_guest_charge":
            EXTRA_GUEST_PRICE

    })


# Run Application

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )