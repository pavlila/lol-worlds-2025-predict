import pandas as pd

def concatDfs(splits):
    return pd.concat(splits, ignore_index=True)

def getStats(team, tournament, date, teamsStats):
    teamDataPast = teamsStats[(teamsStats['Team'] == team) & (teamsStats['date'] < date)]

    assert not teamDataPast.empty, f"\n!!! No data available for team {team} (last match) !!!"

    teamLastData = teamDataPast.sort_values('date', ascending=False).iloc[0]

    if teamLastData.GP > 5:
        teamLastData = teamLastData.drop(columns=['date','Team','tournament'])
        return teamLastData
    else:
        teamDataFromLastTournament = teamsStats[(teamsStats['Team'] == team) & (teamsStats['date'] < date) & (teamsStats['tournament'] != tournament)]

        assert not teamDataPast.empty, f"\n!!! No data available for team {team} (last tournament) !!!"
        
        teamLastDataFromLastTournament = teamDataFromLastTournament.sort_values('date', ascending=False).iloc[0]

        gp_last = min(teamLastDataFromLastTournament.GP, 5)
        gp_curr = teamLastData.GP
        gp = gp_last + gp_curr

        combined_data = pd.Series(dtype=float)
        combined_data['GP'] = gp

        numeric_cols = [
            'AGT','KD','CKPM','GPR','GSPD','EGR','MLR','GD15',
            'FB%','FT%','F3T%','PPG','HLD%','GRB%','FD%','DRG%','ELD%',
            'FBN%','BN%','LNE%','JNG%','WPM','CWPM','WCPM','winrate%'
        ]

        for col in numeric_cols:
            combined_data[col] = (teamLastData[col] * gp_curr + teamLastDataFromLastTournament[col] * gp_last) / (gp_curr + gp_last)

        return combined_data

def mergeMatchesAndTeamsData(matches, teams):
    merged_rows = []
    for _, row in matches.iterrows():
        teamA = row['teamA']
        teamB = row['teamB']
        date = row['date']
        tournament = row['tournament']

        statsA = getStats(teamA, tournament, date, teams)
        statsB = getStats(teamB, tournament, date, teams)

        if statsA.empty or statsB.empty:
            continue

        statsA = statsA[[col for col in statsA.index if col not in ['Team','tournament','date']]]
        statsB = statsB[[col for col in statsB.index if col not in ['Team','tournament','date']]]

        statsA = statsA.add_suffix("_A")
        statsB = statsB.add_suffix("_B")

        combined_data = pd.concat([statsA, statsB])

        combined_data['teamA'] = teamA
        combined_data['teamB'] = teamB
        combined_data['date'] = date
        combined_data['tournament'] = tournament

        merged_rows.append(combined_data)

    return pd.DataFrame(merged_rows).reset_index(drop=True)

new_match = pd.read_csv("../../data/cleaned/new_match.csv", sep=',')

dfs_teams = ['winter','spring','summer','msi','ewc', 'fst']
teams_list = [pd.read_csv(f"../../data/cleaned/teams_{team}.csv", sep=',') for team in dfs_teams]
teams = concatDfs(teams_list)

new_data = mergeMatchesAndTeamsData(new_match, teams)

new_data.to_csv("../../data/merged/new_data.csv", sep=',', index=False)