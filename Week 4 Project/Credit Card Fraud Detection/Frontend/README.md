
# CreditCare Fraud App

Streamlit frontend + training script for Credit Card Fraud Detection.

## Files
- `app.py` — Streamlit frontend (predictions UI)
- `train_model.py` — Train and save a model pipeline (`models/fraud_pipeline.pkl`)
- `requirements.txt` — Python dependencies
- `models/` — Folder where the trained pipeline is saved

## Step-by-step (Windows / macOS / Linux)

1) **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

2) **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

3) **Train the model (once)**
   Put your labeled CSV (with target column, usually `Class`) anywhere and run:
   ```bash
   python train_model.py --csv path/to/your/creditcard.csv --target Class --save-path models/fraud_pipeline.pkl
   ```
   This will print ROC‑AUC and save the pipeline to `models/fraud_pipeline.pkl`.

4) **Run the frontend**
   ```bash
   streamlit run app.py
   ```
   Open the URL shown (usually `http://localhost:8501`).

5) **Use the app**
   - Upload a CSV with the same schema as the training data (it may contain `Class` or not).
   - The app will predict and show counts + a bar chart.
   - Click **Download Predictions CSV** to save results.

## Notes
- If your dataset uses a different target name, change `--target` accordingly.
- The current model is Logistic Regression with class balancing. You can swap it later.
- Make sure the columns at prediction time match the training columns for best results.
