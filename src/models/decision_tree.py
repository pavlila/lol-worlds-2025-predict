import math
import pandas as pd
import numpy as np

from sklearn.tree import DecisionTreeClassifier

from joblib import dump

data = pd.read_csv("../../data/featured/data.csv", sep=';')

Xtrain = data.drop('teamA_win', axis=1)
ytrain = data.teamA_win

model = DecisionTreeClassifier(max_depth=10)
model.fit(Xtrain, ytrain)

dump(model, '../../models/decision_tree.joblib')