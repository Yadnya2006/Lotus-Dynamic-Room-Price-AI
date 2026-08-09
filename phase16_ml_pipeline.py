# ============================================================
# PHASE 16 - MACHINE LEARNING PIPELINE
# Lotus Holiday Resort
# ============================================================

import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\n======================================")
print("LOTUS HOLIDAY RESORT - ML PIPELINE")
print("======================================")

df = pd.read_csv("dataset.csv")

print("\nDataset Loaded Successfully")
print("Dataset Shape:", df.shape)


# ============================================================
# 2. DATA CLEANING
# ============================================================

print("\nData Cleaning")

before = len(df)

df = df.drop_duplicates()

required_columns = [
    "Room_Type",
    "Day_Type",
    "Season",
    "Guests",
    "Extra_Guests",
    "Base_Price"
]

df = df.dropna(subset=required_columns)

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

df = df.dropna()

after = len(df)

print("Rows Before Cleaning:", before)
print("Rows After Cleaning:", after)


# ============================================================
# 3. EDA
# ============================================================

print("\nExploratory Data Analysis")

print("\nDataset Information")
print(df.info())

print("\nDescriptive Statistics")
print(df.describe())

print("\nRoom Type Distribution")
print(df["Room_Type"].value_counts())

print("\nDay Type Distribution")
print(df["Day_Type"].value_counts())

print("\nSeason Distribution")
print(df["Season"].value_counts())


# ============================================================
# 4. SAVE EDA SUMMARY
# ============================================================

eda_summary = pd.DataFrame({
    "Metric": [
        "Dataset Rows",
        "Dataset Columns",
        "Average Base Price",
        "Minimum Base Price",
        "Maximum Base Price",
        "Average Guests",
        "Average Extra Guests"
    ],
    "Value": [
        len(df),
        len(df.columns),
        round(df["Base_Price"].mean(), 2),
        round(df["Base_Price"].min(), 2),
        round(df["Base_Price"].max(), 2),
        round(df["Guests"].mean(), 2),
        round(df["Extra_Guests"].mean(), 2)
    ]
})

eda_summary.to_csv(
    "eda_summary.csv",
    index=False
)


# ============================================================
# 5. FEATURES AND TARGET
# ============================================================

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


# ============================================================
# 6. TRAIN TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTrain Test Split")
print("Training Rows:", len(X_train))
print("Testing Rows:", len(X_test))


# ============================================================
# 7. FEATURES
# ============================================================

categorical_features = [
    "Room_Type",
    "Day_Type",
    "Season"
]

numeric_features = [
    "Guests",
    "Extra_Guests"
]


# ============================================================
# 8. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            Pipeline([
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
            ]),
            categorical_features
        ),
        (
            "numeric",
            Pipeline([
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
            ]),
            numeric_features
        )
    ]
)


# ============================================================
# 9. MODELS
# ============================================================

models = {
    "Linear Regression": LinearRegression(),

    "Ridge Regression": Ridge(),

    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    ),

    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
}


# ============================================================
# 10. MODEL TRAINING AND COMPARISON
# ============================================================

print("\nModel Comparison")

results = []
trained_models = {}

for name, model in models.items():

    print("Training:", name)

    pipeline = Pipeline([
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ])

    pipeline.fit(
        X_train,
        y_train
    )

    predictions = pipeline.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    trained_models[name] = pipeline

    results.append({
        "Model": name,
        "MAE": round(mae, 4),
        "RMSE": round(rmse, 4),
        "R2": round(r2, 4)
    })


comparison_df = pd.DataFrame(results)

comparison_df = comparison_df.sort_values(
    by="R2",
    ascending=False
)

comparison_df.to_csv(
    "model_comparison.csv",
    index=False
)

print("\nModel Comparison Results")
print(comparison_df)


# ============================================================
# 11. CROSS VALIDATION
# ============================================================

print("\nCross Validation")

cv_results = []

for name, pipeline in trained_models.items():

    print("Cross validating:", name)

    scores = cross_val_score(
        pipeline,
        X_train,
        y_train,
        cv=5,
        scoring="r2"
    )

    cv_results.append({
        "Model": name,
        "Mean_R2": round(
            scores.mean(),
            4
        ),
        "Standard_Deviation": round(
            scores.std(),
            4
        )
    })


cv_df = pd.DataFrame(cv_results)

cv_df = cv_df.sort_values(
    by="Mean_R2",
    ascending=False
)

cv_df.to_csv(
    "cross_validation.csv",
    index=False
)

print("\nCross Validation Results")
print(cv_df)


# ============================================================
# 12. GRIDSEARCHCV
# ============================================================

print("\nGridSearchCV")

rf_pipeline = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "model",
        RandomForestRegressor(
            random_state=42
        )
    )
])

param_grid = {
    "model__n_estimators": [
        50,
        100
    ],
    "model__max_depth": [
        None,
        10,
        15
    ],
    "model__min_samples_split": [
        2,
        5
    ]
}

grid_search = GridSearchCV(
    rf_pipeline,
    param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1
)

grid_search.fit(
    X_train,
    y_train
)

print("\nBest Parameters:")
print(grid_search.best_params_)

print(
    "Best CV R2:",
    round(
        grid_search.best_score_,
        4
    )
)


# ============================================================
# 13. FINAL MODEL EVALUATION
# ============================================================

best_model = grid_search.best_estimator_

final_predictions = best_model.predict(
    X_test
)

final_mae = mean_absolute_error(
    y_test,
    final_predictions
)

final_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        final_predictions
    )
)

final_r2 = r2_score(
    y_test,
    final_predictions
)

print("\nFinal Best Model Results")

print(
    "MAE:",
    round(final_mae, 4)
)

print(
    "RMSE:",
    round(final_rmse, 4)
)

print(
    "R2:",
    round(final_r2, 4)
)


# ============================================================
# 14. SAVE GRIDSEARCH RESULT
# ============================================================

grid_result = pd.DataFrame([
    {
        "Model": "Random Forest GridSearchCV",
        "MAE": round(final_mae, 4),
        "RMSE": round(final_rmse, 4),
        "R2": round(final_r2, 4)
    }
])

grid_result.to_csv(
    "gridsearch_result.csv",
    index=False
)


# ============================================================
# 15. SAVE BEST MODEL
# ============================================================

joblib.dump(
    best_model,
    "best_model.pkl"
)

print("\nBest Model Saved Successfully")
print("File: best_model.pkl")


# ============================================================
# 16. SAVE FINAL SUMMARY
# ============================================================

summary = pd.DataFrame([
    {
        "Best_Model": "Random Forest GridSearchCV",
        "MAE": round(final_mae, 4),
        "RMSE": round(final_rmse, 4),
        "R2": round(final_r2, 4),
        "Training_Rows": len(X_train),
        "Testing_Rows": len(X_test)
    }
])

summary.to_csv(
    "ml_summary.csv",
    index=False
)


# ============================================================
# COMPLETE
# ============================================================

print("\n======================================")
print("PHASE 16 ML PIPELINE COMPLETED")
print("======================================")

print("\nCreated Files:")

print("✓ best_model.pkl")
print("✓ model_comparison.csv")
print("✓ cross_validation.csv")
print("✓ gridsearch_result.csv")
print("✓ ml_summary.csv")
print("✓ eda_summary.csv")