import pandas as pd
import os

def create_train_data():
    print(" 1. 깃허브 오픈소스에서 2022 카타르 월드컵 경기 결과 가져오는 중...")
    url = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
    matches = pd.read_csv(url)
    
    # 2022년 카타르 월드컵 데이터만 필터링
    wc_2022 = matches[(matches['tournament'] == 'FIFA World Cup') & 
                      (matches['date'].str.startswith('2022'))].copy()
    print(f" 카타르 월드컵 총 {len(wc_2022)}경기 정답지 확보!")

    print("\n 2. 캐글 스탯 데이터(무기) 불러오는 중...")
    stats_path = os.path.join(os.getcwd(), "data", "team_data.csv")
    stats = pd.read_csv(stats_path)
    
    # AI에게 먹일 핵심 5대 피처만 추출
    features = ['team', 'xg', 'possession', 'passes_pct', 'shots_on_target_pct', 'gk_save_pct']
    stats = stats[features]

    # [팁] 데이터 소스 간 국가 이름 차이 보정 (예: Korea Republic -> South Korea)
    name_map = {'United States': 'USA', 'Korea Republic': 'South Korea', 'IR Iran': 'Iran'}
    stats['team'] = stats['team'].replace(name_map)

    print("\n🔗 3. 데이터 결합 및 피처 엔지니어링 (스탯 차이 계산) 진행 중...")
    # 홈팀 스탯 붙이기
    train_df = pd.merge(wc_2022, stats, left_on='home_team', right_on='team', how='inner')
    train_df = train_df.rename(columns={'xg': 'home_xg', 'possession': 'home_possession', 
                                        'passes_pct': 'home_passes_pct', 
                                        'shots_on_target_pct': 'home_shots_on_target_pct', 
                                        'gk_save_pct': 'home_gk_save_pct'})

    # 원정팀 스탯 붙이기
    train_df = pd.merge(train_df, stats, left_on='away_team', right_on='team', how='inner')
    train_df = train_df.rename(columns={'xg': 'away_xg', 'possession': 'away_possession', 
                                        'passes_pct': 'away_passes_pct', 
                                        'shots_on_target_pct': 'away_shots_on_target_pct', 
                                        'gk_save_pct': 'away_gk_save_pct'})

    #  핵심: 홈팀과 원정팀의 능력치 차이(Diff) 계산
    train_df['xg_diff'] = train_df['home_xg'] - train_df['away_xg']
    train_df['possession_diff'] = train_df['home_possession'] - train_df['away_possession']
    train_df['passes_pct_diff'] = train_df['home_passes_pct'] - train_df['away_passes_pct']
    train_df['shots_on_target_pct_diff'] = train_df['home_shots_on_target_pct'] - train_df['away_shots_on_target_pct']
    train_df['gk_save_pct_diff'] = train_df['home_gk_save_pct'] - train_df['away_gk_save_pct']

    #  정답(Target) 만들기: 홈팀 기준으로 승(2), 무(1), 패(0)
    def get_result(row):
        if row['home_score'] > row['away_score']: return 2
        elif row['home_score'] == row['away_score']: return 1
        else: return 0
    train_df['target'] = train_df.apply(get_result, axis=1)

    # 최종적으로 AI가 학습할 컬럼만 깔끔하게 정리
    final_features = [
        'home_team', 'away_team', 
        'xg_diff', 'possession_diff', 'passes_pct_diff', 
        'shots_on_target_pct_diff', 'gk_save_pct_diff', 
        'target'
    ]
    final_df = train_df[final_features]

    # 결과물 저장
    out_path = os.path.join(os.getcwd(), "data", "train_data.csv")
    final_df.to_csv(out_path, index=False)
    
    print("\n 완벽한 학습용 데이터셋(train_data.csv) 생성 완료!")
    print(final_df.head(3).to_string())

if __name__ == "__main__":
    create_train_data()