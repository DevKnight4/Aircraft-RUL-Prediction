from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, create_model
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="AeroPulse RUL Prediction API", description="API for predicting Remaining Useful Life of aircraft engines.")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and scaler
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

MODEL_PATH = os.path.join(MODELS_DIR, 'final_model.joblib')
SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.joblib')

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("Model and Scaler loaded successfully.")
except Exception as e:
    print(f"Warning: Could not load model or scaler. Ensure they exist in {MODELS_DIR}. Error: {e}")
    model = None
    scaler = None

# We need to expect the exact features the model was trained on
# The model expects: cycle, op_setting_1, op_setting_2, op_setting_3, plus the active sensors
ACTIVE_SENSORS = [
    'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'sensor_6',
    'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10', 'sensor_11', 'sensor_12',
    'sensor_13', 'sensor_14', 'sensor_15', 'sensor_17', 'sensor_18', 'sensor_19',
    'sensor_20', 'sensor_21'
]

class PredictRequest(BaseModel):
    cycle: float
    op_setting_1: float
    op_setting_2: float
    op_setting_3: float
    sensor_1: float
    sensor_2: float
    sensor_3: float
    sensor_4: float
    sensor_5: float
    sensor_6: float
    sensor_7: float
    sensor_8: float
    sensor_9: float
    sensor_10: float
    sensor_11: float
    sensor_12: float
    sensor_13: float
    sensor_14: float
    sensor_15: float
    sensor_17: float
    sensor_18: float
    sensor_19: float
    sensor_20: float
    sensor_21: float

@app.get("/health")
def health_check():
    if model is None or scaler is None:
        return {"status": "unhealthy", "message": "Model or scaler not loaded"}
    return {"status": "healthy"}

@app.post("/predict")
def predict_rul(request: PredictRequest):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model or scaler not loaded.")

    try:
        # Convert request to DataFrame
        data = request.model_dump()
        df = pd.DataFrame([data])

        # Apply scaler ONLY to the active sensors
        df[ACTIVE_SENSORS] = scaler.transform(df[ACTIVE_SENSORS])

        # Ensure column order matches exactly what the model expects
        expected_cols = ['cycle', 'op_setting_1', 'op_setting_2', 'op_setting_3'] + ACTIVE_SENSORS
        df = df[expected_cols]

        # Predict
        rul_pred = model.predict(df)[0]
        
        # Ensure RUL is not negative
        rul_pred = max(0, float(rul_pred))

        # Determine status
        if rul_pred > 50:
            status = "Healthy"
        elif rul_pred >= 20:
            status = "Warning"
        else:
            status = "Critical"

        return {
            "predicted_rul": round(rul_pred, 2),
            "status": status
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/sample-engines")
def get_sample_engines():
    try:
        import sys
        sys.path.append(os.path.join(BASE_DIR, 'src', 'data'))
        from data_loader import load_cmapss_data
        
        test_df = load_cmapss_data(os.path.join(BASE_DIR, 'data', 'raw'), 'test', 'FD002')
        
        # Pick specific engines from the test set and get their last recorded cycle
        samples = []
        for eng_id in [3, 14, 25, 42, 60, 88]:
            eng_data = test_df[test_df['engine_id'] == eng_id].iloc[-1]
            # Replace NaNs with 0 to prevent JSON serialization errors just in case
            eng_dict = eng_data.fillna(0).to_dict()
            samples.append({
                "name": f"Test Engine {eng_id} (Cycle {eng_dict['cycle']})",
                "data": eng_dict
            })
        return samples
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
