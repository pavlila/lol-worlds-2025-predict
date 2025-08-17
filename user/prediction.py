from joblib import load
import pandas as pd

dt = load("../models/decision_tree.joblib")
rf = load("../models/random_forest.joblib")
xgb = load("../models/xg_boost.joblib")
lr = load("../models/logistic_regression.joblib")

scaler_mm = load("../models/min_max_scaler.joblib")
scaler_st = load("../models/standard_scaler.joblib")

data = pd.read_csv("../data/featured/new_data.csv", sep=';')
decode_maps = load("../data/featured/decode_maps.joblib")

teamA_names = data['teamA'].map(decode_maps['teamA'])
teamB_names = data['teamB'].map(decode_maps['teamB'])

print(f"\nTeam A: {teamA_names[0]}")
print(f"Team B: {teamB_names[0]}\n")

prediction = dt.predict(data)
print(f"Decision Tree: {'Win' if prediction[0] == 1 else 'Lose'}")

prediction = rf.predict(data)
print(f"Random Forest: {'Win' if prediction[0] == 1 else 'Lose'}")

prediction = xgb.predict(data)
print(f"XGBoost: {'Win' if prediction[0] == 1 else 'Lose'}")

data_scaled_mm = scaler_mm.transform(data)
data_scaled_st = scaler_st.transform(data)
prediction = lr.predict(data_scaled_st)
print(f"Logistic regression: {'Win' if prediction[0] == 1 else 'Lose'}")
