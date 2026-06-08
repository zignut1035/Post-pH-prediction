# 🫐 Berry Fermentation pH Predictor

> A machine learning pipeline that predicts post-fermentation pH of berry wines from fermentation conditions, with an interactive web interface for real-time prediction.
>
> Developed as part of a work placement project at atSauce Company, in collaboration with Turku University of Applied Sciences.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=flat-square&logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-Regressor-red?style=flat-square)
![Status](https://img.shields.io/badge/Status-Research%20Prototype-yellow?style=flat-square)

---

## Overview

Controlling post-fermentation pH is critical in berry wine production — it directly affects taste, safety, and shelf life. This project builds a regression model to **predict the pH after fermentation** based on measurable fermentation conditions, using both real laboratory data and synthetic data to overcome the challenge of small dataset sizes.

A web interface allows producers or researchers to **input fermentation parameters and receive an instant pH prediction** from the trained model.

---

## Dataset

Two data sources were merged for training:

| Source | Description |
|---|---|
| `lab_df` | Real laboratory fermentation records |
| `syn_df` | Synthetic data generated to augment the small lab dataset |

### Features

| Feature | Description |
|---|---|
| Fruit Numeric | Berry type (Blueberry=1, Blackcurrant=2, Lingonberry=3, Cranberry=4) |
| Temp C | Fermentation temperature (°C) |
| Sugar g/L | Sugar concentration before fermentation |
| Time hours | Fermentation duration (converted uniformly from hours/days) |
| Numerical pH before ferm | pH before fermentation starts |
| aeration | Aeration level during fermentation |

**Target:** `Numerical pH post ferm` — pH value after fermentation

### Dataset Split

| Set | Size |
|---|---|
| Training | 391 rows (lab_df last 6 rows + 80% of syn_df) |
| Testing | 99 rows (lab_df first 2 rows + 20% of syn_df) |

---

## Data Preprocessing

The raw data required significant cleaning before modelling:

- **Time normalization** — mixed formats (`28h`, `7d`, `21 d`) parsed and converted to hours
- **Temperature cleaning** — ranges like `"22 to 25"` averaged; `°C` symbols stripped
- **pH extraction** — ranges like `"4.6-4.8"` averaged; non-numeric values coerced
- **Sugar standardization** — percentage and g/L formats unified to g/L
- **Fruit label encoding** — fruit names mapped to numeric codes; `"Black currant"` → `"Blackcurrant"` normalized
- **NaN handling** — missing values filled via column-level imputation; confirmed 0 NaNs in both dataframes post-cleaning
- **Feature scaling** — `StandardScaler` applied to `Sugar g/L`, `Numerical pH before ferm`, and `aeration`

---

## Correlation Analysis

<img width="370" height="253" alt="{6BAE6587-152E-472E-B7B1-C8140888A31F}" src="https://github.com/user-attachments/assets/9e735979-8844-48e0-b5b8-95c2ada91d82" />


Key findings from the heatmap:
- `Numerical pH before ferm` and `difference` show moderate correlation (0.65)
- Most fermentation features show **low direct correlation** with post-fermentation pH, motivating an ensemble approach

---

## Models Evaluated

Six regression models were trained and evaluated on the same train/test split:

| Model | MSE | R² |
|---|---|---|
| Random Forest | 0.1947 | 0.3645 |
| **Gradient Boosting** | **0.1914** | **0.3752** ⭐ |
| Extra Trees | 0.2128 | 0.3053 |
| Ada Boost | 0.2110 | 0.3112 |
| XGBoost | 0.2295 | 0.2509 |
| Linear Regression | 0.2736 | 0.1069 |

**Gradient Boosting** achieves the best R² (0.375) and lowest MSE (0.191) and is used as the production model.

> **Note:** R² values in the 0.30–0.38 range reflect the high natural variability in fermentation outcomes. The model captures meaningful trends but pH prediction from these features alone has inherent limits — consistent with the weak individual feature correlations observed in the heatmap.

---

## Web Interface

An interactive web app allows users to fill in fermentation parameters and receive a predicted post-fermentation pH instantly.

<img width="291" height="290" alt="{98D144E4-9246-4003-90D4-9AC1A35370B2}" src="https://github.com/user-attachments/assets/45607c18-c30e-4311-8ec6-3d9a5cf1299b" />



**Input fields:**
- Fruit type (dropdown)
- Fermentation temperature (°C)
- Sugar concentration (g/L)
- Fermentation time (hours)
- pH before fermentation
- Aeration level

**Output:** Predicted pH after fermentation

---

## Tech Stack

| Tool | Role |
|---|---|
| Python | Core language |
| Pandas | Data cleaning & preprocessing |
| Scikit-learn | Model training, scaling, evaluation |
| XGBoost | Gradient boosting regressor |
| Matplotlib / Seaborn | Correlation heatmap & visualizations |
| Web framework (Flask/Streamlit) | Interactive prediction interface |

---

## Installation & Usage

```bash
# Clone the repository
git clone https://github.com/zignut1035/Post-pH-prediction.git

```

Then open `http://localhost:5000` in your browser to use the prediction interface.

### Example Prediction

```python
example_features = {
    'Fruit Numeric': 1,        # Blueberry
    'Sugar g/L': 15.0,
    'Time hours': 28,
    'Numerical pH before ferm': 6.2,
    'Temp C': 37,
    'aeration': 22.8
}
# Actual pH:    3.20
# Predicted pH: 4.13
```

---

## Future Work

- **Larger real dataset** — the lab dataset is small; more real fermentation records would substantially improve model reliability
- **Feature engineering** — interaction terms (e.g. temp × time) or domain-derived features may improve R²
- **Hyperparameter tuning** — grid search or Bayesian optimization on the Gradient Boosting model
- **Expanded fruit types** — extend beyond the 4 current berry types

---

## Acknowledgements

This project was carried out as part of a work placement at atSauce, Turku, in collaboration with Turku University of Applied Sciences. Real fermentation data was collected from atSauce laboratory experiments. Synthetic data was generated to supplement the training set due to limited lab sample size.
