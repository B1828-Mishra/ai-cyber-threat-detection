import streamlit as st
import requests
import pandas as pd
import joblib
import os

# Project path
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEATURE_PATH = os.path.join(
    BASE_PATH,
    "models",
    "feature_names.pkl"
)

# Load feature names
feature_names = joblib.load(FEATURE_PATH)

# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="AI Cyber Threat Detection",
    page_icon="Shield",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------

st.title("AI Cyber Threat Detection System")
st.write("Machine Learning based network traffic threat detection")

st.divider()

# -----------------------------
# CSV Upload
# -----------------------------

st.subheader("Upload Network Traffic Dataset")

uploaded_file = st.file_uploader(
    "Upload a CIC-IDS-2017 CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        st.success("CSV file uploaded successfully!")

        # Clean column names
        df.columns = df.columns.str.strip()

        # Dataset information
        st.write("### Dataset Preview")
        st.dataframe(df.head())

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        # -----------------------------
        # Check required features
        # -----------------------------

        missing_features = [
            feature
            for feature in feature_names
            if feature not in df.columns
        ]

        if missing_features:

            st.error(
                f"The uploaded file is missing "
                f"{len(missing_features)} required features."
            )

            st.write("Missing features:")
            st.write(missing_features)

        else:

            st.success("All 78 required features found!")

            # Select exactly the 78 model features
            X = df[feature_names].copy()

            # Convert values to numbers
            X = X.apply(pd.to_numeric, errors="coerce")

            # Replace infinite values
            X = X.replace(
                [float("inf"), float("-inf")],
                0
            )

            # Replace missing values
            X = X.fillna(0)

            st.write("### Threat Detection")

            # Limit first test to 100 flows
            max_rows = min(len(X), 100)

            st.info(
                f"The system will analyze the first "
                f"{max_rows} network flows."
            )

            # -----------------------------
            # Detection button
            # -----------------------------

            if st.button("Detect Threats"):

                predictions = []
                probabilities = []

                progress = st.progress(0)

                for i in range(max_rows):

                    features = X.iloc[i].tolist()

                    try:

                        response = requests.post(
                            "http://127.0.0.1:8000/predict",
                            json={
                                "features": features
                            }
                        )

                        result = response.json()

                        if "error" in result:
                            st.error(result["error"])
                            break

                        predictions.append(
                            result["prediction"]
                        )

                        probabilities.append(
                            result["attack_probability"]
                        )

                    except requests.exceptions.ConnectionError:

                        st.error(
                            "Could not connect to FastAPI. "
                            "Make sure Uvicorn is running."
                        )

                        break

                    progress.progress(
                        (i + 1) / max_rows
                    )

                # -----------------------------
                # Display results
                # -----------------------------

                if len(predictions) == max_rows:

                    results = df.iloc[:max_rows].copy()

                    results["Prediction"] = predictions

                    results["Attack Probability"] = probabilities

                    st.success(
                        f"Successfully analyzed "
                        f"{max_rows} network flows!"
                    )

                    # -----------------------------
                    # Summary
                    # -----------------------------

                    benign_count = predictions.count(
                        "BENIGN"
                    )

                    attack_count = predictions.count(
                        "ATTACK"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Benign Traffic",
                            benign_count
                        )

                    with col2:
                        st.metric(
                            "Attack Traffic",
                            attack_count
                        )

                    st.divider()

                    # -----------------------------
                    # Results table
                    # -----------------------------

                    st.subheader(
                        "Detection Results"
                    )

                    st.dataframe(
                        results[
                            [
                                "Prediction",
                                "Attack Probability"
                            ]
                        ],
                        use_container_width=True
                    )

    except Exception as e:

        st.error(
            f"Error reading CSV file: {e}"
        )