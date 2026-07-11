# ✈️ Aircraft Engine Remaining Useful Life Prediction

An end-to-end machine learning system for predictive maintenance using **NASA's CMAPSS FD002 turbofan engine dataset**. This project estimates the **Remaining Useful Life (RUL)** of aircraft engines using machine learning, exposing predictions through a FastAPI backend and an interactive React dashboard.

🌐 **Live Demo:** https://aircraft-rul-prediction.vercel.app/



![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-19-61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688)
![LightGBM](https://img.shields.io/badge/LightGBM-ML-success)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)

---

## 📖 Project Overview

Aircraft engines gradually degrade over time due to operational stress and component wear. Unexpected failures can lead to expensive repairs, operational delays, and potential safety risks.

Predictive maintenance aims to estimate **how many operational cycles remain before an engine requires maintenance**, allowing organizations to replace reactive maintenance schedules with data-driven decision making.

This project implements an end-to-end machine learning pipeline that predicts an aircraft engine's **Remaining Useful Life (RUL)** from multivariate sensor telemetry using NASA's CMAPSS benchmark dataset.

---

## ✨ Key Features

- Predicts Remaining Useful Life (RUL) of aircraft turbofan engines
- Interactive React dashboard for real-time inference
- FastAPI backend serving trained ML model
- Engine health classification (Healthy / Warning / Critical)
- Feature importance visualization
- Demo mode using real CMAPSS engine telemetry
- Dockerized backend for reproducible deployment

---

# 🏗️ System Architecture

```text
                NASA CMAPSS Dataset
                         │
                         ▼
                Data Preprocessing
                         │
                         ▼
              LightGBM Regressor Model
                         │
                         ▼
                 FastAPI Prediction API
                         │
                         ▼
               React Interactive Dashboard
                         │
                         ▼
                 Dockerized Deployment
```

---

# 🤖 Machine Learning Pipeline

## Dataset

- **Dataset:** NASA CMAPSS FD002
- Multivariate time-series degradation dataset
- Multiple operating conditions
- Multiple engine units
- Sensor noise included to simulate real-world telemetry

---

## Exploratory Data Analysis

The initial analysis focused on understanding sensor behaviour and degradation characteristics across multiple engines.

Major observations included:

- Engines exhibit unique degradation trajectories.
- Operational settings significantly influence sensor behaviour.
- Several sensors show clear degradation trends approaching failure.
- Certain sensors remain nearly constant and contribute little predictive value.

These observations guided subsequent preprocessing and feature selection.

---

## Data Preprocessing

The preprocessing pipeline was designed to maximize model robustness while preventing data leakage.

Steps performed:

- Removed non-informative features
- Standardized numerical features
- Engine-level train-validation split
- Prepared data for supervised regression

---

## Feature Engineering Experiments

Several temporal and statistical features were explored, including:

- Rolling Mean
- Rolling Standard Deviation
- Exponential Moving Average (EMA)
- Rate of Change
- Sensor Interaction Features
- Log(Cycle)

These features were experimentally evaluated but produced only marginal improvements over the baseline feature set.

The final model intentionally uses the simpler feature representation to maintain interpretability while achieving comparable predictive performance.

---

## Model Comparison

Multiple regression models were evaluated:

| Model | Purpose |
|-------|---------|
| Random Forest Regressor | Baseline ensemble model |
| XGBoost Regressor | Gradient boosting comparison |
| LightGBM Regressor | High-performance gradient boosting |
| CatBoost Regressor | Additional boosting benchmark |

Each model was evaluated using:

- RMSE
- MAE
- R² Score

Following comparative evaluation and hyperparameter tuning, **LightGBM Regressor** delivered the best overall validation performance and was selected as the final production model.

---


# 📊 Results

| Metric | Value |
|---------|--------|
| RMSE | *34.86* |
| MAE | *26.15* |
| R² Score | *0.7193* |

The trained model successfully predicts engine Remaining Useful Life while providing an intuitive interface for interactive inference and health monitoring.

---

# 🛠️ Technologies Used

| Category | Technologies |
|----------|--------------|
| **Machine Learning** | Python • Pandas • NumPy • Scikit-learn • LightGBM |
| **Backend** | FastAPI |
| **Frontend** | React • Tailwind CSS |
| **Visualization** | Matplotlib • Seaborn |
| **Deployment** | Docker • Vercel |
---

# 🚀 Setup Instructions

## 1. Local Development

### Backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI backend
python backend/main.py
```

The backend will be available at:

```
http://localhost:8000
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

The frontend will be available at:

```
http://localhost:5173
```

---

## 2. Docker Deployment

Build the Docker image:

```bash
docker build -t engine-life-analysis .
```

Run the container:

```bash
docker run -p 8000:8000 engine-life-analysis
```

The API will be available at:

```
http://localhost:8000
```

Interactive API documentation:

```
http://localhost:8000/docs
```

The React frontend can still be executed locally using `npm run dev` and will communicate with the Dockerized backend.

---

# 🙏 Acknowledgements

- NASA Prognostics Center of Excellence for the CMAPSS Turbofan Engine Degradation Simulation Dataset.
- The open-source Python, FastAPI, React, and LightGBM communities whose tools made this project possible.
