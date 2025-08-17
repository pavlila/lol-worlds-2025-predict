import math
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from joblib import dump

data = pd.read_csv("../../data/featured/data.csv", sep=';')

Xtrain = data.drop('teamA_win', axis=1)
ytrain = data.teamA_win

model = RandomForestClassifier(max_depth=6, n_estimators=35)
model.fit(Xtrain, ytrain)

dump(model, '../../models/random_forest.joblib')