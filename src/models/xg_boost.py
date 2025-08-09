import math
import pandas as pd
import numpy as np

import xgboost as xgb

from joblib import dump

data = pd.read_csv("../../data/featured/data.csv", sep=';')

Xtrain = data.drop('teamA_win', axis=1)
ytrain = data.teamA_win

model = xgb.XGBClassifier(
        eval_metric='logloss',
        max_depth=3,
        learning_rate=0.25,
        n_estimators=192
    )
model.fit(Xtrain, ytrain)

dump(model, '../../models/xg_boost.joblib')