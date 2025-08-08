from joblib import load
import pandas as pd

dt = load("models/decision_tree.joblib")

data = pd.read_csv("data/featured/new_data.csv", sep=';')
data = data.drop('teamA_win', axis=1)

prediction = dt.predict(data)

print(prediction)