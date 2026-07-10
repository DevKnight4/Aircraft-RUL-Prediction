import json
import os

notebook = {
 "cells": [],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}

def add_md(text):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    })

def add_code(code):
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.split("\n")]
    })

# 1. Introduction
add_md("# PRD 0: CMAPSS FD002 Exploratory Data Analysis (Refined)\n\nThis notebook performs Exploratory Data Analysis on the CMAPSS FD002 dataset using a strict ML engineering mindset. We aim to understand the sensor data, operating conditions, and engine degradation behavior through observation rather than assumption.")

# 2. Setup and Imports
add_code("""import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import random

# Adjust path to import data loader (check both notebooks/ and project root context)
for path in [os.path.abspath(os.path.join('..', 'src', 'data')), os.path.abspath(os.path.join('src', 'data'))]:
    if os.path.exists(path):
        sys.path.append(path)
        break
from data_loader import load_cmapss_data, load_rul_data

# Styling
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('deep')
plt.rcParams['figure.figsize'] = (10, 6)

import warnings
warnings.filterwarnings('ignore')
""")

# 4. Data Loading and Target Generation
add_md("## Dataset Loading & Target Generation")
add_code("""DATA_PATH = os.path.join('..', 'data', 'raw')

train_df = load_cmapss_data(DATA_PATH, dataset_type='train', dataset_id='FD002')
test_df = load_cmapss_data(DATA_PATH, dataset_type='test', dataset_id='FD002')
rul_df = load_rul_data(DATA_PATH, dataset_id='FD002')

print(f"Train Shape: {train_df.shape}")
print(f"Test Shape: {test_df.shape}")

# Generate RUL for training data
max_cycles = train_df.groupby('engine_id')['cycle'].max()
train_df['RUL'] = train_df.apply(lambda row: max_cycles[row['engine_id']] - row['cycle'], axis=1)
""")

# 5. Dataset Profiling & Data Quality
add_md("## Dataset Profiling & Data Quality")
add_code("""print("--- Dataset Summary ---")
print(f"Number of engines (Train): {train_df['engine_id'].nunique()}")
print(f"Total observations (Train): {len(train_df)}")

# Missing Values
missing_vals = train_df.isnull().sum().sum()
print(f"Total missing values: {missing_vals}")

# Constant Features
std_devs = train_df.std()
constant_features = std_devs[std_devs == 0].index.tolist()
print(f"Constant features (Std == 0): {constant_features}")

low_variance_features = std_devs[std_devs < 0.01].index.tolist()
print(f"Near-constant features (Std < 0.01): {low_variance_features}")
""")

# 6. Operational Condition Analysis
add_md("## 1. Operational Condition Analysis (Visual Exploration)\n\nWe analyze the three operational settings directly to determine whether distinct operating conditions naturally emerge, without imposing prior assumptions.\n\nWe use PCA **only** as an exploratory visualization to answer:\n- Do operating conditions naturally separate?\n- Is there any visible clustering?\n- Does the dataset exhibit obvious structure?")
add_code("""op_cols = ['op_setting_1', 'op_setting_2', 'op_setting_3']

# Pairwise scatter plots
sns.pairplot(train_df[op_cols].sample(10000, random_state=42), diag_kind='kde', corner=True, plot_kws={'alpha': 0.1})
plt.suptitle('Pairwise Plot of Operational Settings (Sampled)', y=1.02, fontsize=16)
plt.show()

# PCA for visualization (2D)
pca = PCA(n_components=2)
op_pca = pca.fit_transform(train_df[op_cols])

plt.figure(figsize=(10, 6))
plt.scatter(op_pca[:, 0], op_pca[:, 1], alpha=0.05, s=5)
plt.title('PCA of Operational Settings (2 Components)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

print("Variance explained by 2 components:", pca.explained_variance_ratio_.sum())
""")

