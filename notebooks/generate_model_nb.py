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

add_md("# PRD 3: Model Development & Evaluation\n\nThis notebook compares strong tree-based regression models to predict Remaining Useful Life (RUL) using the processed FD002 dataset. We evaluate Random Forest, XGBoost, LightGBM, and CatBoost, tune the best performing model, and export it for deployment.")

add_code("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
import joblib

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('deep')
import warnings
warnings.filterwarnings('ignore')
""")

add_md("## 1. Load Processed Datasets")
add_code("""DATA_PATH = os.path.join('..', 'data', 'processed')
train_df = pd.read_csv(os.path.join(DATA_PATH, 'train_processed.csv'))
val_df = pd.read_csv(os.path.join(DATA_PATH, 'validation_processed.csv'))

# Prepare X and y
drop_cols = ['engine_id', 'RUL']
features = [col for col in train_df.columns if col not in drop_cols]

X_train, y_train = train_df[features], train_df['RUL']
X_val, y_val = val_df[features], val_df['RUL']

print(f"X_train shape: {X_train.shape}")
print(f"X_val shape: {X_val.shape}")
""")

add_md("## 2. Model Comparison\n\nWe train four state-of-the-art tree-based regressors with reasonable default parameters to establish baselines.")
add_code("""models = {
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    'XGBoost': XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    'LightGBM': LGBMRegressor(n_estimators=100, random_state=42, n_jobs=-1, verbose=-1),
    'CatBoost': CatBoostRegressor(iterations=100, random_state=42, verbose=False)
}

results = []

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    
    rmse = np.sqrt(mean_squared_error(y_val, preds))
    mae = mean_absolute_error(y_val, preds)
    r2 = r2_score(y_val, preds)
    
    results.append({
        'Model': name,
        'RMSE': rmse,
        'MAE': mae,
        'R2': r2
    })

results_df = pd.DataFrame(results).sort_values('RMSE')
display(results_df)

best_model_name = results_df.iloc[0]['Model']
print(f"\\nBest performing model based on RMSE: {best_model_name}")
""")

add_md("## 3. Light Hyperparameter Tuning\n\nWe perform a modest RandomizedSearchCV on the best performing model to squeeze out additional performance.")
add_code("""# Define tuning grids based on the best model
param_grids = {
    'Random Forest': {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 15, None],
        'min_samples_split': [2, 5, 10]
    },
    'XGBoost': {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.05, 0.1]
    },
    'LightGBM': {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.05, 0.1]
    },
    'CatBoost': {
        'iterations': [100, 200, 300],
        'depth': [4, 6, 8],
        'learning_rate': [0.01, 0.05, 0.1]
    }
}

base_model = models[best_model_name]
param_grid = param_grids[best_model_name]

print(f"Tuning {best_model_name}...")
random_search = RandomizedSearchCV(
    estimator=base_model,
    param_distributions=param_grid,
    n_iter=10,
    scoring='neg_root_mean_squared_error',
    cv=3,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

random_search.fit(X_train, y_train)

best_model = random_search.best_estimator_
print(f"\\nBest Parameters: {random_search.best_params_}")

# Evaluate tuned model
tuned_preds = best_model.predict(X_val)
tuned_rmse = np.sqrt(mean_squared_error(y_val, tuned_preds))
tuned_mae = mean_absolute_error(y_val, tuned_preds)
tuned_r2 = r2_score(y_val, tuned_preds)

print(f"Tuned RMSE: {tuned_rmse:.2f} (vs Default: {results_df.iloc[0]['RMSE']:.2f})")
print(f"Tuned MAE: {tuned_mae:.2f}")
print(f"Tuned R2: {tuned_r2:.4f}")
""")

add_md("## 4. Model Interpretation\n\nWe plot the feature importance of the final tuned model to identify which raw sensors drive the degradation predictions.")
add_code("""if hasattr(best_model, 'feature_importances_'):
    importances = best_model.feature_importances_
else:
    # Fallback if somehow not available
    importances = np.zeros(len(features))

feat_imp = pd.Series(importances, index=features).sort_values(ascending=False)

plt.figure(figsize=(10, 8))
sns.barplot(x=feat_imp.head(15).values, y=feat_imp.head(15).index, palette='viridis')
plt.title(f'Top 15 Feature Importances ({best_model_name})')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.show()

print("This simple feature importance plot confirms which operational settings and raw sensors most heavily influence RUL predictions.")
""")

add_md("## 5. Export Final Model\n\nWe save the tuned model using `joblib` so it can be deployed in the backend API (PRD 4).")
add_code("""MODELS_DIR = os.path.join('..', 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

model_path = os.path.join(MODELS_DIR, 'final_model.joblib')
joblib.dump(best_model, model_path)

print(f"Successfully saved final model to: {os.path.abspath(model_path)}")
""")

output_path = os.path.join(os.path.dirname(__file__), '04_model_development.ipynb')
with open(output_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print(f"Notebook generated at {output_path}")
