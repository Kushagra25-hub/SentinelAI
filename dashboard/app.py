
import pandas as pd
import streamlit as st
import requests
import json
from pathlib import Path

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SentinelAI | Fraud Monitoring",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------
# API Configuration
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SAMPLE_FILE = (
    PROJECT_ROOT / "data" / "processed" / "dashboard_samples.json"
)

# --------------------------------------------------
# Dashboard Header
# --------------------------------------------------

st.title("🛡️ SentinelAI")
st.subheader("Intelligent ML Model Monitoring & Fraud Detection")

st.markdown(
    "Monitor machine learning models, detect transaction fraud, "
    "and track prediction drift."
)

st.divider()

# --------------------------------------------------
# System Status
# --------------------------------------------------

st.header("System Status")

try:
    response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )

    response.raise_for_status()
    health_data = response.json()

    st.success("SentinelAI API is connected and running.")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("API Status", "Healthy")

    with col2:
        st.metric("Application", health_data["application"])

except requests.exceptions.RequestException:
    st.error(
        "Cannot connect to SentinelAI API. "
        "Make sure the FastAPI server is running."
    )

st.divider()

# --------------------------------------------------
# Active Model Information
# --------------------------------------------------

st.header("Active ML Model")

model_info = None

try:
    response = requests.get(
        f"{API_URL}/model-info",
        timeout=5
    )

    response.raise_for_status()
    model_info = response.json()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Model", model_info["model_name"])

    with col2:
        st.metric(
            "Classification Threshold",
            f'{model_info["classification_threshold"]:.2f}'
        )

    with col3:
        st.metric(
            "Features",
            model_info["expected_features"]
        )

except requests.exceptions.RequestException:
    st.warning("Model information is currently unavailable.")

st.divider()

# --------------------------------------------------
# Single Transaction Fraud Prediction
# --------------------------------------------------

st.header("🔍 Fraud Detection")

st.write(
    "Enter transaction features to predict whether "
    "a transaction is fraudulent."
)

if model_info is not None:

    feature_names = model_info["feature_names"]

    # ----------------------------------------------
    # Load Sample Transactions
    # ----------------------------------------------

    st.subheader("Load Sample Transaction")

    try:
        if not SAMPLE_FILE.exists():
            st.error(
                f"Sample file not found: {SAMPLE_FILE}"
            )
            dashboard_samples = None

        else:
            with open(SAMPLE_FILE, "r", encoding="utf-8") as file:
                dashboard_samples = json.load(file)

        if dashboard_samples is not None:

            sample_type = st.selectbox(
                "Choose transaction type",
                [
                    "Select sample type",
                    "Legitimate",
                    "Fraudulent"
                ]
            )

            if st.button("Load Sample", key="load_sample"):

                if sample_type == "Select sample type":
                    st.warning(
                        "Please select a transaction type first."
                    )

                else:
                    selected_sample = dashboard_samples[sample_type]

                    for feature in feature_names:
                        st.session_state[
                            f"single_{feature}"
                        ] = float(selected_sample[feature])

                    st.session_state["sample_loaded"] = sample_type

                    st.success(
                        f"{sample_type} sample loaded successfully!"
                    )

    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        st.error(f"Unable to load sample transactions: {error}")

    # ----------------------------------------------
    # Transaction Input Form
    # ----------------------------------------------

    st.divider()
    st.subheader("Transaction Details")

    with st.form("single_prediction_form"):

        transaction_features = {}

        columns = st.columns(3)

        for index, feature in enumerate(feature_names):

            widget_key = f"single_{feature}"

            if widget_key not in st.session_state:
                st.session_state[widget_key] = 0.0

            with columns[index % 3]:

                transaction_features[feature] = st.number_input(
                    feature,
                    format="%.8f",
                    key=widget_key
                )

        submitted = st.form_submit_button(
            "Analyze Transaction",
            use_container_width=True
        )

    # ----------------------------------------------
    # Generate Prediction
    # ----------------------------------------------

    if submitted:

        payload = {
            "features": transaction_features
        }

        try:
            with st.spinner("Analyzing transaction..."):

                response = requests.post(
                    f"{API_URL}/predict",
                    json=payload,
                    timeout=15
                )

            if response.status_code == 200:

                result = response.json()

                st.divider()
                st.subheader("Prediction Result")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Fraud Probability",
                        f'{result["fraud_probability"]:.2%}'
                    )

                with col2:
                    st.metric(
                        "Predicted Class",
                        result["predicted_class"]
                    )

                with col3:
                    st.metric(
                        "Classification Threshold",
                        f'{result["threshold"]:.2f}'
                    )

                if result["predicted_class"] == 1:
                    st.error(
                        "⚠️ Fraudulent transaction detected!"
                    )

                else:
                    st.success(
                        "✅ Transaction classified as legitimate."
                    )

            else:
                st.error(
                    f"Prediction failed: {response.text}"
                )

        except requests.exceptions.RequestException as error:
            st.error(f"Unable to connect to prediction API: {error}")

