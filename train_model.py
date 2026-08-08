import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("dataset.csv")

room_encoder = LabelEncoder()
day_encoder = LabelEncoder()
season_encoder = LabelEncoder()

df["Room_Type"] = room_encoder.fit_transform(df["Room_Type"])
df["Day_Type"] = day_encoder.fit_transform(df["Day_Type"])
df["Season"] = season_encoder.fit_transform(df["Season"])

joblib.dump(room_encoder, "room_encoder.pkl")
joblib.dump(day_encoder, "day_encoder.pkl")
joblib.dump(season_encoder, "season_encoder.pkl")

X = df[
    [
        "Room_Type",
        "Day_Type",
        "Season",
        "Guests",
        "Extra_Guests"
    ]
]

y = df["Base_Price"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print()

print("MAE :", round(mean_absolute_error(y_test, predictions), 2))

print("R² :", round(r2_score(y_test, predictions), 4))

joblib.dump(model, "model.pkl")

print()

print("Model Saved Successfully")