from joblib import load
import pandas as pd

dt = load("models/decision_tree.joblib")
rf = load("models/random_forest.joblib")
xgb = load("models/xg_boost.joblib")
lr = load("models/logistic_regression.joblib")

scaler_mm = load("models/min_max_scaler.joblib")

data = pd.read_csv("data/featured/new_data.csv", sep=';')
data = data.drop('teamA_win', axis=1)

prediction = dt.predict(data)
print(f"Decision Tree: {prediction}")

prediction = rf.predict(data)
print(f"Random Forest: {prediction}")

prediction = xgb.predict(data)
print(f"XGBoost: {prediction}")

data_scaled_mm = scaler_mm.transform(data)
prediction = lr.predict(data_scaled_mm)
print(f"Logistic regression: {prediction}")