# 7. Sensor Analysis
add_md("## 2. Preliminary Sensor Analysis (Linear Correlation)\n\nWe examine the Pearson correlation matrix. **Note:** Correlation only measures linear relationships. Sensors with low linear correlation might still contain critical degradation signals through non-linear interactions.")
add_code("""sensors = [f'sensor_{i}' for i in range(1, 22)]
active_sensors = [s for s in sensors if s not in constant_features]

corr = train_df[active_sensors + ['RUL']].corr()
plt.figure(figsize=(15, 12))
sns.heatmap(corr, annot=False, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap of Active Sensors and RUL')
plt.show()

rul_corr = corr['RUL'].abs().sort_values(ascending=False)
print("Correlation with RUL:")
display(rul_corr.head(10))
""")

# Sensor Summary Table
add_md("### Sensor Summary Table\n\nThis table compiles observational statistics for every sensor. Qualitative columns are left blank to be filled based on visual review, maintaining descriptive observations without forcing engineering decisions.")
add_code("""summary_df = pd.DataFrame({
    'Sensor': active_sensors,
    'Variance': train_df[active_sensors].var().values,
    'Pearson_Corr_RUL': [corr.loc[s, 'RUL'] for s in active_sensors],
    'Appears_Stable (Y/N)': [''] * len(active_sensors),
    'Apparent_Degradation_Trend (Y/N)': [''] * len(active_sensors),
    'Noise_Level (Low/Med/High)': [''] * len(active_sensors),
    'Observations': [''] * len(active_sensors)
})
display(summary_df)
""")


# 8. Sensor Stability Analysis
add_md("## 3. Sensor Stability & Trajectory Analysis\n\nWe overlay trajectories from randomly selected engines (using a fixed random seed) to understand how each sensor behaves across the engine's lifetime. This helps identify smooth degradation, stability, heavy fluctuation, or noise.")
add_code("""def plot_multi_engine_trajectories(df, sensors, n_engines=10, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    engine_ids = random.sample(list(df['engine_id'].unique()), n_engines)
    
    n_sensors = len(sensors)
    cols = 3
    rows = int(np.ceil(n_sensors / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(16, 4 * rows))
    axes = axes.flatten()
    
    for i, sensor in enumerate(sensors):
        for eid in engine_ids:
            engine_data = df[df['engine_id'] == eid]
            axes[i].plot(engine_data['cycle'], engine_data[sensor], alpha=0.5, linewidth=1)
        axes[i].set_title(f'{sensor}')
        axes[i].set_xlabel('Cycle')
        
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')
        
    plt.tight_layout()
    plt.show()

print("Plotting trajectories for active sensors across 10 random engines...")
plot_multi_engine_trajectories(train_df, active_sensors, n_engines=10, seed=42)
""")

# 9. Fleet-Level Degradation Visualization
add_md("## 4. Fleet-Level Degradation Visualization\n\nTo determine if degradation trends are consistent across engines or highly variable, we plot the fleet-level mean sensor value across cycles, along with ±1 standard deviation bands.\n\n*Note: Because engine lifespans vary, we plot this against RUL (Remaining Useful Life) to synchronize the failure points at x=0.*")
add_code("""def plot_fleet_degradation(df, sensors):
    cols = 3
    rows = int(np.ceil(len(sensors) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(16, 4 * rows))
    axes = axes.flatten()
    
    # Grouping by RUL synchronizes the engines at failure (RUL=0)
    fleet_stats = df.groupby('RUL')[sensors].agg(['mean', 'std'])
    
    for i, sensor in enumerate(sensors):
        mean_val = fleet_stats[sensor]['mean']
        std_val = fleet_stats[sensor]['std']
        rul_idx = fleet_stats.index
        
        axes[i].plot(rul_idx, mean_val, color='blue', label='Mean')
        axes[i].fill_between(rul_idx, mean_val - std_val, mean_val + std_val, color='blue', alpha=0.2, label='±1 Std Dev')
        
        # Invert x-axis so time moves forward (RUL decreases to 0)
        axes[i].invert_xaxis()
        
        axes[i].set_title(f'{sensor} Fleet-Level Trend')
        axes[i].set_xlabel('Remaining Useful Life (RUL)')
        axes[i].set_ylabel('Sensor Value')
        if i == 0:
            axes[i].legend()
            
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')
        
    plt.tight_layout()
    plt.show()

# Visualize for a subset of representative sensors
sample_sensors = ['sensor_2', 'sensor_3', 'sensor_4', 'sensor_7', 'sensor_11', 'sensor_15']
plot_fleet_degradation(train_df, sample_sensors)
""")

