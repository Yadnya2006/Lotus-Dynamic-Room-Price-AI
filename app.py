from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
from graph_generator import generate_all_graphs

app = Flask(__name__)

# Load Model
model = joblib.load("model.pkl")

# Load Encoders
room_encoder = joblib.load("room_encoder.pkl")
day_encoder = joblib.load("day_encoder.pkl")
season_encoder = joblib.load("season_encoder.pkl")


@app.route("/")
def home():

    return render_template(

        "index.html",

        room_types=list(room_encoder.classes_),

        day_types=list(day_encoder.classes_),

        seasons=list(season_encoder.classes_)

    )


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        room_type = data["room_type"]
        day_type = data["day_type"]
        season = data["season"]

        guests = int(data["guests"])
        extra_guests = int(data["extra_guests"])

        room = room_encoder.transform([room_type])[0]
        day = day_encoder.transform([day_type])[0]
        season_value = season_encoder.transform([season])[0]

        input_df = pd.DataFrame({

            "Room_Type": [room],
            "Day_Type": [day],
            "Season": [season_value],
            "Guests": [guests],
            "Extra_Guests": [extra_guests]

        })

        base_price = int(model.predict(input_df)[0])

        extra_charge = extra_guests * 800

        final_price = base_price + extra_charge

        if season.lower() == "festival":

            demand = "High"
            occupancy = 95
            trend = "Increasing"

        elif day_type.lower() == "weekend":

            demand = "Medium"
            occupancy = 85
            trend = "Stable"

        else:

            demand = "Low"
            occupancy = 70
            trend = "Normal"

        confidence = 96

        recommendation = (
            f"AI recommends ₹{final_price} for this booking because "
            f"the selected room, season, day type and guest count "
            f"indicate {demand.lower()} demand with approximately "
            f"{occupancy}% occupancy."
        )

        # Generate graphs
        generate_all_graphs(
            base_price,
            extra_charge,
            final_price,
            guests,
            extra_guests
        )

        return jsonify({

            "base_price": base_price,

            "extra_charge": extra_charge,

            "final_price": final_price,

            "demand": demand,

            "occupancy": occupancy,

            "trend": trend,

            "confidence": confidence,

            "recommendation": recommendation,

            "price_graph": "/static/graphs/price_graph.png",

            "guest_graph": "/static/graphs/guest_graph.png",

            "occupancy_graph": "/static/graphs/occupancy_graph.png"

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


if __name__ == "__main__":

    app.run(debug=True)