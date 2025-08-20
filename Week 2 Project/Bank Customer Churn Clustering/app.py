
from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model pipeline
model_pipeline = joblib.load('churn_model_pipeline.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from form
        data = request.form.to_dict()
        
        # Convert necessary fields to numeric types
        data['CreditScore'] = int(data['CreditScore'])
        data['Age'] = int(data['Age'])
        data['Tenure'] = int(data['Tenure'])
        data['Balance'] = float(data['Balance'])
        data['NumOfProducts'] = int(data['NumOfProducts'])
        data['HasCrCard'] = int(data['HasCrCard'])
        data['IsActiveMember'] = int(data['IsActiveMember'])
        data['EstimatedSalary'] = float(data['EstimatedSalary'])

        # Create a DataFrame from the input
        input_df = pd.DataFrame([data])

        # Make prediction
        prediction = model_pipeline.predict(input_df)
        probability = model_pipeline.predict_proba(input_df)

        # Prepare the result
        if prediction[0] == 1:
            result_text = f"This customer is likely to CHURN with a probability of {probability[0][1]:.2f}."
        else:
            result_text = f"This customer is likely to STAY with a probability of {probability[0][0]:.2f}."
            
        return render_template('index.html', prediction_result=result_text)

    except Exception as e:
        return render_template('index.html', prediction_result=f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
