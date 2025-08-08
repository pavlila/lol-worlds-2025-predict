from joblib import load
import pandas as pd

dt = load("models/decision_tree.joblib")
rf = load("models/random_forest.joblib")
xgb = load("models/xg_boost.joblib")

data = pd.read_csv("data/featured/new_data.csv", sep=';')
data = data.drop('teamA_win', axis=1)

prediction = dt.predict(data)
print(f"Decision Tree: {prediction}")

prediction = rf.predict(data)
print(f"Random Forest: {prediction}")

prediction = xgb.predict(data)
print(f"XGBoost: {prediction}")