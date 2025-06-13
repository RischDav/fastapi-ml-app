from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

from app.api.endpoints import router

# Kürzel zu Ministerium (ohne Bundesland)
MINISTRY_SHORTCUTS = {
    "MW": "Ministerium für Wirtschaft",
    "VM": "Ministerium für Verkehr",
    "SM": "Ministerium für Soziales",
    "BM": "Ministerium für Bildung",
    "UM": "Ministerium für Umwelt",
    "FM": "Ministerium der Finanzen",
    "IM": "Ministerium des Innern",
    "GM": "Ministerium für Gesundheit",
    # ... ergänze nach Bedarf ...
}

def get_ministry_from_id(entity_id):
    # Ausnahmefall für Bund
    if entity_id == "BUND" or (isinstance(entity_id, str) and entity_id.startswith("BUND")):
        return "Bundesministerium für Digitales und Verkehr"
    if isinstance(entity_id, str) and "_" in entity_id:
        shortcut = entity_id.split("_")[-1]
        return MINISTRY_SHORTCUTS.get(shortcut, "Unbekanntes Ministerium")
    return "Unbekanntes Ministerium"

app = FastAPI()
app.include_router(router)

class PredictionRequest(BaseModel):
    model: str
    description: str = None
    district: str = None
    state: str = None
    category: str = None

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
            pred_id = prediction[0]
            ministry = get_ministry_from_id(pred_id)
            if pred_id == "BUND" or (isinstance(pred_id, str) and pred_id.startswith("BUND")):
                readable = f"Das {ministry} ist für deine Anfrage zuständig."
                state = "kein bundesland"
            else:
                bundesland = request.state if request.state else ""
                readable = f"Das {ministry} in {bundesland} ist für deine Anfrage zuständig."
                state = bundesland
            return {
                "model": "model1",
                "prediction": pred_id,
                "responsible_entity_readable": readable,
                "state": state
            }
        elif request.model == "model2":
            if not all([request.district, request.state, request.category]):
                raise HTTPException(status_code=400, detail="district, state, and category are required for model2")
            model_dict = joblib.load("app/model/model2/xgb_all_models.pkl")
            features = np.array([[request.district, request.state, request.category]])
            pred_level = model_dict["Level"].predict(features)[0]
            pred_state_code = model_dict["State Code"].predict(features)[0]
            pred_department = model_dict["Department"].predict(features)[0]
            result = f"{pred_level}_{pred_state_code}_{pred_department}"
            ministry = get_ministry_from_id(result)
            if result == "BUND" or (isinstance(result, str) and result.startswith("BUND")):
                readable = f"Das {ministry} ist für deine Anfrage zuständig."
                state = "kein bundesland"
            else:
                bundesland = request.state if request.state else ""
                readable = f"Das {ministry} in {bundesland} ist für deine Anfrage zuständig."
                state = bundesland
            return {
                "model": "model2",
                "prediction": result,
                "responsible_entity_readable": readable,
                "state": state
            }
        else:
            raise HTTPException(status_code=400, detail="Unknown model type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))