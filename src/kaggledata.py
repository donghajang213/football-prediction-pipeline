import kagglehub
import os
import shutil
import pandas as pd

def download_and_move_dataset():
    # 1. 현재 내 프로젝트의 루트 경로 가져오기 (E:\football-prediction-pipeline)
    project_root = os.getcwd()
    target_data_dir = os.path.join(project_root, "data")
    
    # 2. 프로젝트 폴더 내에 'data' 폴더가 없다면 자동으로 생성
    if not os.path.exists(target_data_dir):
        os.makedirs(target_data_dir)
        print(f"📂 새 폴더 생성 완료: {target_data_dir}")

    # 3. 캐글 서버에서 데이터셋 다운로드 (임시 캐시 경로로 다운됨)
    print("⚽ 캐글에서 2022 월드컵 데이터셋 다운로드 중...")
    cache_path = kagglehub.dataset_download("swaptr/fifa-world-cup-2022-statistics")
    
    # 4. 캐시 폴더 안에 있는 모든 파일 목록 확인
    cache_files = os.listdir(cache_path)
    print(f"📦 다운로드된 원본 파일 목록: {cache_files}")

    # 5. 캐시 폴더의 파일들을 내 프로젝트의 data 폴더로 복사
    print("🚚 파일들을 프로젝트 내부 'data' 폴더로 복사하는 중...")
    for file_name in cache_files:
        src_file = os.path.join(cache_path, file_name)
        dst_file = os.path.join(target_data_dir, file_name)
        
        # 파일 복사 수행 (이미 있으면 덮어씀)
        shutil.copy(src_file, dst_file)
    
    print(f"✅ 모든 파일이 {target_data_dir} 경로로 무사히 이전되었습니다.")

    # 6. 이전된 데이터 중 하나를 로드해서 검증
    sample_csv = os.path.join(target_data_dir, "team_data.csv")
    if os.path.exists(sample_csv):
        df = pd.read_csv(sample_csv)
        print("\n📊 복사된 team_data.csv 데이터 미리보기:")
        print(df.head(3))

if __name__ == "__main__":
    download_and_move_dataset()