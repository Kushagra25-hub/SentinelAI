
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    average_precision_score
)


def evaluate_model(y_true, y_probabilities, threshold=0.5):
    """
    Evaluate a binary classification model using a probability threshold.
    """

    if len(y_true) != len(y_probabilities):
        raise ValueError("y_true and y_probabilities must have equal lengths")

    if len(y_true) == 0:
        raise ValueError("Evaluation data cannot be empty")

    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")

    if not all(0 <= p <= 1 for p in y_probabilities):
        raise ValueError("Probabilities must be between 0 and 1")

    # Convert probabilities into class predictions
    y_pred = (y_probabilities >= threshold).astype(int)

    # Calculate evaluation metrics
    metrics = {
        "Threshold": threshold,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1 Score": f1_score(y_true, y_pred, zero_division=0),
        "PR-AUC (Average Precision)": average_precision_score(
            y_true, y_probabilities
        )
    }

    # Generate confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

    confusion_df = pd.DataFrame(
        cm,
        index=["Actual Legitimate", "Actual Fraud"],
        columns=["Predicted Legitimate", "Predicted Fraud"]
    )

    return {
        "metrics": pd.DataFrame([metrics]),
        "confusion_matrix": confusion_df
    }
