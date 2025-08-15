import math
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LogisticRegression
from joblib import dump

data = pd.read_csv("../../data/featured/data.csv", sep=';')

Xtrain = data.drop('teamA_win', axis=1)
ytrain = data.teamA_win

scaler_mm = MinMaxScaler()
Xtrain_mm = scaler_mm.fit_transform(Xtrain)

scaler_st = StandardScaler()
Xtrain_st = scaler_st.fit_transform(Xtrain)

model = LogisticRegression(C = 0.01, penalty = 'l2', solver = 'saga')
model.fit(Xtrain_mm,ytrain)

dump(scaler_mm, "../../models/min_max_scaler.joblib")
dump(scaler_st, "../../models/standard_scaler.joblib")
dump(model, "../../models/logistic_regression.joblib")