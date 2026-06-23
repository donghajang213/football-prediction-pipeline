import pandas as pd

def calculate_power_index(df):
    home = df[['HomeTeam', 'HomeScore_FullTime', 'HomeScore_HalfTime']].rename(
        columns={'HomeTeam': 'Team', 'HomeScore_FullTime': 'Goals', 'HomeScore_HalfTime': 'HalfTimeGoals'}
    )
    away = df[['AwayTeam', 'AwayScore_FullTime', 'AwayScore_HalfTime']].rename(
        columns={'AwayTeam': 'Team', 'AwayScore_FullTime': 'Goals', 'AwayScore_HalfTime': 'HalfTimeGoals'}
    )
    
    all_goals = pd.concat([home, away])
    
    power_df = all_goals.groupby('Team').agg(
        MatchCount=('Goals', 'count'),
        TotalGoals=('Goals', 'sum'),
        TotalHalfTimeGoals=('HalfTimeGoals', 'sum'),
        PowerIndex=('Goals', 'mean')
    ).reset_index()
    
    power_df = power_df.sort_values(by='PowerIndex', ascending=False).round(2)
    return power_df
