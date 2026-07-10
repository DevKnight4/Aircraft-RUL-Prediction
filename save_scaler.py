import os
import sys
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

sys.path.append(os.path.abspath(os.path.join('src', 'data')))
from data_loader import load_cmapss_data

DATA_PATH = os.path.join('data', 'raw')
train_df = load_cmapss_data(DATA_PATH, dataset_type='train', dataset_id='FD002')

ACTIVE_SENSORS = [
    'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'sensor_6',
    'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10', 'sensor_11', 'sensor_12',
    'sensor_13', 'sensor_14', 'sensor_15', 'sensor_17', 'sensor_18', 'sensor_19',
    'sensor_20', 'sensor_21'
]

engine_ids = train_df['engine_id'].unique()
train_engines, _ = train_test_split(engine_ids, test_size=0.2, random_state=42)
train_split = train_df[train_df['engine_id'].isin(train_engines)].copy()

scaler = StandardScaler()
scaler.fit(train_split[ACTIVE_SENSORS])

os.makedirs('models', exist_ok=True)
joblib.dump(scaler, os.path.join('models', 'scaler.joblib'))
print("Scaler successfully created and saved to models/scaler.joblib")
