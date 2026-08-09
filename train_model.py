# Train Best Model

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor


# Configuration

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


DATASET_FILE = os.path.join(
    BASE_DIR,
    "dataset.csv"
)


MODEL_FILE = os.path.join(
    BASE_DIR,
    "best_model.pkl"
)


# Load Dataset

if not os.path.exists(
    DATASET_FILE
):

    raise FileNotFoundError(
        "dataset.csv was not found."
    )


df = pd.read_csv(
    DATASET_FILE
)


print(
    "Dataset loaded successfully."
)


print(
    "Dataset shape:",
    df.shape
)


# Data Cleaning

df = df.drop_duplicates()


df["Guests"] = pd.to_numeric(
    df["Guests"],
    errors="coerce"
)


df["Extra_Guests"] = pd.to_numeric(
    df["Extra_Guests"],
    errors="coerce"
)


df["Base_Price"] = pd.to_numeric(
    df["Base_Price"],
    errors="coerce"
)


df = df.dropna(
    subset=[
        "Room_Type",
        "Day_Type",
        "Season",
        "Guests",
        "Extra_Guests",
        "Base_Price"
    ]
)


# Features

features = [

    "Room_Type",

    "Day_Type",

    "Season",

    "Guests",

    "Extra_Guests"
]


target = "Base_Price"


X = df[
    features
]


y = df[
    target
]


# Train Test Split

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42
)


# Feature Groups

categorical_features = [

    "Room_Type",

    "Day_Type",

    "Season"
]


numeric_features = [

    "Guests",

    "Extra_Guests"
]


# Categorical Pipeline

categorical_pipeline = Pipeline(

    steps=[

        (
            "imputer",

            SimpleImputer(
                strategy="most_frequent"
            )
        ),

        (
            "encoder",

            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)


# Numeric Pipeline

numeric_pipeline = Pipeline(

    steps=[

        (
            "imputer",

            SimpleImputer(
                strategy="median"
            )
        ),

        (
            "scaler",

            StandardScaler()
        )
    ]
)


# Preprocessor

preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",

            categorical_pipeline,

            categorical_features
        ),

        (
            "numeric",

            numeric_pipeline,

            numeric_features
        )
    ]
)


# Random Forest Pipeline

random_forest_pipeline = Pipeline(

    steps=[

        (
            "preprocessor",

            preprocessor
        ),

        (
            "model",

            RandomForestRegressor(

                random_state=42,

                n_jobs=-1
            )
        )
    ]
)


# GridSearchCV Parameters

param_grid = {

    "model__n_estimators": [

        50,

        100,

        150
    ],

    "model__max_depth": [

        None,

        5,

        10,

        15
    ],

    "model__min_samples_split": [

        2,

        5
    ],

    "model__min_samples_leaf": [

        1,

        2
    ]
}


# GridSearchCV

print()

print(
    "Starting GridSearchCV..."
)


grid_search = GridSearchCV(

    estimator=random_forest_pipeline,

    param_grid=param_grid,

    cv=5,

    scoring="r2",

    n_jobs=-1
)


grid_search.fit(

    X_train,

    y_train
)


# Display Best Parameters

print()

print(
    "Best Parameters:"
)


print(
    grid_search.best_params_
)


print()

print(
    "Best Cross Validation R2:"
)


print(
    round(
        grid_search.best_score_,
        4
    )
)


# Save Best Model

best_model = (
    grid_search.best_estimator_
)


joblib.dump(

    best_model,

    MODEL_FILE
)


print()

print(
    "Best model saved successfully."
)


print(
    "File:",
    MODEL_FILE
)


# Test Prediction

sample_data = pd.DataFrame(

    [

        {

            "Room_Type":
                "AC Cottage",

            "Day_Type":
                "Weekday",

            "Season":
                "Normal",

            "Guests":
                2,

            "Extra_Guests":
                0
        }
    ]
)


prediction = best_model.predict(

    sample_data
)


print()

print(
    "Sample Prediction"
)


print(
    "Room Type: AC Cottage"
)


print(
    "Day Type: Weekday"
)


print(
    "Season: Normal"
)


print(
    "Guests: 2"
)


print(
    "Extra Guests: 0"
)


print(
    "Predicted Base Price: ₹",
    round(
        float(
            prediction[0]
        ),
        2
    )
)


print()

print(
    "Training completed successfully."
)