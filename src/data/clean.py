import pandas as pd

def matchesClean(df, prefix):
    df.columns = df.columns.str.strip()
    df = df[['teamA','scoreA','scoreB','teamB','date','tournament']].copy()
    df['match_id'] = prefix + df.index.astype(str)

    def divideMatchOnMaps(row):
        results = [1]*int(row['scoreA']) + [0]*int(row['scoreB'])
        return pd.DataFrame([{
            'tournament': row['tournament'],
            'match_id': row['match_id'],
            'game_in_series': i + 1,
            'teamA': row['teamA'],
            'teamB': row['teamB'],
            'teamA_win': win,
            'date': row['date'],
        } for i, win in enumerate(results)])
    
    return pd.concat(df.apply(divideMatchOnMaps, axis=1).tolist(), ignore_index=True)

def teamsClean(df):
    df = df.drop(columns=['Season'])
    return df

matches_winter = pd.read_csv("../../data/raw/matches_winter.csv", sep=r'\t|\s{2,}', engine='python')
matches_spring = pd.read_csv("../../data/raw/matches_spring.csv", sep=r'\t|\s{2,}', engine='python')
matches_msi = pd.read_csv("../../data/raw/matches_msi.csv", sep=r'\t|\s{2,}', engine='python')
matches_ewc = pd.read_csv("../../data/raw/matches_ewc.csv", sep=r'\t|\s{2,}', engine='python')

matches_winter = matchesClean(matches_winter, 'winter_')
matches_spring = matchesClean(matches_spring, 'spring_')
matches_msi = matchesClean(matches_msi, 'msi_')
matches_ewc = matchesClean(matches_ewc, 'ewc_')

matches_winter.to_csv("../../data/cleaned/matches_winter.csv", sep=';', index=False)
matches_spring.to_csv("../../data/cleaned/matches_spring.csv", sep=';', index=False)
matches_msi.to_csv("../../data/cleaned/matches_msi.csv", sep=';', index=False)
matches_ewc.to_csv("../../data/cleaned/matches_ewc.csv", sep=';', index=False)

teams_winter = pd.read_csv("../../data/raw/teams_winter.csv", sep=',')
teams_spring = pd.read_csv("../../data/raw/teams_spring.csv", sep=',')
teams_msi = pd.read_csv("../../data/raw/teams_msi.csv", sep=',')
teams_ewc = pd.read_csv("../../data/raw/teams_ewc.csv", sep=',')

teams_winter.to_csv("../../data/cleaned/teams_winter.csv", sep=';', index=False)
teams_spring.to_csv("../../data/cleaned/teams_spring.csv", sep=';', index=False)
teams_msi.to_csv("../../data/cleaned/teams_msi.csv", sep=';', index=False)
teams_ewc.to_csv("../../data/cleaned/teams_ewc.csv", sep=';', index=False)