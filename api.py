from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import joblib

# Define input data model
class InputData(BaseModel):
    description: str
    category: str

# Initialize app
app = FastAPI(title="Entity Classifier API")

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
model = BertForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=NUM_LABELS)
model.load_state_dict(torch.load("best_model.pt", map_location=torch.device('cpu')))
model.eval()

# Load Label Encoder
le = joblib.load("label_encoder.joblib")  # You need to save this during training

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Prediction function
def predict_entity(description: str, category: str):
    combined = f"{description} [SEP] {category}"
    encoding = tokenizer(combined, truncation=True, padding='max_length', max_length=128, return_tensors='pt')
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        prediction = torch.argmax(outputs.logits, dim=1).item()
    
    predicted_label = le.inverse_transform([prediction])[0]
    return predicted_label

# Endpoint
@app.post("/predict/")
def predict(data: InputData):
    prediction = predict_entity(data.description, data.category)
    return {"responsible_entity_id": prediction}