# 10. Variance Analysis over Engine Life
add_md("## 5. Variance Analysis over Engine Life\n\nWe compute the rolling standard deviation for a random engine to see if variability increases as the engine approaches failure. This explores temporal patterns that could inspire future engineered features.")
add_code("""def plot_rolling_variance(df, sensors, engine_id=42, window=15):
    engine_data = df[df['engine_id'] == engine_id].copy()
    engine_data = engine_data.sort_values('cycle')
    
    cols = 3
    rows = int(np.ceil(len(sensors) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(16, 4 * rows))
    axes = axes.flatten()
    
    for i, sensor in enumerate(sensors):
        rolling_std = engine_data[sensor].rolling(window=window).std()
        
        ax1 = axes[i]
        ax2 = ax1.twinx()
        
        ax1.plot(engine_data['cycle'], engine_data[sensor], alpha=0.5, color='blue', label='Raw')
        ax2.plot(engine_data['cycle'], rolling_std, color='red', linewidth=2, label=f'Rolling Std (w={window})')
        
        ax1.set_title(f'{sensor}')
        ax1.set_xlabel('Cycle')
        ax1.set_ylabel('Raw Value', color='blue')
        ax2.set_ylabel('Rolling Std', color='red')
        
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')
        
    plt.tight_layout()
    plt.show()

print("Plotting Raw vs Rolling Standard Deviation for Engine 42:")
plot_rolling_variance(train_df, sample_sensors, engine_id=42, window=15)
""")

# 11. End PRD 0
add_md("""## Hypotheses for PRD 1

Based on the evidence gathered above, we form the following hypotheses to be tested during preprocessing:

* **H1:** Certain sensors appear nearly constant and may later be removable.
* **H2:** Operational settings significantly influence several sensor measurements (evident from the PCA structure and dataset origin).
* **H3:** Temporal degradation appears smoother than instantaneous readings, suggesting rolling or smoothing functions could be beneficial.
* **H4:** Rolling statistics (like rolling variance) may capture degradation signals better than raw sensor values for sensors that exhibit increasing variance near end-of-life.
* **H5:** Fleet-level trends indicate that despite inter-engine variability, the degradation paths are consistent when aligned by Remaining Useful Life.

---

## Key Findings

- **Operational Structure:** The dataset exhibits distinct structural clusters within the operating conditions. 
- **Sensor Degradation:** Several active sensors display clear monotonic degradation trends correlated with RUL.
- **Sensor Noise:** Certain sensors appear heavily dominated by noise or operational conditions rather than pure degradation.
- **Consistency:** Inter-engine variability is present, but fleet-level mean trends (±1 std) remain identifiable when synchronized at the failure point (RUL=0).

---

## Next Questions

These engineering questions should be answered in PRD 1:
- Which normalization strategy is most appropriate (Global vs. Operating-Condition Specific)?
- Which sensors should be retained, and which should be dropped due to being constant or noisy?
- Should preprocessing be operating-condition specific?
- Does denoising or smoothing improve the signal quality?
- Which temporal features (e.g., rolling means, standard deviations) are worth engineering for predictive modeling?
""")

# Save the notebook
output_path = os.path.join(os.path.dirname(__file__), '01_eda_fd002.ipynb')
with open(output_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print(f"Notebook generated at {output_path}")
