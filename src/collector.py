import os
import requests
import pandas as pd
import sys

def fetch_data():
    api_key = os.getenv("FOOTBALL_DATA_API_KEY")
    if not api_key:
        print("에러: FOOTBALL_DATA_API_KEY가 설정되지 않았습니다.", flush=True)
        sys.exit(1)
    
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": api_key}
    
    print("⚽ 상세 데이터 수집 시작...", flush=True)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        matches = response.json().get('matches', [])
        match_data = []
        for m in matches:
            if m['status'] == 'FINISHED':
                match_data.append({
                    "Date": m['utcDate'],
                    "Stage": m.get('stage', 'UNKNOWN'),
                    "HomeTeam": m['homeTeam']['name'],
                    "AwayTeam": m['awayTeam']['name'],
                    "HomeScore_FullTime": m['score']['fullTime'].get('home', 0),
                    "AwayScore_FullTime": m['score']['fullTime'].get('away', 0),
                    "HomeScore_HalfTime": m['score']['halfTime'].get('home', 0),
                    "AwayScore_HalfTime": m['score']['halfTime'].get('away', 0)
                })
        
        df = pd.DataFrame(match_data)
        print(f"✅ 수집 완료: {len(df)}개 경기 (수집된 컬럼: {len(df.columns)}개)", flush=True)
        return df
    else:
        print(f"에러: {response.status_code}", flush=True)
        return None
