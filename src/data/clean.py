import pandas as pd
import numpy as np

def renameTeamsInMatches(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize team names in a match dataset for consistency.

    This function replaces alternative spellings or legacy names 
    of teams in the 'teamA' and 'teamB' columns with a unified 
    naming convention. Useful for linking match data with other 
    datasets (e.g. team statistics).

    Args:
        df (pd.DataFrame): DataFrame of matches containing columns 
            'teamA' and 'teamB' with potentially inconsistent team names.

    Returns:
        pd.DataFrame: DataFrame with standardized team names in 
            columns 'teamA' and 'teamB'.
    """
    replace_map = {
        'Edward Gaming': 'EDward Gaming',
        'Hanwha Life eSports': 'Hanwha Life Esports',
        'TALON': 'PSG Talon',
        'BNK FearX': 'BNK FEARX',
        'GIANTX': 'GiantX',
        'OMG': 'Oh My God',
        'Fluxo': 'Fluxo W7M',
        'Gen.G eSports': 'Gen.G',
        'Anyone s Legend': "Anyone's Legend",
        'Isurus Estral': 'Isurus',
        'Funplus Phoenix': 'FunPlus Phoenix',
        'OK BRION': 'OKSavingsBank BRION',
        'TT': 'ThunderTalk Gaming'  
    }

    df[['teamA', 'teamB']] = df[['teamA', 'teamB']].replace(replace_map).copy()
    return df

def matchesClean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess raw match data.

    This function selects relevant columns from the raw matches dataset,
    standardizes team names, converts scores to numeric values, creates
    a binary target feature 'teamA_win', and parses the match date.

    Specifically:
        - Keeps only ['tournament', 'date', 'teamA', 'teamB', 'scoreA', 'scoreB']
        - Converts 'scoreA' and 'scoreB' to numeric
        - Creates new column 'teamA_win' (1 if teamA wins, else 0)
        - Drops 'scoreA' and 'scoreB'
        - Standardizes team names via 'renameTeamsInMatches'
        - Converts 'date' to datetime

    Args:
        df (pd.DataFrame): Raw matches DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame with columns:
            - 'tournament' (str)
            - 'date' (datetime64)
            - 'teamA' (str, standardized)
            - 'teamB' (str, standardized)
            - 'teamA_win' (int, 0/1)
    """
    df.columns = df.columns.str.strip()
    df = df[['tournament','date','teamA','teamB','scoreA','scoreB']].copy()

    df['scoreA'] = pd.to_numeric(df['scoreA'], errors='coerce')
    df['scoreB'] = pd.to_numeric(df['scoreB'], errors='coerce')

    df['teamA_win'] = (df['scoreA'] > df['scoreB']).astype(int)
    df = df.drop(columns=['scoreA','scoreB'])

    df = renameTeamsInMatches(df)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def teamsClean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess raw team statistics.

    This function converts numeric columns, calculates winrate, 
    normalizes percentage columns, and ensures proper date formatting.

    Specifically:
        - Converts 'W' (wins) and 'GP' (games played) to numeric
        - Creates 'winrate%' column as W / GP
        - Drops unused columns: ['W', 'L', 'K', 'D']
        - Converts percentage columns (e.g. 'FB%', 'FT%', 'GRB%') 
          from string with '%' to float in range [0, 1]
        - Converts 'date' to datetime

    Args:
        df (pd.DataFrame): Raw DataFrame of team statistics.

    Returns:
        pd.DataFrame: Cleaned DataFrame with numeric, normalized 
            percentage values and standardized columns.
    """
    df['W'] = pd.to_numeric(df['W'], errors='coerce').fillna(0)
    df['GP'] = pd.to_numeric(df['GP'], errors='coerce').fillna(0)
    df['winrate%'] = df['W'] / df['GP']

    df = df.drop(columns=['W','L','K','D'])
    percent_cols = ['FB%','FT%','F3T%','HLD%','GRB%','FD%','DRG%','ELD%','FBN%','GSPD','BN%','LNE%','JNG%']

    for col in percent_cols:
        if col in df.columns:
            df[col] = (df[col].astype(str).str.replace('%', '', regex=False).replace('nan', np.nan).astype(float) / 100)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def main() -> None:
    """
    Batch process for cleaning match and team data.

    Reads raw CSV files, applies cleaning functions, 
    and saves cleaned datasets.
    """
    # List of seasons/tournaments to process for matches
    dfs_matches = ['winter', 'spring', 'summer', 'msi', 'ewc', 'fst']

    # Process and clean matches data
    for df_match in dfs_matches:
        df = pd.read_csv(f"../../data/raw/matches_{df_match}.csv", sep=r'\t|\s{2,}', engine='python')
        df_clean = matchesClean(df)
        df_clean.to_csv(f"../../data/cleaned/matches_{df_match}.csv", sep=',', index=False)

    # List of seasons/tournaments to process for teams
    dfs_teams = ['winter', 'spring', 'summer', 'msi', 'ewc', 'fst']

    # Process and clean teams data
    for df_team in dfs_teams:
        df = pd.read_csv(f"../../data/raw/teams_{df_team}.csv", sep=',')
        df_clean = teamsClean(df)
        df_clean.to_csv(f"../../data/cleaned/teams_{df_team}.csv", sep=',', index=False)

if __name__ == "__main__":
    main()