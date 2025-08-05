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

matches_winter = pd.read_csv("../../data/cleaned/matches_winter.csv", sep=';')
matches_spring = pd.read_csv("../../data/cleaned/matches_spring.csv", sep=';')
matches_summer = pd.read_csv("../../data/cleaned/matches_summer.csv", sep=';')

teams_winter = pd.read_csv("../../data/cleaned/teams_winter.csv", sep=';')
teams_spring = pd.read_csv("../../data/cleaned/teams_spring.csv", sep=';')
teams_summer = pd.read_csv("../../data/cleaned/teams_summer.csv", sep=';')

winter = matchesAndTeamsMerge(matches_winter, teams_winter)
spring = matchesAndTeamsMerge(matches_spring, teams_spring)
summer = matchesAndTeamsMerge(matches_summer, teams_summer)

winter_spring = mergeSplits([winter, spring])
spring_summer = mergeSplits([spring, summer])
winter_spring_summer = mergeSplits([winter, spring, summer])

spring.to_csv("../../data/merged/spring.csv", sep=';', index=False)
summer.to_csv("../../data/merged/summer.csv", sep=';', index=False)
winter_spring.to_csv("../../data/merged/winter_spring.csv", sep=';', index=False)
spring_summer.to_csv("../../data/merged/spring_summer.csv", sep=';', index=False)
winter_spring_summer.to_csv("../../data/merged/winter_spring_summer.csv", sep=';', index=False)