else:
    st.warning(
        "Fraud prediction is unavailable because model information "
        "could not be retrieved from the API."
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()


# --------------------------------------------------
# ML Model Monitoring Dashboard
# --------------------------------------------------

st.divider()
st.header("📊 ML Model Monitoring")

processed_dir = PROJECT_ROOT / "data" / "processed"

monitoring_file = processed_dir / "overall_monitoring_report.csv"
feature_file = processed_dir / "feature_drift_report.csv"
prediction_file = processed_dir / "prediction_drift_report.csv"

if monitoring_file.exists():

    try:
        monitoring_df = pd.read_csv(monitoring_file)

        if monitoring_df.empty:
            st.warning("The monitoring report is empty.")

        else:
            report = monitoring_df.iloc[0]

            # Load feature-level report
            feature_df = (
                pd.read_csv(feature_file)
                if feature_file.exists()
                else pd.DataFrame()
            )

            # ------------------------------------------
            # KPI Metrics
            # ------------------------------------------

            st.subheader("Monitoring Overview")

            total_features = (
                len(feature_df)
                if not feature_df.empty
                else 0
            )

            initial_signals = int(
                report["Initial Feature Drift Signals"]
            )

            confirmed_drift = int(
                report["Confirmed Feature Drift"]
            )

            prediction_status = str(
                report["Prediction Monitoring Status"]
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Features Monitored",
                    total_features
                )

            with col2:
                st.metric(
                    "Initial Drift Signals",
                    initial_signals
                )

            with col3:
                st.metric(
                    "Confirmed Feature Drift",
                    confirmed_drift
                )

            with col4:
                st.metric(
                    "Prediction Monitoring",
                    prediction_status
                )

            # ------------------------------------------
            # Overall Monitoring Status
            # ------------------------------------------

            st.subheader("Overall Monitoring Status")

            overall_status = str(
                report["Overall Monitoring Status"]
            )

            if overall_status == "DRIFT DETECTED":
                st.error(f"⚠️ {overall_status}")

            elif overall_status == "WARNING":
                st.warning(f"⚠️ {overall_status}")

            else:
                st.success(f"✅ {overall_status}")

            # ------------------------------------------
            # Prediction Drift Statistics
            # ------------------------------------------

            st.subheader("Prediction Distribution Drift")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "KS Statistic",
                    f'{report["Prediction KS Statistic"]:.6f}'
                )

            with col2:
                st.metric(
                    "P-Value",
                    f'{report["Prediction P-Value"]:.6f}'
                )

            # ------------------------------------------
            # Feature-Level Drift Analysis
            # ------------------------------------------

            st.subheader("Feature-Level Drift Analysis")

            if not feature_df.empty:

                st.dataframe(
                    feature_df,
                    use_container_width=True
                )

                if "Monitoring Status" in feature_df.columns:
                    status_counts = (
                        feature_df["Monitoring Status"].value_counts()
                    )
                    
                    st.subheader("Feature Drift Status Distribution")
                    st.bar_chart(status_counts)

            else:
                st.warning(
                    "Feature-level drift report is unavailable."
                )

            # ------------------------------------------
            # Prediction Drift Report
            # ------------------------------------------

            st.subheader("Prediction Drift Report")

            if prediction_file.exists():

                prediction_df = pd.read_csv(prediction_file)

                st.dataframe(
                    prediction_df,
                    use_container_width=True
                )

            else:
                st.warning(
                    "Prediction drift report is unavailable."
                )

            # ------------------------------------------
            # Download Reports
            # ------------------------------------------

            st.subheader("Download Monitoring Reports")

            col1, col2, col3 = st.columns(3)

            with col1:
                with open(monitoring_file, "rb") as file:
                    st.download_button(
                        "Overall Report",
                        data=file,
                        file_name="overall_monitoring_report.csv",
                        mime="text/csv",
                        key="download_overall_report"
                    )

            with col2:
                if feature_file.exists():
                    with open(feature_file, "rb") as file:
                        st.download_button(
                            "Feature Drift Report",
                            data=file,
                            file_name="feature_drift_report.csv",
                            mime="text/csv",
                            key="download_feature_report"
                        )

            with col3:
                if prediction_file.exists():
                    with open(prediction_file, "rb") as file:
                        st.download_button(
                            "Prediction Drift Report",
                            data=file,
                            file_name="prediction_drift_report.csv",
                            mime="text/csv",
                            key="download_prediction_report"
                        )

    except (KeyError, ValueError, OSError) as error:
        st.error(f"Unable to display monitoring reports: {error}")

