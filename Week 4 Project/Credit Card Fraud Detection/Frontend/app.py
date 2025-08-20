import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title="CreditCare • AI Fraud Detection", layout="wide")

st.title("💳 CreditCare • AI Based Credit Card Fraud Detection")
st.write("Upload a CSV to get fraud predictions using the trained AI model (Neural Network).")

# ---- Load AI Model and Scaler ----
try:
    model = tf.keras.models.load_model("models/ai_fraud_model.h5")
    scaler = joblib.load("models/scaler.pkl")
    model_status = "✅ AI model loaded successfully!"
except Exception as e:
    model = None
    scaler = None
    model_status = f"⚠️ Failed to load model: {e}"

with st.sidebar:
    st.header("Model Status")
    st.info(model_status)

uploaded = st.file_uploader("Upload a CSV file with transactions", type=["csv"])

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        st.stop()

    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head(20), use_container_width=True)

    if model is None or scaler is None:
        st.warning("AI model or scaler not loaded. Please retrain and try again.")
        st.stop()

    # Drop target column if present
    if "Class" in df.columns:
        X = df.drop("Class", axis=1)
    else:
        X = df.copy()

    # Scale features
    X_scaled = scaler.transform(X)

    # Predictions
    preds_proba = model.predict(X_scaled)
    preds = (preds_proba > 0.5).astype(int)

    # Add predictions to dataframe
    df["Fraud_Probability"] = preds_proba
    df["AI_Prediction"] = preds

    st.subheader("AI Prediction Results")
    st.dataframe(df.head(50), use_container_width=True)

    # Metrics
    fraud_count = int((df["AI_Prediction"] == 1).sum())
    non_fraud_count = int((df["AI_Prediction"] == 0).sum())
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fraud Transactions", fraud_count)
    with col2:
        st.metric("Non-Fraud Transactions", non_fraud_count)

    # Plot
    fig, ax = plt.subplots()
    df["AI_Prediction"].value_counts().sort_index().plot(kind="bar", ax=ax)
    ax.set_xticklabels(["Non-Fraud", "Fraud"], rotation=0)
    ax.set_ylabel("Count")
    ax.set_title("AI Prediction Distribution")
    st.pyplot(fig)

    # Download results
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    st.download_button(
        label="Download Predictions CSV",
        data=buf.getvalue().encode("utf-8"),
        file_name="ai_predictions.csv",
        mime="text/csv",
    )
else:
    st.caption("📂 Upload a CSV file to start predictions.")
