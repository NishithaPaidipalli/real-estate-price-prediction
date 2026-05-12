from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd
from pydantic import BaseModel, Field

app = FastAPI(title="Real Estate Production API")

# Updated Schema to match your CSV exactly
class HouseData(BaseModel):
    Area: float = Field(..., gt=0)
    Bedrooms: int = Field(..., ge=1)
    Bathrooms: int = Field(..., ge=1)
    Age: int = Field(..., ge=0)
    Location: str
    Property_Type: str

# Load the model
try:
    with open('models/house_model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None

@app.post("/predict")
async def predict_price(data: HouseData):
    if model is None:
        raise HTTPException(status_code=503, detail="Model file missing. Run training script first.")
    
    # Create DataFrame with exact column names used during training
    input_df = pd.DataFrame([data.model_dump()])
    
    prediction = model.predict(input_df)[0]
    
    return {
        "Price_Estimate": round(float(prediction), 2),
        "Status": "Success"
    }
import logging

# Set up logging to a file
logging.basicConfig(
    filename='app_performance.log',
    level=logging.INFO,
    format='%(asctime)s % (levelname)s : %(message)s'
)

@app.post("/predict")
async def predict_price(data: HouseData):
    # ... your existing code ...
    prediction = model.predict(input_df)[0]
    
    # Log the prediction for monitoring
    logging.info(f"Prediction made for {data.Location}: ${prediction}")
    
    return {"Price_Estimate": round(float(prediction), 2)}
