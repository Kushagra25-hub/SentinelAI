
import pandas as pd
import streamlit as st
import requests
import json
from pathlib import Path

# --------------------------------------------------
# API and Project Configuration
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SAMPLE_FILE = (
    PROJECT_ROOT / "data" / "processed" / "dashboard_samples.json"
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SentinelAI | Fraud Monitoring",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------
# SentinelAI Dark Theme
# --------------------------------------------------

st.markdown("""


<style>

/* ==========================================
   SENTINELAI — PREMIUM MONOCHROME THEME
========================================== */

:root {
    --bg: #090909;
    --surface: #171717;
    --surface-hover: #242424;
    --border: #383838;
    --text: #FFFFFF;
    --muted: #A3A3A3;
    --button: #FFFFFF;
    --button-text: #000000;
}

/* GLOBAL APPLICATION */
.stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: "Inter", sans-serif;
}

/* FULL WIDTH LAYOUT */
.block-container {
    width: 100% !important;
    max-width: 100% !important;
    padding: 1.5rem 2rem 3rem 2rem !important;
}

/* HIDE SIDEBAR */
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* ==========================================
   TYPOGRAPHY
========================================== */

h1, h2, h3, h4, h5, h6 {
    color: var(--text) !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

p, label {
    color: #E5E5E5;
}

small {
    color: var(--muted) !important;
}

/* Remove blue welcome heading accent */
h1 span,
h2 span {
    color: #FFFFFF !important;
}

/* ==========================================
   TOP NAVIGATION
========================================== */

div[data-testid="stRadio"] {
    width: 100% !important;
}

/* Hide radio widget label */
div[data-testid="stRadio"] > label {
    display: none !important;
}

/* Navigation container */
div[role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    align-items: center !important;
    flex-wrap: nowrap !important;
    width: 100% !important;
    min-height: 80px !important;
    padding: 35px !important;
    gap: 100px !important;
    background: #black !important;
    border: 1px solid #black !important;
    border-radius: 50px !important;
}

/* Navigation options */
div[role="radiogroup"] label {
    display: flex !important;
    flex: 1 1 0 !important;
    min-width: 0 !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 12px 8px !important;
    margin: 0 !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

/* Remove radio circles */
div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

div[role="radiogroup"] label input[type="radio"] {
    position: absolute !important;
    opacity: 0 !important;
    width: 1px !important;
    height: 1px !important;
}

/* Navigation text */
div[role="radiogroup"] label p {
    color: #E5E5E5 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    margin: 0 !important;
}

/* Active navigation */
div[role="radiogroup"] label:has(input:checked) {
    background: #FFFFFF !important;
}

div[role="radiogroup"] label:has(input:checked) p {
    color: #000000 !important;
    font-weight: 750 !important;
}

/* Navigation hover */
div[role="radiogroup"] label:hover:not(:has(input:checked)) {
    background: #303030 !important;
    border-color: #666666 !important;
}



/* ==========================================
   METRIC CARDS
========================================== */

[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    border-color: #777777 !important;
    transform: translateY(-2px);
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 13px !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
}

[data-testid="stMetricDelta"] {
    color: #D4D4D4 !important;
}

/* ==========================================
   ALL BUTTONS — CONSISTENT DESIGN
========================================== */

.stButton button,
.stFormSubmitButton button,
.stDownloadButton button {
    background: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #FFFFFF !important;
    border-radius: 9px !important;
    min-height: 42px !important;
    padding: 10px 20px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    opacity: 1 !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
}

/* Button text and icons */
.stButton button *,
.stFormSubmitButton button *,
.stDownloadButton button * {
    color: #000000 !important;
}

/* Button hover */
.stButton button:hover:not(:disabled),
.stFormSubmitButton button:hover:not(:disabled),
.stDownloadButton button:hover:not(:disabled) {
    background: #D4D4D4 !important;
    color: #000000 !important;
    border-color: #D4D4D4 !important;
}

/* Disabled buttons */
.stButton button:disabled,
.stFormSubmitButton button:disabled,
.stDownloadButton button:disabled {
    background: #D4D4D4 !important;
    color: #555555 !important;
    border-color: #D4D4D4 !important;
    opacity: 1 !important;
    cursor: not-allowed !important;
}

/* Keyboard focus */
.stButton button:focus-visible,
.stFormSubmitButton button:focus-visible,
.stDownloadButton button:focus-visible {
    outline: 2px solid #FFFFFF !important;
    outline-offset: 3px !important;
}

/* ==========================================
   FILE UPLOADER
========================================== */

[data-testid="stFileUploader"] {
    background: #171717 !important;
    border: 1px dashed #666666 !important;
    border-radius: 12px !important;
    padding: 15px !important;
}

/* Upload button */
[data-testid="stFileUploader"] button {
    background: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #FFFFFF !important;
    border-radius: 9px !important;
    min-height: 42px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

[data-testid="stFileUploader"] button * {
    color: #000000 !important;
}

[data-testid="stFileUploader"] button:hover {
    background: #D4D4D4 !important;
    border-color: #D4D4D4 !important;
}

[data-testid="stFileUploader"] small {
    color: #D4D4D4 !important;
}

/* ==========================================
   INPUT FIELDS
========================================== */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: #171717 !important;
    color: #FFFFFF !important;
    border: 1px solid #444444 !important;
    border-radius: 8px !important;
}

.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    background: #171717 !important;
    border-color: #444444 !important;
    border-radius: 8px !important;
}

/* Input focus */
.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border-color: #FFFFFF !important;
    box-shadow: 0 0 0 1px #FFFFFF !important;
}

/* ==========================================
   DATA TABLES
========================================== */

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid #383838 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ==========================================
   ALERTS AND STATUS
========================================== */

.stAlert {
    border-radius: 10px !important;
}

/* ==========================================
   CHART CONTAINERS
========================================== */

[data-testid="stPlotlyChart"],
[data-testid="stVegaLiteChart"] {
    background: #171717 !important;
    border: 1px solid #383838 !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* ==========================================
   DIVIDERS
========================================== */

hr {
    border: none !important;
    border-top: 1px solid #383838 !important;
    margin-top: 2px!important;
    margin-bottom: 1.5rem !important;
}

/* ==========================================
   RESPONSIVE DESIGN
========================================== */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    div[role="radiogroup"] {
        flex-wrap: wrap !important;
    }

    div[role="radiogroup"] label {
        flex: 1 1 45% !important;
    }
}

@media (max-width: 600px) {

    div[role="radiogroup"] {
        gap: 4px !important;
    }

    div[role="radiogroup"] label {
        flex: 1 1 100% !important;
    }

    div[role="radiogroup"] label p {
        font-size: 13px !important;
    }
}

</style>

""", unsafe_allow_html=True)




# --------------------------------------------------
# SENTINELAI PREMIUM NAVBAR
# --------------------------------------------------

nav_left, nav_center, nav_right = st.columns(
    [1.5, 6, 1.5],
    vertical_alignment="center"
)

with nav_left:
    st.markdown("""
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            white-space:nowrap;
            padding:8px 0;
        ">
            <span style="font-size:34px;">🛡️</span>
            <span style="
                color:#FFFFFF;
                font-size:27px;
                font-weight:800;
                letter-spacing:-1px;
            ">SentinelAI</span>
        </div>
    """, unsafe_allow_html=True)

with nav_center:
    selected_page = st.radio(
        "Navigation",
        [
            "Overview",
            "Fraud Detection",
            "Batch Analysis",
            "Model Monitoring"
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="top_navigation"
    )

with nav_right:
    st.markdown("""
        <div style="
            display:flex;
            justify-content:flex-end;
            align-items:center;
            gap:8px;
            white-space:nowrap;
            padding:10px 0;
        ">
            <span style="color:#FFFFFF;">●</span>
            <span style="
                color:#FFFFFF;
                font-size:12px;
                font-weight:700;
                letter-spacing:0.5px;
            ">SYSTEM ONLINE</span>
        </div>
    """, unsafe_allow_html=True)

st.divider()


# --------------------------------------------------
# API Configuration and Model Information
# --------------------------------------------------

model_info = None
health_data = None
api_connected = False

try:
    health_response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )
    health_response.raise_for_status()
    health_data = health_response.json()
    api_connected = True

except requests.exceptions.RequestException:
    api_connected = False

try:
    model_response = requests.get(
        f"{API_URL}/model-info",
        timeout=5
    )
    model_response.raise_for_status()
    model_info = model_response.json()

except requests.exceptions.RequestException:
    model_info = None


# --------------------------------------------------
# Overview Page
# --------------------------------------------------

if selected_page == "Overview":
    st.markdown("""
    <h1 style="
        color: #FFFFFF;
        font-size: 44px;
        font-weight: 800;
        letter-spacing: -1px;
    ">
        Welcome to SentinelAI
    </h1>

    <p style="
        color: #A3A3A3;
        font-size: 16px;
    ">
        Intelligent Fraud Detection & ML Model Monitoring Platform
    </p>
    """, unsafe_allow_html=True)


    st.divider()

    st.subheader("System Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        status = "Connected" if api_connected else "Offline"
        st.metric("API Status", status)

    with col2:
        st.metric(
            "Active Model",
            model_info["model_name"] if model_info else "Unavailable"
        )

    with col3:
        st.metric(
            "Input Features",
            model_info["expected_features"] if model_info else "N/A"
        )

    st.divider()

    st.subheader("Active Model Configuration")

    if model_info is not None:

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Model Type",
                model_info["model_type"]
            )

        with col2:
            st.metric(
                "Classification Threshold",
                f'{model_info["classification_threshold"]:.2f}'
            )

        st.success("Model information loaded successfully.")

    else:
        st.warning("Model information is currently unavailable.")

    if api_connected:
        st.success("SentinelAI API is connected and running.")
    else:
        st.error(
            "Cannot connect to SentinelAI API. "
            "Please start the FastAPI server."
        )

# --------------------------------------------------
# Fraud Detection Page
# --------------------------------------------------

if selected_page == "Fraud Detection":


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

            # Basic transaction features
            st.markdown("### Basic Features")

            basic_features = ["Time", "Amount"]

            basic_columns = st.columns(2)

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
# Model Monitoring Page
# --------------------------------------------------

if selected_page == "Model Monitoring":

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
# Batch Analysis Page
# --------------------------------------------------

if selected_page == "Batch Analysis":   

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
