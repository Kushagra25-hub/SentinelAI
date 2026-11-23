# SentinelAI – Intelligent ML Model Monitoring & Drift Detection Platform

An end-to-end Machine Learning project for credit card fraud detection, statistical drift monitoring, and model deployment using FastAPI and Streamlit.

## Overview

SentinelAI is an end-to-end machine learning platform designed to detect potentially fraudulent credit card transactions and monitor changes in machine learning model behavior.

The platform combines machine learning-based fraud detection, statistical drift detection, REST API deployment, and an interactive monitoring dashboard.

Unlike a standalone fraud classification model, SentinelAI also monitors changes in incoming data distributions and prediction behavior to help identify potential model reliability issues.

## Problem Statement

Credit card fraud detection presents several challenges:

- **Severe class imbalance:** Fraudulent transactions represent a very small percentage of total transactions.
- **Financial losses:** Undetected fraudulent transactions can cause financial damage to customers and financial institutions.
- **False positives:** Incorrectly flagging legitimate transactions can inconvenience customers and increase investigation costs.
- **Changing transaction patterns:** Incoming transaction distributions may change over time.
- **Model reliability:** A model that performs well during training may behave differently when exposed to new data.
- **Lack of monitoring:** Deployed ML models require continuous monitoring to identify potential changes in their behavior.

SentinelAI addresses these challenges by combining fraud prediction with statistical monitoring of transaction features and model prediction distributions.

## Key Features

### Fraud Detection
- Credit card fraud classification using Logistic Regression, Random Forest, and XGBoost.
- Class imbalance handling using class weighting and SMOTE.
- Decision threshold optimization using validation data.
- Evaluation using Precision, Recall, F1-score, and PR-AUC.
- Individual and batch transaction predictions.

### Data Drift Monitoring
- Feature distribution comparison between reference and current datasets.
- Kolmogorov–Smirnov (KS) statistical testing.
- Benjamini–Hochberg correction for multiple hypothesis testing.
- Feature-level drift reports and monitoring status.

### Prediction Drift Monitoring
- Comparison of reference and current prediction probability distributions.
- KS-based prediction drift detection.
- Monitoring of average fraud probabilities and predicted fraud rates.

### API Deployment
- REST API development using FastAPI.
- Single transaction prediction endpoint.
- Batch transaction prediction endpoint.
- Input validation and model information endpoints.

### Interactive Dashboard
- Streamlit-based monitoring dashboard.
- Single transaction fraud prediction.
- Batch CSV prediction.
- Model and API health information.
- Feature drift and prediction drift reports.
- Monitoring report downloads.

## Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Statistical Analysis | SciPy |
| Machine Learning | Scikit-learn, XGBoost |
| Imbalanced Data | Imbalanced-learn, SMOTE |
| Visualization | Matplotlib, Seaborn |
| API Development | FastAPI, Uvicorn |
| Dashboard | Streamlit |
| Development Environment | Jupyter Notebook, VS Code |
| Model Persistence | Joblib |
| Version Control | Git, GitHub |

## Dataset

**Dataset:** Credit Card Fraud Detection

