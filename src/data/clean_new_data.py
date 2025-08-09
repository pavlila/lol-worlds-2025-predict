import pandas as pd
import numpy as np

def newMatchesClean(df, prefix):
    df.columns = df.columns.str.strip()
    df = df[['teamA','number_of_matches','teamB','date','tournament']].copy()
    df['match_id'] = prefix + df.index.astype(str)

    def divideMatchOnMaps(row):
        results = range(row['number_of_matches'])
        return pd.DataFrame([{
            'tournament': row['tournament'],
            'match_id': row['match_id'],
            'game_in_series': i + 1,
            'teamA': row['teamA'],
            'teamB': row['teamB'],
            'teamA_win': np.nan,
            'date': row['date'],
        } for i, win in enumerate(results)])
    
    return pd.concat(df.apply(divideMatchOnMaps, axis=1).tolist(), ignore_index=True)

new_match = pd.read_csv("../../user/new_match.csv", sep=';')

new_match = newMatchesClean(new_match, 'worlds_')
new_match.to_csv("../../data/cleaned/new_match.csv", sep=';', index=False)