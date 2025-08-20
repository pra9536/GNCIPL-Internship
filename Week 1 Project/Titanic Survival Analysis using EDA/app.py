from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load("titanic_model.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        pclass = int(request.form['pclass'])
        sex = request.form['sex']
        age = float(request.form['age'])
        sibsp = int(request.form['sibsp'])
        parch = int(request.form['parch'])
        fare = float(request.form['fare'])
        embarked = request.form['embarked']

        sex = 1 if sex == "female" else 0
        embarked_dict = {"C": 0, "Q": 1, "S": 2}
        embarked = embarked_dict[embarked]

        input_data = pd.DataFrame({
            "Pclass": [pclass],
            "Sex": [sex],
            "Age": [age],
            "SibSp": [sibsp],
            "Parch": [parch],
            "Fare": [fare],
            "Embarked": [embarked]
        })

        prediction = model.predict(input_data)[0]
        result = "🎉 Survived!" if prediction == 1 else "❌ Did not survive."

        return render_template('result.html', prediction=result)

if __name__ == "__main__":
    app.run(debug=True)
