import os
import sys
import requests
import pandas as pd
import joblib
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

def send_discord_message(msg):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        requests.post(webhook_url, json={"content": msg})
    else:
        print("\n[디스코드 미리보기]\n", msg)

def predict_tomorrow_matches():
    print("🌐 1. 실시간 2026 월드컵 대진표 가져오기...")
    
    api_key = os.getenv("FOOTBALL_DATA_API_KEY")
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": api_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"🚨 API 호출 실패: {response.status_code}")
        return

    matches = response.json().get('matches', [])
    upcoming = [m for m in matches if m['status'] in ['TIMED', 'SCHEDULED']]
    
    # 시간 경고 해결: timezone-aware 방식 적용
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).strftime('%Y-%m-%d')
    tomorrow_matches = [m for m in upcoming if m['utcDate'].startswith(tomorrow)]

    if not tomorrow_matches:
        send_discord_message(f"⚽ **[AI 예측 봇]** 내일({tomorrow}) 예정된 2026 월드컵 경기가 없습니다.")
        return

    print("🧠 2. AI 모델 및 데이터 로드 중...")
    model = joblib.load(os.path.join(os.getcwd(), "models", "wc_predictor.pkl"))
    stats = pd.read_csv(os.path.join(os.getcwd(), "data", "team_data.csv"))
    name_map = {'United States': 'USA', 'Korea Republic': 'South Korea', 'IR Iran': 'Iran'}
    stats['team'] = stats['team'].replace(name_map)

    # 🔥 결측치(Cold Start) 대비용 평균 스탯 계산
    mean_stats = stats.mean(numeric_only=True)

    print("🔮 3. 100% 승률 예측 및 결측치 보정 진행...")
    discord_report = f"🤖 **[AI 예측 리포트] 2026 월드컵 내일({tomorrow})의 경기**\n\n"

    for m in tomorrow_matches:
        home = m['homeTeam']['name']
        away = m['awayTeam']['name']
        
        # 💡 콜드 스타트 문제 해결 로직 (Mean Imputation with Penalty)
        home_is_imputed, away_is_imputed = False, False
        
        if home in stats['team'].values:
            home_stats = stats[stats['team'] == home].iloc[0]
        else:
            home_stats = mean_stats * 0.9 # 신규 진출국은 평균의 90% 전력으로 가정
            home_is_imputed = True
            
        if away in stats['team'].values:
            away_stats = stats[stats['team'] == away].iloc[0]
        else:
            away_stats = mean_stats * 0.9
            away_is_imputed = True

        features = pd.DataFrame([{
            'xg_diff': home_stats['xg'] - away_stats['xg'],
            'possession_diff': home_stats['possession'] - away_stats['possession'],
            'passes_pct_diff': home_stats['passes_pct'] - away_stats['passes_pct'],
            'shots_on_target_pct_diff': home_stats['shots_on_target_pct'] - away_stats['shots_on_target_pct'],
            'gk_save_pct_diff': home_stats['gk_save_pct'] - away_stats['gk_save_pct']
        }])

        pred = model.predict(features)[0]
        probs = model.predict_proba(features)[0]
        
        result_map = {2: f"{home} 승리", 1: "무승부", 0: f"{away} 승리"}
        
        warning_msg = ""
        if home_is_imputed or away_is_imputed:
            warning_msg = " *(⚠️ 과거 데이터 부족으로 보정된 전력 기반 예측)*"

        discord_report += f"⚔️ **{home} vs {away}**\n"
        discord_report += f"👉 AI 예측: **{result_map[pred]}** {warning_msg}\n"
        discord_report += f"📊 세부 승률: {home} {probs[2]*100:.1f}% | 무 {probs[1]*100:.1f}% | {away} {probs[0]*100:.1f}%\n\n"

    send_discord_message(discord_report)
    print("✅ 예측 완료 및 전송 성공!")

if __name__ == "__main__":
    predict_tomorrow_matches()