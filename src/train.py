import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def train_model():
    # 1. 완벽하게 정제된 데이터 불러오기
    data_path = os.path.join(os.getcwd(), "data", "train_data.csv")
    df = pd.read_csv(data_path)

    # 2. X(문제)와 y(정답) 분리
    feature_cols = [
        'xg_diff', 'possession_diff', 'passes_pct_diff', 
        'shots_on_target_pct_diff', 'gk_save_pct_diff'
    ]
    X = df[feature_cols]
    y = df['target']

    # 3. 학습용 / 테스트용 데이터 분리 (80%는 학습에, 20%는 시험 보는데 사용)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("🤖 인공지능 모델 학습을 시작합니다...")
    # 4. 랜덤 포레스트 모델 생성 및 학습
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # 5. 분리해둔 20%의 테스트 데이터로 예측 시험 보기
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n✅ 모델 학습 완료! 예측 정확도(Accuracy): {acc * 100:.2f}%")

    # 6. Feature Importance (AI가 승패를 가를 때 가장 중요하게 본 요소)
    print("\n💡 AI가 승패 예측 시 가장 중요하게 본 데이터 비율:")
    importances = model.feature_importances_
    for name, imp in sorted(zip(feature_cols, importances), key=lambda x: x[1], reverse=True):
        print(f" - {name}: {imp * 100:.1f}%")

    # 7. 훈련된 똑똑한 모델을 파일로 저장 (나중에 2026년 예측에 재사용)
    model_dir = os.path.join(os.getcwd(), "models")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    model_path = os.path.join(model_dir, "wc_predictor.pkl")
    joblib.dump(model, model_path)
    print(f"\n💾 학습된 AI 모델이 '{model_path}'에 저장되었습니다.")

if __name__ == "__main__":
    train_model()