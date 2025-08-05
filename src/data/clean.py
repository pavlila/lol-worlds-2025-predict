import pandas as pd

def matchesClean(df, prefix=''):
    df.columns = df.columns.str.strip()
    df = df[['teamA','scoreA','scoreB','teamB']].copy()
    df['match_id'] = prefix + df.index.astype(str)

    def devideMatchOnMaps(row):
        results = [1]*int(row['scoreA']) + [0]*int(row['scoreB'])
        return pd.DataFrame([{
            'match_id': row['match_id'],
            'game_in_series': i + 1,
            'teamA': row['teamA'],
            'teamB': row['teamB'],
            'teamA_win': win
        } for i, win in enumerate(results)])
    
    return pd.concat(df.apply(devideMatchOnMaps, axis=1).tolist(), ignore_index=True)

matches_winter = pd.read_csv("../../data/raw/matches_winter.csv", sep=r'\t|\s{2,}', engine='python')
matches_spring = pd.read_csv("../../data/raw/matches_spring.csv", sep=r'\t|\s{2,}', engine='python')

matches_winter = matchesClean(matches_winter)
matches_spring = matchesClean(matches_spring)

matches_winter.to_csv("../../data/cleaned/matches_winter.csv", sep=';', index=False)
matches_spring.to_csv("../../data/cleaned/matches_spring.csv", sep=';', index=False)