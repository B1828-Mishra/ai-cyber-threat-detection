import os
import joblib
import pandas as pd


# Project path
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_PATH,
    "models",
    "random_forest_model.pkl"
)

FEATURE_PATH = os.path.join(
    BASE_PATH,
    "models",
    "feature_names.pkl"
)


# Load model
model = joblib.load(MODEL_PATH)

# Load feature names
feature_names = joblib.load(FEATURE_PATH)

print("Model loaded successfully!")
print("Number of features:", len(feature_names))


# Create sample network flow
sample = pd.DataFrame(
    [[0] * len(feature_names)],
    columns=feature_names
)


# Make prediction
prediction = model.predict(sample)[0]

probability = model.predict_proba(sample)[0][1]


if prediction == 0:
    result = "BENIGN"
else:
    result = "ATTACK"


print("\nPrediction:", result)
print(f"Attack probability: {probability:.2%}")