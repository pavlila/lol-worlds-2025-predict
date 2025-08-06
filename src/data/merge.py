import pandas as pd

def matchesAndTeamsMerge(matches, teams):
    data = matches.merge(teams, how='left', left_on='teamA', right_on='Name')
    data = data.rename(columns=lambda x: x if x in ['teamA','teamB','teamA_win','match_id','game_in_series','date','split'] else f"{x}_A")
    data = data.drop(columns=['Name_A'], errors='ignore')

    data = data.merge(teams, how='left', left_on='teamB', right_on='Name')
    data = data.rename(columns=lambda x: x if x in ['teamA','teamB','teamA_win','match_id','game_in_series','date','split'] or x.endswith('_A') else f"{x}_B")
    data = data.drop(columns=['Name_B'], errors='ignore')
    return data

def mergeSplits(splits):
    return pd.concat(splits, ignore_index=True)


import pandas as pd

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



matches_winter = pd.read_csv("../../data/cleaned/matches_winter.csv", sep=';')
#matches_spring = pd.read_csv("../../data/cleaned/matches_spring.csv", sep=';')
#matches_summer = pd.read_csv("../../data/cleaned/matches_summer.csv", sep=';')
#matches_msi = pd.read_csv("../../data/cleaned/matches_msi.csv", sep=';')
#matches_ewc = pd.read_csv("../../data/cleaned/matches_ewc.csv", sep=';')

#teams_winter = pd.read_csv("../../data/cleaned/teams_winter.csv", sep=';')
#teams_spring = pd.read_csv("../../data/cleaned/teams_spring.csv", sep=';')
#teams_summer = pd.read_csv("../../data/cleaned/teams_summer.csv", sep=';')
teams_winter_daily = pd.read_csv("../../data/cleaned/teams_winter_daily.csv", sep=';')

#winter = matchesAndTeamsMerge(matches_winter, teams_winter)
#spring = matchesAndTeamsMerge(matches_spring, teams_spring)
#summer = matchesAndTeamsMerge(matches_summer, teams_summer)
#msi = matchesAndTeamsMerge(matches_msi, teams_spring) # end of spring split
#ewc = matchesAndTeamsMerge(matches_ewc, teams_spring) # start of summer split

winter_daily = merge_match_with_team_stats(matches_winter, teams_winter_daily)
# potrebuju jeste se naucit spojovat podle tymu, datumu (co nejblizsi pred tim dnem) a podle turnaje
# musis pridat jeste do matches sloupec turnaje a udelej to jenom s hlavnimi peti ligy viz github

#spring = mergeSplits([spring, msi])
#summer = mergeSplits([summer, ewc])
#winter_spring = mergeSplits([winter, spring, msi])
#spring_summer = mergeSplits([spring, summer, msi, ewc])
#winter_spring_summer = mergeSplits([winter, spring, summer, msi, ewc])

#spring.to_csv("../../data/merged/spring.csv", sep=';', index=False)
#summer.to_csv("../../data/merged/summer.csv", sep=';', index=False)
#winter_spring.to_csv("../../data/merged/winter_spring.csv", sep=';', index=False)
#spring_summer.to_csv("../../data/merged/spring_summer.csv", sep=';', index=False)
#winter_spring_summer.to_csv("../../data/merged/winter_spring_summer.csv", sep=';', index=False)
winter_daily.to_csv("../../data/merged/winter_daily.csv", sep=';', index=False)