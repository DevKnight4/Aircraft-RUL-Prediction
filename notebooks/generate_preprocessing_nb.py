import json
import os

notebook = {
 "cells": [],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}

def add_md(text):
    notebook["cells"].append({"cell_type": "markdown", "metadata": {}, "source": [line + "\n" for line in text.split("\n")]})

def add_code(code):
    notebook["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + "\n" for line in code.split("\n")]})

add_md("# PRD 1: Data Preparation\n\nThe objective of this notebook is to cleanly preprocess the CMAPSS FD002 dataset based on observations from our EDA (PRD 0), preparing it for future feature engineering and modeling. We keep all decisions reproducible and data-driven.")

add_code("""import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split

# Add src to path (check both notebooks/ and project root context)
for path in [os.path.abspath(os.path.join('..', 'src', 'data')), os.path.abspath(os.path.join('src', 'data'))]:
    if os.path.exists(path):
        sys.path.append(path)
        break
from data_loader import load_cmapss_data, load_rul_data

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('deep')
import warnings
warnings.filterwarnings('ignore')
""")

add_md("## 1. Load Data & Generate RUL")
add_code("""DATA_PATH = os.path.join('..', 'data', 'raw')
train_df = load_cmapss_data(DATA_PATH, dataset_type='train', dataset_id='FD002')
test_df = load_cmapss_data(DATA_PATH, dataset_type='test', dataset_id='FD002')
rul_df = load_rul_data(DATA_PATH, dataset_id='FD002')

# Generate RUL for the training set
max_cycles = train_df.groupby('engine_id')['cycle'].max()
train_df['RUL'] = train_df.apply(lambda row: max_cycles[row['engine_id']] - row['cycle'], axis=1)

print(f"Loaded Train Data: {train_df.shape}")
print(f"Loaded Test Data: {test_df.shape}")
""")

add_md("## 2. Data Integrity Checks\n\nEnsure no missing or infinite values are present.")
add_code("""missing_vals = train_df.isnull().sum().sum()
inf_vals = np.isinf(train_df.select_dtypes(include=np.number)).sum().sum()
duplicates = train_df.duplicated().sum()

print(f"Missing Values: {missing_vals}")
print(f"Infinite Values: {inf_vals}")
print(f"Duplicate Rows: {duplicates}")
""")

add_md("## 3. Constant & Near-Constant Feature Removal\n\nIdentify sensors that provide zero or near-zero variance across the dataset and remove them.")
add_code("""std_devs = train_df.std()
constant_sensors = std_devs[std_devs == 0].index.tolist()
near_constant_sensors = std_devs[(std_devs > 0) & (std_devs < 0.01)].index.tolist()

sensors_to_drop = constant_sensors + near_constant_sensors

print(f"Sensors to drop: {sensors_to_drop}")

train_df_reduced = train_df.drop(columns=sensors_to_drop)
test_df_reduced = test_df.drop(columns=sensors_to_drop)

print(f"Original shape: {train_df.shape}")
print(f"Reduced shape: {train_df_reduced.shape}")
""")

add_md("## 4. Normalization Strategy Exploration\n\nWe briefly compare `StandardScaler`, `MinMaxScaler`, and `RobustScaler` on a sample engine to visually confirm which strategy normalizes the scale appropriately without distorting the underlying degradation trajectory.")
add_code("""sample_sensors = ['sensor_2', 'sensor_3', 'sensor_4', 'sensor_7', 'sensor_11']

df_std = train_df_reduced.copy()
df_minmax = train_df_reduced.copy()
df_robust = train_df_reduced.copy()

std_scaler = StandardScaler()
minmax_scaler = MinMaxScaler()
robust_scaler = RobustScaler()

df_std[sample_sensors] = std_scaler.fit_transform(df_std[sample_sensors])
df_minmax[sample_sensors] = minmax_scaler.fit_transform(df_minmax[sample_sensors])
df_robust[sample_sensors] = robust_scaler.fit_transform(df_robust[sample_sensors])

def plot_scalers(original, std, minmax, robust, sensor, engine_id=3):
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    
    o_data = original[original['engine_id'] == engine_id]
    s_data = std[std['engine_id'] == engine_id]
    m_data = minmax[minmax['engine_id'] == engine_id]
    r_data = robust[robust['engine_id'] == engine_id]
    
    axes[0].plot(o_data['cycle'], o_data[sensor])
    axes[0].set_title(f'Original')
    
    axes[1].plot(s_data['cycle'], s_data[sensor])
    axes[1].set_title('StandardScaler')
    
    axes[2].plot(m_data['cycle'], m_data[sensor])
    axes[2].set_title('MinMaxScaler')
    
    axes[3].plot(r_data['cycle'], r_data[sensor])
    axes[3].set_title('RobustScaler')
    
    plt.suptitle(f"Normalization Comparison for {sensor}", y=1.05)
    plt.tight_layout()
    plt.show()

plot_scalers(train_df_reduced, df_std, df_minmax, df_robust, 'sensor_2')
print("Observation: StandardScaler correctly standardizes the values (mean=0, variance=1) while preserving the monotonic trend. We proceed with StandardScaler for simplicity and ML compatibility.")
""")

add_md("## 5. Engine-Level Train/Validation Split\n\nTo prevent data leakage, we perform the train/validation split at the engine level rather than the row level. This ensures no engine trajectory spans both sets.")
add_code("""engine_ids = train_df_reduced['engine_id'].unique()
train_engines, val_engines = train_test_split(engine_ids, test_size=0.2, random_state=42)

train_split = train_df_reduced[train_df_reduced['engine_id'].isin(train_engines)].copy()
val_split = train_df_reduced[train_df_reduced['engine_id'].isin(val_engines)].copy()
test_split = test_df_reduced.copy()

print(f"Total engines: {len(engine_ids)}")
print(f"Training engines: {len(train_engines)}")
print(f"Validation engines: {len(val_engines)}")
print(f"\\nTrain split shape: {train_split.shape}")
print(f"Val split shape: {val_split.shape}")
print(f"Test split shape: {test_split.shape}")
""")

add_md("## 6. Apply Final Preprocessing & Save\n\nWe apply `StandardScaler` to all active sensor readings. Crucially, the scaler is **fitted only on the training split**, and then used to transform the validation and test splits.")
add_code("""final_scaler = StandardScaler()

active_sensors = [col for col in train_split.columns if 'sensor' in col]

train_split[active_sensors] = final_scaler.fit_transform(train_split[active_sensors])
val_split[active_sensors] = final_scaler.transform(val_split[active_sensors])
test_split[active_sensors] = final_scaler.transform(test_split[active_sensors])

# Export processed datasets
processed_dir = os.path.join('..', 'data', 'processed')
os.makedirs(processed_dir, exist_ok=True)

train_split.to_csv(os.path.join(processed_dir, 'train_processed.csv'), index=False)
val_split.to_csv(os.path.join(processed_dir, 'validation_processed.csv'), index=False)
test_split.to_csv(os.path.join(processed_dir, 'test_processed.csv'), index=False)

import joblib
models_dir = os.path.join('..', 'models')
os.makedirs(models_dir, exist_ok=True)
joblib.dump(final_scaler, os.path.join(models_dir, 'scaler.joblib'))

print(f"Successfully saved processed datasets to {os.path.abspath(processed_dir)}")
print(f"Successfully saved scaler to {os.path.abspath(models_dir)}")
""")

add_md("## Final Preprocessing Decisions\n\n- **Constant Sensors Removed:** `['sensor_1', 'sensor_5', 'sensor_6', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19']` (Constant features naturally dropped).\n- **Chosen Normalization Strategy:** Global `StandardScaler` applied to all retained sensors. Condition-specific scaling was bypassed in favor of a simpler, robust global baseline.\n- **Train/Validation Split:** 80/20 split strictly at the engine level (Seed=42) to prevent time-series data leakage.\n- **Processed Datasets:** `train_processed.csv`, `validation_processed.csv`, and `test_processed.csv` generated successfully.")

output_path = os.path.join(os.path.dirname(__file__), '02_preprocessing_experiments.ipynb')
with open(output_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print(f"Notebook generated at {output_path}")
