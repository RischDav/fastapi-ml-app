from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from collections import Counter

app = FastAPI()

# Mapping from responsible_entity_id to state (Bundesland)
ENTITY_ID_TO_STATE = {
    "BUND_BUNDESMINISTERIUM_FÜR_DIGITALES_UND_VERKEHR": "Bund",
    "LAND_01_BM": "Schleswig-Holstein",
    "LAND_02_BM": "Hamburg",
    "LAND_03_BM": "Niedersachsen",
    "LAND_04_BM": "Bremen",
    "LAND_05_BM": "Nordrhein-Westfalen",
    "LAND_06_BM": "Hessen",
    "LAND_07_BM": "Rheinland-Pfalz",
    "LAND_08_BM": "Baden-Württemberg",
    "LAND_09_BM": "Bayern",
    "LAND_10_BM": "Saarland",
    "LAND_11_BM": "Berlin",
    "LAND_12_BM": "Brandenburg",
    "LAND_13_BM": "Mecklenburg-Vorpommern",
    "LAND_14_BM": "Sachsen",
    "LAND_15_BM": "Sachsen-Anhalt",
    "LAND_16_BM": "Thüringen",
}

class PredictionRequest(BaseModel):
    model: str
    description: str = None
    district: str = None
    state: str = None
    category: str = None

@app.get("/requests-number-state")
def requests_number_state():
    df = pd.read_csv("csv/data.csv")
    df["state"] = df["responsible_entity_id"].map(lambda x: ENTITY_ID_TO_STATE.get(x, "Unknown") if isinstance(x, str) else "Unknown")
    counts = dict(Counter(df["state"]))
    return {"requests": counts}

@app.get("/requests-per-state")
def requests_per_state():
    df = pd.read_csv("csv/data.csv")
    counts = dict(Counter(df["state"]))
    return {"requests": counts}

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        if request.model == "model1":
            if not request.description:
                raise HTTPException(status_code=400, detail="description is required for model1")
            model = joblib.load("app/model/model1/model.pkl")
            vectorizer = joblib.load("app/model/model1/vectorizer.pkl")
            description_vector = vectorizer.transform([request.description])
            prediction = model.predict(description_vector)
            return {"model": "model1", "prediction": prediction[0]}
        elif request.model == "model2":
            if not all([request.district, request.state, request.category]):
                raise HTTPException(status_code=400, detail="district, state, and category are required for model2")
            model_dict = joblib.load("app/model/model2/xgb_all_models.pkl")
            features = np.array([[request.district, request.state, request.category]])
            pred_level = model_dict["Level"].predict(features)[0]
            pred_state_code = model_dict["State Code"].predict(features)[0]
            pred_department = model_dict["Department"].predict(features)[0]
            result = f"{pred_level}_{pred_state_code}_{pred_department}"
            return {"model": "model2", "prediction": result}
        else:
            raise HTTPException(status_code=400, detail="Unknown model type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))