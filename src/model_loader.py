
from pathlib import Path
import joblib


# Locate the project-level models directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"


def load_model_artifacts(model_name="random_forest"):
    """
    Load a trained model, its scaler, and classification threshold.

    Supported models:
    - random_forest
    - logistic_regression
    - xgboost
    """

    supported_models = [
        "random_forest",
        "logistic_regression",
        "xgboost"
    ]

    if model_name not in supported_models:
        raise ValueError(
            f"Unsupported model: {model_name}. "
            f"Choose from {supported_models}"
        )

    model_path = MODEL_DIR / f"{model_name}_baseline.pkl"
    scaler_path = MODEL_DIR / f"{model_name}_scaler.pkl"
    threshold_path = MODEL_DIR / f"{model_name}_threshold.pkl"

    # Check that all files exist
    for path in [model_path, scaler_path, threshold_path]:
        if not path.exists():
            raise FileNotFoundError(
                f"Required model artifact not found: {path}"
            )

    # Load artifacts
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    threshold = joblib.load(threshold_path)

    print(f"{model_name} artifacts loaded successfully!")
    print("Model:", model_path.name)
    print("Scaler:", scaler_path.name)
    print("Threshold:", threshold)

    return {
        "model": model,
        "scaler": scaler,
        "threshold": float(threshold)
    }
