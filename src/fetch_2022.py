import os
import requests
import pandas as pd

def fetch_2022_worldcup():
    # .env를 쓰거나 직접 터미널에 export로 넣은 키를 가져옵니다.
    api_key = os.getenv("FOOTBALL_DATA_API_KEY") 
    
    # URL 끝에 ?season=2022 를 붙여서 카타르 월드컵만 타겟팅합니다.
    url = "https://api.football-data.org/v4/competitions/WC/matches?season=2022"
    headers = {"X-Auth-Token": api_key}
    
    print("⚽ 2022 카타르 월드컵 데이터 수집 시작...")
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
                    "HomeScore": m['score']['fullTime'].get('home', 0),
                    "AwayScore": m['score']['fullTime'].get('away', 0),
                    # 승무패(Label) 만들기: 홈팀 기준 (W: 승, D: 무, L: 패)
                    "HomeResult": m['score']['winner'] 
                })
                
        df = pd.DataFrame(match_data)
        
        # 'WINNER' 값을 우리가 쓰기 편하게 HOME_TEAM, AWAY_TEAM, DRAW 로 변환
        def get_result(row):
            if row['HomeResult'] == 'HOME_TEAM': return 'W'
            elif row['HomeResult'] == 'AWAY_TEAM': return 'L'
            else: return 'D'
            
        df['Result'] = df.apply(get_result, axis=1)
        df.drop(columns=['HomeResult'], inplace=True)
        
        # CSV 파일로 저장 (머신러닝 학습용 교재)
        df.to_csv("worldcup_2022_matches.csv", index=False)
        print(f"✅ 수집 완료! 총 {len(df)}경기 데이터가 worldcup_2022_matches.csv로 저장되었습니다.")
        
    else:
        print(f"❌ API 호출 에러: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    fetch_2022_worldcup()