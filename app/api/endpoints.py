from fastapi import APIRouter, HTTPException
import pandas as pd
from collections import Counter

router = APIRouter()

ENTITY_ID_TO_STATE = {
    "BUND": "Bund",
    "01": "Schleswig-Holstein",
    "02": "Hamburg",
    "03": "Niedersachsen",
    "04": "Bremen",
    "05": "Nordrhein-Westfalen",
    "06": "Hessen",
    "07": "Rheinland-Pfalz",
    "08": "Baden-Württemberg",
    "09": "Bayern",
    "10": "Saarland",
    "11": "Berlin",
    "12": "Brandenburg",
    "13": "Mecklenburg-Vorpommern",
    "14": "Sachsen",
    "15": "Sachsen-Anhalt",
    "16": "Thüringen",
}

@router.get("/requests-number-state")
def requests_number_state():
    df = pd.read_csv("csv/data.csv")
    result = {name: 0 for name in ENTITY_ID_TO_STATE.values()}
    for idx, row in df.iterrows():
        rid = row.get("responsible_entity_id", "")
        bundesland = "Unknown"
        if isinstance(rid, str):
            if rid.startswith("LAND_"):
                parts = rid.split("_")
                if len(parts) > 1:
                    code = parts[1]
                    bundesland = ENTITY_ID_TO_STATE.get(code, "Unknown")
            elif rid.startswith("BUND_"):
                bundesland = ENTITY_ID_TO_STATE.get("BUND", "Unknown")
        if bundesland != "Unknown":
            result[bundesland] = result.get(bundesland, 0) + 1
    return {"requests": result}

@router.get("/requests-per-state")
def requests_per_state():
    df = pd.read_csv("csv/data.csv")
    # Zählt nur, was in der Spalte "state" steht und ignoriert "Unknown"
    counts = dict(Counter(df["state"]))
    if "Unknown" in counts:
        del counts["Unknown"]
    return {"requests": counts}

@router.get("/requests-per-category")
def requests_per_category():

    df = pd.read_csv("csv/data.csv")
    # Zählt, wie oft jede Kategorie vorkommt
    counts = dict(Counter(df["category"]))
    return {"categories": counts}