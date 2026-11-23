
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from typing import Dict
from typing import List
import math

from src.model_loader import load_model_artifacts
from src.prediction_engine import predict_transaction

app = FastAPI(
    title="SentinelAI",
    description="Intelligent ML Model Monitoring and Fraud Detection Platform",
    version="1.0.0"
)

# Load model artifacts once when the API starts
rf_artifacts = load_model_artifacts("random_forest")

rf_model = rf_artifacts["model"]
rf_scaler = rf_artifacts["scaler"]
rf_threshold = rf_artifacts["threshold"]

# Get the exact feature names expected by the model
FEATURE_NAMES = list(rf_scaler.feature_names_in_)

def validate_transaction_features(features):
    """
    Validate transaction feature names and numerical values.
    """

    if set(features.keys()) != set(FEATURE_NAMES):
        missing = set(FEATURE_NAMES) - set(features.keys())
        extra = set(features.keys()) - set(FEATURE_NAMES)

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Invalid transaction features",
                "missing_features": sorted(missing),
                "extra_features": sorted(extra)
            }
        )

    # Reject NaN and infinite values
    invalid_values = [
        name for name, value in features.items()
        if not math.isfinite(value)
    ]

    if invalid_values:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Transaction contains invalid numerical values",
                "invalid_features": invalid_values
            }
        )


class TransactionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    features: Dict[str, float] = Field(
        ...,
        description="Transaction features required by the model"
    )


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "SentinelAI",
        "message": "API is running successfully!"
    }


@app.post("/predict")
def predict(input_data: TransactionInput):
    
    validate_transaction_features(input_data.features)

    # Validate required features
    if set(input_data.features.keys()) != set(FEATURE_NAMES):
        missing = set(FEATURE_NAMES) - set(input_data.features.keys())
        extra = set(input_data.features.keys()) - set(FEATURE_NAMES)

        raise HTTPException(
            status_code=422,
            detail={
                "missing_features": sorted(missing),
                "extra_features": sorted(extra)
            }
        )

    try:
        # Convert input into a DataFrame
        transaction_df = pd.DataFrame(
            [input_data.features],
            columns=FEATURE_NAMES
        )

        # Generate prediction
        result = predict_transaction(
            transaction_data=transaction_df,
            model=rf_model,
            scaler=rf_scaler,
            threshold=rf_threshold
        )

        return {
            "fraud_probability": float(
                result["Fraud Probability"].iloc[0]
            ),
            "predicted_class": int(
                result["Predicted Class"].iloc[0]
            ),
            "prediction_label": result["Prediction Label"].iloc[0],
            "threshold": rf_threshold
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


class BatchTransactionInput(BaseModel):
    transactions: List[TransactionInput] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of transactions to evaluate"
    )


@app.post("/predict/batch")
def predict_batch(input_data: BatchTransactionInput):

    results = []

    for index, transaction in enumerate(input_data.transactions):

        try:
            validate_transaction_features(transaction.features)

        except HTTPException as error:
            raise HTTPException(
        status_code=error.status_code,
        detail={
            "transaction_index": index,
            "validation_error": error.detail
            }
        )

        try:
            # Convert transaction into a DataFrame
            transaction_df = pd.DataFrame(
                [transaction.features],
                columns=FEATURE_NAMES
            )

            # Generate prediction
            result = predict_transaction(
                transaction_data=transaction_df,
                model=rf_model,
                scaler=rf_scaler,
                threshold=rf_threshold
            )

            results.append({
                "transaction_index": index,
                "fraud_probability": float(
                    result["Fraud Probability"].iloc[0]
                ),
                "predicted_class": int(
                    result["Predicted Class"].iloc[0]
                ),
                "prediction_label": result["Prediction Label"].iloc[0]
            })

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"Transaction {index}: {str(error)}"
            )

    return {
        "total_transactions": len(results),
        "results": results
    }



@app.get("/model-info")
def get_model_info():
    """
    Return information about the active ML model.
    """

    return {
        "application": "SentinelAI",
        "model_name": "Random Forest Classifier",
        "model_type": type(rf_model).__name__,
        "classification_threshold": rf_threshold,
        "expected_features": len(FEATURE_NAMES),
        "feature_names": FEATURE_NAMES,
        "prediction_endpoints": [
            "/predict",
            "/predict/batch"
        ]
    }



# Required for transaction DataFrame creation
import pandas as pd
