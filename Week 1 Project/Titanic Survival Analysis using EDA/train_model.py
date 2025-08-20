import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Dataset load
data = pd.read_csv("Titanic-Dataset - Copy.csv")

# 2. Select features and target
X = data[["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]]
y = data["Survived"]

# 3. Handle missing values
X["Age"].fillna(X["Age"].median(), inplace=True)
X["Fare"].fillna(X["Fare"].median(), inplace=True)
X["Embarked"].fillna("S", inplace=True)

# 4. Encode categorical values
le_sex = LabelEncoder()
X["Sex"] = le_sex.fit_transform(X["Sex"])   # male=1, female=0 or vice versa

le_embarked = LabelEncoder()
X["Embarked"] = le_embarked.fit_transform(X["Embarked"])  # C=0, Q=1, S=2

# 5. Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Train Model (Logistic Regression)
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# 7. Save Model
joblib.dump(model, "titanic_model.pkl")

print("✅ Model trained and saved as titanic_model.pkl")
