# train_model.py (AI version)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import joblib

# 1. Dataset load
data = pd.read_csv("creditcard.csv")
X = data.drop("Class", axis=1)
y = data["Class"]

# 2. Scale features
scaler = StandardScaler()
X = scaler.fit_transform(X)
joblib.dump(scaler, "models/scaler.pkl")

# 3. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. ANN model
model = Sequential([
    Dense(64, activation="relu", input_dim=X_train.shape[1]),
    Dropout(0.3),
    Dense(32, activation="relu"),
    Dropout(0.2),
    Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# 5. Train model
model.fit(X_train, y_train, epochs=10, batch_size=2048, validation_split=0.2)

# 6. Save AI model
model.save("models/ai_fraud_model.h5")
print("✅ AI Model trained & saved as models/ai_fraud_model.h5")
