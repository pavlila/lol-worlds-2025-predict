import pandas as pd

def mergeSplits(splits):
    return pd.concat(splits, ignore_index=True)

def get_closest_past_stats(team_name, match_date, stats_df):
    team_data = stats_df[(stats_df["Team"] == team_name) & (stats_df["date"] < match_date)]
    if team_data.empty:
        return pd.Series(dtype=float)  # prázdný řádek
    return team_data.sort_values("date", ascending=False).iloc[0]

def merge_match_with_team_stats(matches_df, teams_df):
    matches_df = matches_df.copy()
    teams_df = teams_df.copy()

    # Ošetření formátu datumu
    matches_df["date"] = pd.to_datetime(matches_df["date"], errors="coerce")
    teams_df["date"] = pd.to_datetime(teams_df["date"], errors="coerce")

    # Vyhoď řádky s NaT (nepovedený převod)
    matches_df = matches_df.dropna(subset=["date"])
    teams_df = teams_df.dropna(subset=["date"])

    ignore_cols = {"Team", "tournament", "date"}  # tyto nechceš přidávat vůbec
    merged_rows = []

    for _, row in matches_df.iterrows():
        teamA = row["teamA"]
        teamB = row["teamB"]
        match_date = row["date"]

        stats_A = get_closest_past_stats(teamA, match_date, teams_df)
        stats_B = get_closest_past_stats(teamB, match_date, teams_df)

        # Odstraň ignorované sloupce
        stats_A = stats_A.drop(labels=ignore_cols, errors="ignore")
        stats_B = stats_B.drop(labels=ignore_cols, errors="ignore")

        # Přejmenuj zbytek
        stats_A = stats_A.add_prefix("A_")
        stats_B = stats_B.add_prefix("B_")

        # Sloučíme s původním řádkem – zajistíme unikátní indexy
        combined_data = pd.concat([row.drop(labels=ignore_cols, errors="ignore"), stats_A, stats_B])

        # Přidej zpět potřebné sloupce (např. tournament a date z match)
        combined_data["tournament"] = row["tournament"]
        combined_data["date"] = row["date"]

        merged_rows.append(combined_data)

    # Vrátíme dataframe
    return pd.DataFrame(merged_rows).reset_index(drop=True)

def rename(df):
    df["teamA"] = df["teamA"].replace({
    "Edward Gaming": "EDward Gaming",
    "Hanwha Life eSports": "Hanwha Life Esports",
    "PSG Talon": "TALON",
    "BNK FearX": "BNK FEARX",
    "GIANTX": "GiantX",
    "OMG": "Oh My God",
    "Fluxo": "Fluxo W7M",
    "Gen.G eSports": "Gen.G",
    "Anyone s Legend": "Anyone's Legend",
    "Isurus": "Isurus Estral",
    "Funplus Phoenix": "FunPlus Phoenix",
    "OK BRION": "OKSavingsBank BRION",
    "TT": "ThunderTalk Gaming"
    })

    df["teamB"] = df["teamB"].replace({
    "Edward Gaming": "EDward Gaming",
    "Hanwha Life eSports": "Hanwha Life Esports",
    "PSG Talon": "TALON",
    "BNK FearX": "BNK FEARX",
    "GIANTX": "GiantX",
    "OMG": "Oh My God",
    "Fluxo": "Fluxo W7M",
    "Gen.G eSports": "Gen.G",
    "Anyone s Legend": "Anyone's Legend",
    "Isurus": "Isurus Estral",
    "Funplus Phoenix": "FunPlus Phoenix",
    "OK BRION": "OKSavingsBank BRION",
    "TT": "ThunderTalk Gaming"
    })

    return df

teams_winter = pd.read_csv("../../data/cleaned/teams_winter.csv", sep=';')
teams_spring = pd.read_csv("../../data/cleaned/teams_spring.csv", sep=';')
teams_msi = pd.read_csv("../../data/cleaned/teams_msi.csv", sep=';')
teams_ewc = pd.read_csv("../../data/cleaned/teams_ewc.csv", sep=';')

teams = mergeSplits([teams_winter,teams_spring,teams_msi,teams_ewc])

new_match = pd.read_csv("../../data/cleaned/new_match.csv", sep=';')
new_match = rename(new_match)

new_data = merge_match_with_team_stats(new_match, teams)

new_data.to_csv("../../data/merged/new_data.csv", sep=';', index=False)