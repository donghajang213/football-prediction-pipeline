import pandas as pd
import os
import joblib
import sys

def predict_match(home_team, away_team):
    # 1. 훈련된 AI 뇌(Pickle 모델) 불러오기
    model_path = os.path.join(os.getcwd(), "models", "wc_predictor.pkl")
    if not os.path.exists(model_path):
        print("🚨 모델 파일이 없습니다! 먼저 train.py를 실행하여 모델을 구워주세요.")
        sys.exit(1)
        
    model = joblib.load(model_path)

    # 2. 팀 스탯 데이터(무기) 불러오기
    stats_path = os.path.join(os.getcwd(), "data", "team_data.csv")
    stats = pd.read_csv(stats_path)
    
    # 국가명 예외 처리 보정
    name_map = {'United States': 'USA', 'Korea Republic': 'South Korea', 'IR Iran': 'Iran'}
    stats['team'] = stats['team'].replace(name_map)

    # 3. 입력된 두 팀의 데이터 찾기
    try:
        home_stats = stats[stats['team'] == home_team].iloc[0]
        away_stats = stats[stats['team'] == away_team].iloc[0]
    except IndexError:
        print(f"🚨 에러: '{home_team}' 또는 '{away_team}'의 데이터를 찾을 수 없습니다. (예: South Korea, Germany)")
        sys.exit(1)

    # 4. AI에게 먹일 피처(능력치 차이) 계산
    features = pd.DataFrame([{
        'xg_diff': home_stats['xg'] - away_stats['xg'],
        'possession_diff': home_stats['possession'] - away_stats['possession'],
        'passes_pct_diff': home_stats['passes_pct'] - away_stats['passes_pct'],
        'shots_on_target_pct_diff': home_stats['shots_on_target_pct'] - away_stats['shots_on_target_pct'],
        'gk_save_pct_diff': home_stats['gk_save_pct'] - away_stats['gk_save_pct']
    }])

    # 5. 승패 및 확률 예측
    pred = model.predict(features)[0]
    probs = model.predict_proba(features)[0]

    # 결과 매핑 (2: 승, 1: 무, 0: 패)
    result_map = {2: f"{home_team} 승리", 1: "무승부", 0: f"{away_team} 승리"}

    print(f"\n⚽ [매치 예측 결과] {home_team} vs {away_team}")
    print(f"👉 AI 최종 판정: **{result_map[pred]}**")
    print(f"📊 세부 승률: {home_team} 승({probs[2]*100:.1f}%) | 무승부({probs[1]*100:.1f}%) | {away_team} 승({probs[0]*100:.1f}%)")

if __name__ == "__main__":
    # 터미널에서 국가명을 입력받음 (기본값: 대한민국 vs 포르투갈)
    team_a = "South Korea"
    team_b = "Portugal"

    if len(sys.argv) == 3:
        team_a = sys.argv[1]
        team_b = sys.argv[2]

    predict_match(team_a, team_b)