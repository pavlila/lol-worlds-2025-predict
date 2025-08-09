# lol-worlds-2025-predict

This project aims to predict the outcome of the League of Legends World Championship based on match data from the entire 2025 season, sourced from [gol.gg](https://gol.gg/). Team statistics, sourced from [oracleselixir.com](https://oracleselixir.com/), are updated daily and reflect performance only within the current tournament — from the team’s first match to their last match in that tournament. The prediction logic dynamically uses these team stats limited to each tournament’s timeframe.

## Team-Match Linking Logic:

picture

## Used tournaments

- winter

        lpl - LPL 2025 Split 1 | LPL 2025 Split 1 Playoffs

        lec - LEC Winter 2025 | LEC 2025 Winter Playoffs

        lck - LCK Cup 2025

        lta - LTA North 2025 Split 1 | LTA South 2025 Split 1 | LTA 2025 Split 1 Playoffs

        lcp - LCP 2025 Season Kickoff | LCP 2025 Season Kickoff Qualifying Series

- spring

        lpl - LPL 2025 Split 2 Placements | LPL 2025 Split 2 | LPL 2025 Split 2 Playoffs
    
        lec - LEC 2025 Spring Season | LEC 2025 Spring Playoffs

        lck - LCK 2025 Rounds 1-2 | LCK 2025 Road to MSI

        lta - LTA North 2025 Split 2 | LTA North 2025 Split 2 Playoffs | LTA South 2025 Split 2 | LTA South 2025 Split 2 Playoffs

        lcp - LCP 2025 Mid Season | LCP 2025 Mid Season Qualifying Series

- summer

- interleague

        2025 Mid-Season Invitational

        Esports World Cup 2025

## how to use it (Linux)

- Clone the repository

      git clone https://github.com/pavlila/lol-worlds-2025-predict.git
      cd lol-worlds-2025-predict
        
- Create and activate a virtual environment
  
      python3 -m venv venv
      source venv/bin/activate

- Install dependencies

      pip install -r requirements.txt
  
- Prepare the input data
  
  - Place your data file at data/raw/new_match.csv
    
  - Make sure the file contains the following columns: tournament | teamA | number_of_matches | teamB | date
 
- Process the new data

- Run the prediction script
  
      python3 prediction.py

        
