import pandas as pd
import numpy as np

def renameTeamsInMatches(df):
    replace_map = {
        "Edward Gaming": "EDward Gaming",
        "Hanwha Life eSports": "Hanwha Life Esports",
        "TALON": "PSG Talon",
        "BNK FearX": "BNK FEARX",
        "GIANTX": "GiantX",
        "OMG": "Oh My God",
        "Fluxo": "Fluxo W7M",
        "Gen.G eSports": "Gen.G",
        "Anyone s Legend": "Anyone's Legend",
        "Isurus Estral": "Isurus",
        "Funplus Phoenix": "FunPlus Phoenix",
        "OK BRION": "OKSavingsBank BRION",
        "TT": "ThunderTalk Gaming"  
    }

    df[["teamA", "teamB"]] = df[["teamA", "teamB"]].replace(replace_map).copy()

    return df

def matchesClean(df):
    df.columns = df.columns.str.strip()
    df = df[['tournament','date','teamA','teamB','scoreA','scoreB']].copy()

    df['scoreA'] = pd.to_numeric(df['scoreA'], errors='coerce')
    df['scoreB'] = pd.to_numeric(df['scoreB'], errors='coerce')

    df['teamA_win'] = (df['scoreA'] > df['scoreB']).astype(int)
    df = df.drop(columns=['scoreA','scoreB'])

    df = renameTeamsInMatches(df)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df

def teamsClean(df):
    df['W'] = pd.to_numeric(df['W'], errors='coerce').fillna(0)
    df['GP'] = pd.to_numeric(df['GP'], errors='coerce').fillna(0)

    df['winrate%'] = df['W'] / df['GP']

    df = df.drop(columns=['W','L','K','D'])

    percent_cols = ['FB%','FT%','F3T%','HLD%','GRB%','FD%','DRG%','ELD%','FBN%','GSPD','BN%','LNE%','JNG%']

    for col in percent_cols:
        if col in df.columns:
            df[col] = (df[col].astype(str).str.replace('%', '', regex=False).replace('nan', np.nan).astype(float) / 100)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df

dfs_matches = ['winter', 'spring', 'summer', 'msi', 'ewc']

for df_match in dfs_matches:
    df = pd.read_csv(f"../../data/raw/matches_{df_match}.csv", sep=r'\t|\s{2,}', engine='python')
    df_clean = matchesClean(df)
    df_clean.to_csv(f"../../data/cleaned/matches_{df_match}.csv", sep=',', index=False)

dfs_teams = ['winter', 'spring', 'summer', 'msi', 'ewc']

for df_team in dfs_teams:
    df = pd.read_csv(f"../../data/raw/teams_{df_team}.csv", sep=',')
    df_clean = teamsClean(df)
    df_clean.to_csv(f"../../data/cleaned/teams_{df_team}.csv", sep=',', index=False)