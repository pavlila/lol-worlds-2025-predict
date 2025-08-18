import pandas as pd
import numpy as np
from joblib import load

def setFavorite(row):
    if row['winrate%_B'] > row['winrate%_A']:

        a_cols = [c for c in row.index if c.endswith('_A')]
        for a_col in a_cols:
            base = a_col[:-2]
            b_col = f'{base}_B'
            row[a_col], row[b_col] = row[b_col], row[a_col]

        row['teamA'], row['teamB'] = row['teamB'], row['teamA']

        return row
    return row
    

def makeDiff(df):
    a_cols = [c for c in df.columns if c.endswith('_A')]
    b_cols = [c for c in df.columns if c.endswith('_B')]

    for a_col in a_cols:
        base = a_col[:-2]
        b_col = f'{base}_B'

        if b_col in b_cols:
            df[f'diff_{base}'] = df[a_col] - df[b_col]
            df[f'ratio_{base}'] = df[a_col] / (df[b_col] + 1e-6)

    df = df.drop(columns=a_cols + b_cols)
    return df

def makeFeature(df):
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df = df.drop(columns=['date'])
        
    decode_maps = load("../../data/featured/decode_maps.joblib")

    for col, mapping in decode_maps.items():
        df[col] = df[col].map({v: k for k, v in mapping.items()}).fillna(-1).astype(int)
    
    df = df.fillna(-1)
    df = makeDiff(df)

    return df

new_data = pd.read_csv("../../data/merged/new_data.csv", sep=';')

new_data = makeFeature(new_data)

new_data.to_csv("../../data/featured/new_data.csv", sep=';', index=False)