else:
    st.warning(
        "Overall monitoring report not found. "
        "Generate it using the drift monitoring notebook."
    )

st.divider()

st.caption(
    "SentinelAI | Intelligent ML Model Monitoring Platform"
)



# --------------------------------------------------
# Batch Fraud Prediction
# --------------------------------------------------

st.divider()

st.header("📂 Batch Fraud Prediction")

st.write(
    "Upload a CSV file containing multiple transactions "
    "to analyze them together."
)

if model_info is not None:

    feature_names = model_info["feature_names"]

    uploaded_file = st.file_uploader(
        "Upload transaction CSV",
        type=["csv"],
        key="batch_csv"
    )

    if uploaded_file is not None:

        try:
            batch_df = pd.read_csv(uploaded_file)

            st.subheader("Uploaded Transaction Data")

            st.write("Dataset shape:", batch_df.shape)

            st.dataframe(batch_df.head(10), use_container_width=True)

            missing_features = [
                feature for feature in feature_names
                if feature not in batch_df.columns
            ]

            extra_features = [
                feature for feature in batch_df.columns
                if feature not in feature_names
            ]

            if missing_features:
                st.error(
                    f"Missing required features: {missing_features}"
                )

            elif extra_features:
                st.error(
                    f"Unexpected columns found: {extra_features}"
                )

            else:

                if st.button(
                    "Analyze All Transactions",
                    key="batch_predict"
                ):

                    batch_payload = {
                        "transactions": [
                            {"features": row}
                            for row in batch_df[feature_names].to_dict(
                                orient="records"
                            )
                        ]
                    }

                    with st.spinner(
                        "Analyzing transactions..."
                    ):

                        response = requests.post(
                            f"{API_URL}/predict/batch",
                            json=batch_payload,
                            timeout=120
                        )

                    if response.status_code == 200:

                        batch_results = response.json()

                        results_df = pd.DataFrame(
                            batch_results["results"]
                        )

                        st.subheader("Batch Prediction Results")

                        total = len(results_df)

                        fraud_count = int(
                            (results_df["predicted_class"] == 1).sum()
                        )

                        legitimate_count = total - fraud_count

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric(
                                "Total Transactions",
                                total
                            )

                        with col2:
                            st.metric(
                                "Fraudulent Transactions",
                                fraud_count
                            )

                        with col3:
                            st.metric(
                                "Legitimate Transactions",
                                legitimate_count
                            )

                        st.dataframe(
                            results_df,
                            use_container_width=True
                        )

                        csv_data = results_df.to_csv(
                            index=False
                        ).encode("utf-8")

                        st.download_button(
                            "Download Prediction Report",
                            data=csv_data,
                            file_name="sentinelai_batch_predictions.csv",
                            mime="text/csv"
                        )

                    else:
                        st.error(
                            f"Batch prediction failed: {response.text}"
                        )

        except Exception as error:
            st.error(f"Unable to process uploaded CSV: {error}")

else:
    st.warning(
        "Batch prediction is unavailable because model information "
        "could not be retrieved."
    )
