
import pandas as pd


def predict_transaction(transaction_data, model, scaler, threshold):
    """
    Predict whether a transaction is fraudulent.

    Parameters:
        transaction_data: pandas DataFrame containing transaction features
        model: trained ML model
        scaler: fitted StandardScaler
        threshold: fraud classification threshold

    Returns:
        Dictionary containing fraud probability and prediction.
    """

    if not isinstance(transaction_data, pd.DataFrame):
        raise TypeError("transaction_data must be a pandas DataFrame")

    if transaction_data.empty:
        raise ValueError("transaction_data cannot be empty")

    # Validate feature names and order
    expected_features = list(scaler.feature_names_in_)

    missing_features = [
        feature for feature in expected_features
        if feature not in transaction_data.columns
    ]

    extra_features = [
        feature for feature in transaction_data.columns
        if feature not in expected_features
    ]

    if missing_features or extra_features:
        raise ValueError(
            f"Missing features: {missing_features}; "
            f"Unexpected features: {extra_features}"
        )

    # Arrange features in the original training order
    transaction_data = transaction_data[expected_features].copy()

    # Apply the fitted scaler
    scaled_data = pd.DataFrame(
        scaler.transform(transaction_data),
        columns=expected_features,
        index=transaction_data.index
    )

    # Generate fraud probabilities
    fraud_probabilities = model.predict_proba(scaled_data)[:, 1]

    # Apply classification threshold
    predictions = (fraud_probabilities >= threshold).astype(int)

    # Return results
    results = pd.DataFrame({
        "Fraud Probability": fraud_probabilities,
        "Predicted Class": predictions,
        "Prediction Label": [
            "Fraud" if prediction == 1 else "Legitimate"
            for prediction in predictions
        ]
    }, index=transaction_data.index)

    return results
