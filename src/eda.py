import pandas as pd
import os

def analyze_data():
    # 데이터 경로 세팅
    data_dir = os.path.join(os.getcwd(), "data")
    team_csv = os.path.join(data_dir, "team_data.csv")
    group_csv = os.path.join(data_dir, "group_stats.csv")

    # 데이터 불러오기
    df_team = pd.read_csv(team_csv)
    df_group = pd.read_csv(group_csv)

    print("===  [team_data.csv] 컬럼 목록 ===")
    print(list(df_team.columns))
    print(f"데이터 개수: {df_team.shape[0]}행 x {df_team.shape[1]}열")
    
    print("\n===  [group_stats.csv] 컬럼 목록 ===")
    print(list(df_group.columns))
    print(f"데이터 개수: {df_group.shape[0]}행 x {df_group.shape[1]}열")

    print("\n team_data.csv 데이터 미리보기 (가로로 길게 출력):")
    # 컬럼이 많아도 잘리지 않게 설정
    pd.set_option('display.max_columns', None) 
    print(df_team.head(2))

if __name__ == "__main__":
    analyze_data()