import os
import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


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


# Load trained model
model = joblib.load(MODEL_PATH)

# Load feature names
feature_names = joblib.load(FEATURE_PATH)


app = FastAPI(
    title="AI Cyber Threat Detection API",
    description="API for detecting network security threats using Machine Learning",
    version="1.0.0"
)


class PredictionRequest(BaseModel):
    features: list[float]


@app.get("/")
def home():
    return {
        "message": "AI Cyber Threat Detection API is running"
    }


@app.post("/predict")
def predict(request: PredictionRequest):

    if len(request.features) != len(feature_names):
        return {
            "error": f"Expected {len(feature_names)} features, "
                      f"but received {len(request.features)}"
        }

    input_data = pd.DataFrame(
    [request.features],
    columns=feature_names
)

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    if prediction == 0:
        result = "BENIGN"
    else:
        result = "ATTACK"

    return {
        "prediction": result,
        "attack_probability": round(float(probability), 4)
    }