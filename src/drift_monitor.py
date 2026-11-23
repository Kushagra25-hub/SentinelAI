
import pandas as pd
from scipy.stats import ks_2samp
from statsmodels.stats.multitest import multipletests


def detect_feature_drift(reference_data, current_data, alpha=0.05):
    """
    Detect feature-level distribution drift using the KS test
    and Benjamini-Hochberg multiple-testing correction.
    """

    if not isinstance(reference_data, pd.DataFrame):
        raise TypeError("reference_data must be a pandas DataFrame")

    if not isinstance(current_data, pd.DataFrame):
        raise TypeError("current_data must be a pandas DataFrame")

    if reference_data.empty or current_data.empty:
        raise ValueError("Reference and current datasets cannot be empty")

    if set(reference_data.columns) != set(current_data.columns):
        raise ValueError("Reference and current features must match")

    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    current_data = current_data[reference_data.columns]

    results = []

    for feature in reference_data.columns:
        reference_values = reference_data[feature].dropna()
        current_values = current_data[feature].dropna()

        if reference_values.empty or current_values.empty:
            raise ValueError(f"Feature '{feature}' has no valid observations")

        ks_statistic, p_value = ks_2samp(
            reference_values,
            current_values
        )

        results.append({
            "Feature": feature,
            "KS Statistic": ks_statistic,
            "P-Value": p_value
        })

    drift_df = pd.DataFrame(results)

    # Correct p-values for multiple comparisons
    reject, adjusted_p_values, _, _ = multipletests(
        drift_df["P-Value"],
        alpha=alpha,
        method="fdr_bh"
    )

    drift_df["Adjusted P-Value"] = adjusted_p_values
    drift_df["Drift Detected"] = drift_df["P-Value"] < alpha
    drift_df["Significant After Correction"] = reject

    return drift_df


def detect_prediction_drift(reference_probabilities, current_probabilities, alpha=0.05):
    """
    Detect drift in model prediction probabilities using the KS test.
    """

    reference_probabilities = pd.Series(reference_probabilities).dropna()
    current_probabilities = pd.Series(current_probabilities).dropna()

    if reference_probabilities.empty or current_probabilities.empty:
        raise ValueError("Prediction probability arrays cannot be empty")

    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    ks_statistic, p_value = ks_2samp(
        reference_probabilities,
        current_probabilities
    )

    return {
        "KS Statistic": ks_statistic,
        "P-Value": p_value,
        "Drift Detected": bool(p_value < alpha),
        "Reference Mean": reference_probabilities.mean(),
        "Current Mean": current_probabilities.mean()
    }


def generate_monitoring_report(feature_drift_df, prediction_drift_result):
    """
    Combine feature-level and prediction-level drift results.
    """

    initial_drift_count = int(
        feature_drift_df["Drift Detected"].sum()
    )

    confirmed_drift_count = int(
        feature_drift_df["Significant After Correction"].sum()
    )

    prediction_drift_detected = prediction_drift_result["Drift Detected"]

    if prediction_drift_detected:
        overall_status = "DRIFT DETECTED"
    elif initial_drift_count > 0:
        overall_status = "WARNING"
    else:
        overall_status = "STABLE"

    report = {
        "Overall Status": overall_status,
        "Total Features Monitored": len(feature_drift_df),
        "Initial Feature Drift Signals": initial_drift_count,
        "Confirmed Feature Drift": confirmed_drift_count,
        "Prediction Drift Detected": prediction_drift_detected,
        "Prediction KS Statistic": prediction_drift_result["KS Statistic"],
        "Prediction P-Value": prediction_drift_result["P-Value"],
        "Reference Mean Probability": prediction_drift_result["Reference Mean"],
        "Current Mean Probability": prediction_drift_result["Current Mean"]
    }

    return pd.DataFrame([report])

