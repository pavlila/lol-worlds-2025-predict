import pandas as pd
import numpy as np

def matchesCleanByMatch(df):
    df.columns = df.columns.str.strip()
    df = df[['tournament','date','teamA','teamB','scoreA','scoreB']].copy()
    df['win'] = (df['scoreA'] > df['scoreB']).astype(int)
    df = df.drop(columns=['scoreA','scoreB'])

    return df

def teamsClean(df):
    df = df.drop(columns=['Season'])
    return df

matches_winter = pd.read_csv("../../data/raw/matches_winter.csv", sep=r'\t|\s{2,}', engine='python')
matches_spring = pd.read_csv("../../data/raw/matches_spring.csv", sep=r'\t|\s{2,}', engine='python')
matches_msi = pd.read_csv("../../data/raw/matches_msi.csv", sep=r'\t|\s{2,}', engine='python')
matches_ewc = pd.read_csv("../../data/raw/matches_ewc.csv", sep=r'\t|\s{2,}', engine='python')

matches_winter = matchesCleanByMatch(matches_winter)
matches_spring = matchesCleanByMatch(matches_spring)
matches_msi = matchesCleanByMatch(matches_msi)
matches_ewc = matchesCleanByMatch(matches_ewc)

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