**Source:** [Kaggle – Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

Dataset characteristics:

- 284,807 original transactions.
- 31 columns, including transaction features and target variable.
- 30 input features and one target column (`Class`).
- Target class 0 represents legitimate transactions.
- Target class 1 represents fraudulent transactions.
- Fraud prevalence is approximately 0.167%.

Exact duplicate rows were removed during preprocessing, resulting in 283,726 records.

The dataset contains anonymized PCA-transformed features (`V1`–`V28`), along with `Time` and `Amount`.

## Machine Learning Models

Three classification algorithms were trained and evaluated:

1. Logistic Regression
2. Random Forest
3. XGBoost

Experiments included:
- Baseline model training.
- Class-weighted training.
- SMOTE-based oversampling.
- Decision threshold optimization.
- Validation-based model comparison.
- Final evaluation on a held-out test set.

## Model Performance

The following results represent the selected baseline models evaluated on the held-out test dataset.

| Model | Precision | Recall | F1-score | PR-AUC |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.8434 | 0.7368 | 0.7865 | 0.6939 |
| Random Forest | 0.9467 | 0.7474 | 0.8353 | 0.7770 |
| XGBoost | 0.9589 | 0.7368 | 0.8333 | 0.8164 |

### Key Findings

- Random Forest achieved the highest F1-score among the selected baseline models.
- XGBoost achieved the highest PR-AUC.
- XGBoost achieved the highest precision.
- Thresholds were selected using validation data rather than the test set.

Random Forest was selected as the primary model for the prediction API.

**Note:** These are experimental results on a public dataset and do not represent production banking performance.

## Model Monitoring Methodology

SentinelAI implements two complementary monitoring approaches.

### 1. Feature Drift Detection

- Compares reference and current feature distributions.
- Uses the Kolmogorov–Smirnov test.
- Applies Benjamini–Hochberg correction at a 0.05 significance level.
- Generates feature-level monitoring reports.

Initial experiment:
- 30 features monitored.
- 3 features generated initial statistical drift signals.
- 0 features remained statistically significant after multiple-testing correction.

### 2. Prediction Drift Detection

- Compares fraud probability distributions between reference and current datasets.
- Uses the KS statistical test.
- Tracks changes in mean predicted fraud probability and predicted fraud rate.

Initial experiment:
- KS statistic: approximately 0.0117.
- P-value: approximately 0.000014.
- Prediction distribution drift was statistically detected.

A statistically significant result does not automatically mean that model accuracy has degraded. Further investigation using labeled data is required.

## System Architecture

```text
                 Credit Card Dataset
                         |
                         v
              Data Preprocessing & EDA
                         |
                         v
             ML Model Training & Evaluation
                         |
                         v
                Trained ML Models
                         |
                         v
                 Prediction Engine
                         |
              +----------+----------+
              |                     |
              v                     v
        FastAPI Backend       Drift Monitoring
              |                     |
              +----------+----------+
                         |
                         v
                Streamlit Dashboard
                         |
                         v
             Predictions & Monitoring
                    Reports
```

## Project Structure

```text
SentinelAI/
|
|-- data/
|   |-- raw/
|   |-- processed/
|
|-- dashboard/
|   |-- app.py
|
|-- models/
|   |-- random_forest_baseline.pkl
|   |-- random_forest_scaler.pkl
|   |-- random_forest_threshold.pkl
|   |-- logistic_regression_baseline.pkl
|   |-- xgboost_baseline.pkl
|
|-- notebooks/
|   |-- 01_data_understanding.ipynb
|   |-- 02_preprocessing_testing.ipynb
|
|-- src/
|   |-- __init__.py
|   |-- api.py
|   |-- data_preprocessing.py
|   |-- drift_monitor.py
|   |-- model_evaluation.py
|   |-- model_loader.py
|   |-- prediction_engine.py
|
|-- .gitignore
|-- requirements.txt
|-- README.md
```

## API Endpoints

The FastAPI backend provides the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks API health |
| GET | `/model-info` | Returns model information |
| POST | `/predict` | Predicts a single transaction |
| POST | `/predict/batch` | Predicts multiple transactions |

Interactive API documentation is available through Swagger UI.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/SentinelAI.git
cd SentinelAI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI backend

```bash
uvicorn src.api:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Start the Streamlit dashboard

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run dashboard/app.py
```

Dashboard:

```text
http://localhost:8501
```

## Limitations and Future Improvements

Current limitations:

- Drift experiments use randomly split reference and current datasets rather than genuinely time-ordered production data.
- Statistical drift does not necessarily indicate model performance degradation.
- Automatic model retraining is not implemented.
- The system is not connected to a live banking transaction platform.
- Production-scale monitoring and alerting have not yet been implemented.

Potential future improvements:

- Implement time-based drift monitoring.
- Add automated model retraining pipelines.
- Integrate real-time transaction streaming.
- Add monitoring alerts and notifications.
- Track model performance using delayed ground-truth labels.
- Add experiment tracking and model versioning.

## Learning Outcomes

This project demonstrates practical experience with:

- End-to-end machine learning workflows.
- Imbalanced classification problems.
- Model evaluation and threshold optimization.
- Statistical drift detection.
- Multiple hypothesis testing.
- ML model deployment using FastAPI.
- Interactive dashboards using Streamlit.
- Modular Python application development.

## Author

**Kushagra Srivastava**

Machine Learning / AI Engineer

GitHub:https://github.com/Kushagra25-hub

LinkedIn:https://www.linkedin.com/in/kushagrasri25/

## License

