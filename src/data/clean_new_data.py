import pandas as pd

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

def newMatchesCleanByMatch(df):
    df.columns = df.columns.str.strip()
    df = df[['teamA','teamB','date','tournament']].copy()

    df = renameTeamsInMatches(df)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df

new_match = pd.read_csv("../../user/new_match.csv", sep=',')
new_match = newMatchesCleanByMatch(new_match)
new_match.to_csv("../../data/cleaned/new_match.csv", sep=',', index=False)