from fastapi import APIRouter, HTTPException
import pandas as pd
from collections import Counter

from fastapi import APIRouter
import pandas as pd
from collections import Counter

router = APIRouter()

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
    # ...add all other mappings as needed...
}

@router.get("/requests-number-state")
def requests_per_state():
    df = pd.read_csv("csv/data.csv")
    # Map responsible_entity_id to state
    df["state"] = df["responsible_entity_id"].map(lambda x: ENTITY_ID_TO_STATE.get(x, "Unknown") if isinstance(x, str) else "Unknown")
    counts = dict(Counter(df["state"]))
    return {"requests": counts}



@router.get("/requests-per-state")
async def requests_per_state():
    try:
        df = pd.read_csv("csv/data.csv")
        # Count requests per state
        counts = dict(Counter(df["state"]))
        return {"requests": counts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))