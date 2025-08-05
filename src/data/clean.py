import pandas as pd

def matchesClean(df, split, prefix):
    df.columns = df.columns.str.strip()
    df = df[['teamA','scoreA','scoreB','teamB','date']].copy()
    df['match_id'] = prefix + df.index.astype(str)

    def divideMatchOnMaps(row):
        results = [1]*int(row['scoreA']) + [0]*int(row['scoreB'])
        return pd.DataFrame([{
            'match_id': row['match_id'],
            'game_in_series': i + 1,
            'teamA': row['teamA'],
            'teamB': row['teamB'],
            'teamA_win': win,
            'date': row['date'],
            'split': split
        } for i, win in enumerate(results)])
    
    return pd.concat(df.apply(divideMatchOnMaps, axis=1).tolist(), ignore_index=True)

def teamsClean(df, split):
    df = df.drop(columns=['Season'])
    df['split'] = split
    return df

matches_winter = pd.read_csv("../../data/raw/matches_winter.csv", sep=r'\t|\s{2,}', engine='python')
matches_spring = pd.read_csv("../../data/raw/matches_spring.csv", sep=r'\t|\s{2,}', engine='python')
matches_summer = pd.read_csv("../../data/raw/matches_summer.csv", sep=r'\t|\s{2,}', engine='python')

matches_winter = matchesClean(matches_winter, 1, 'winter_')
matches_spring = matchesClean(matches_spring, 2, 'spring_')
matches_summer = matchesClean(matches_summer, 3, 'summer_')

matches_winter.to_csv("../../data/cleaned/matches_winter.csv", sep=';', index=False)
matches_spring.to_csv("../../data/cleaned/matches_spring.csv", sep=';', index=False)
matches_summer.to_csv("../../data/cleaned/matches_summer.csv", sep=';', index=False)

teams_winter = pd.read_csv("../../data/raw/teams_winter.csv", sep=r'\t|\s{2,}', engine='python')
teams_spring = pd.read_csv("../../data/raw/teams_spring.csv", sep=r'\t|\s{2,}', engine='python')
teams_summer = pd.read_csv("../../data/raw/teams_summer.csv", sep=r'\t|\s{2,}', engine='python')

teams_winter = teamsClean(teams_winter, 1)
teams_spring = teamsClean(teams_spring, 2)
teams_summer = teamsClean(teams_summer, 3)

teams_winter.to_csv("../../data/cleaned/teams_winter.csv", sep=';', index=False)
teams_spring.to_csv("../../data/cleaned/teams_spring.csv", sep=';', index=False)
teams_summer.to_csv("../../data/cleaned/teams_summer.csv", sep=';', index=False)