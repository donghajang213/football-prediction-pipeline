# 🏆 2026 World Cup Data & ML Prediction Pipeline

## 📌 프로젝트 소개
본 프로젝트는 2026 북중미 월드컵 경기 데이터를 실시간으로 수집하여 파워 랭킹을 시각화하고, 머신러닝(Random Forest)을 통해 내일 열릴 경기의 승패를 예측하는 **End-to-End 데이터 및 MLOps 파이프라인**입니다.

모든 수집 및 예측 과정은 스케줄링되어 자동으로 실행되며, 파이프라인 실행 결과 및 인공지능의 내일 경기 예측 리포트는 메신저(Discord) 웹훅을 통해 실시간으로 모니터링됩니다.

## 🏗 아키텍처 및 기술 스택
- **Language:** Python 3.10+ (Pandas, Scikit-Learn, Joblib)
- **Infrastructure & Container:** Docker, Google Kubernetes Engine (GKE), GCP Cloud Shell
- **Data Warehouse:** Google BigQuery
- **Data Visualization:** Looker Studio
- **Monitoring & Alert:** Discord Webhook API
- **Data Source:** Football-Data API (v4), Kaggle Open Data (2022 World Cup Stats)

## 💡 핵심 구현 사항

### 1. 데이터 파이프라인 및 시각화 (ETL / Data Mart)
- `collector.py` & `transformer.py`: API 
연동을 통해 매치 데이터를 추출하고 전반/풀타임 득점 데이터를 결합하여 국가별 '파워 지수' 파생 변수 생성.
- K8s `CronJob`을 활용하여 매일 자정(KST) BigQuery에 최신 데이터 자동 갱신.
- **[대시보드]** 수집된 데이터를 기반으로 실시간 랭킹 변동 및 득점 통계 시각화 완료.
  - [🔗 Looker Studio 대시보드 바로가기](https://datastudio.google.com/reporting/a800d198-88de-4704-8b72-507807603408)
 
  - <img width="1908" height="801" alt="축구 데이터" src="https://github.com/user-attachments/assets/06e09ced-2900-400a-88d3-e7a41fc9c11c" />

### 2. 머신러닝 기반 경기 예측 (MLOps)
- 과거 카타르 월드컵 데이터를 바탕으로 `기대득점(xG)`, `점유율`, `패스 성공률`, `유효슈팅`, `선방률` 등 5가지 핵심 스탯의 차이값(Diff)을 피처로 활용하여 ML 모델 학습 및 `.pkl` 직렬화.
- 스케줄러를 통해 내일 열릴 경기의 대진표를 가져오고, AI가 승률(%)을 계산하여 Discord Bot으로 자동 리포팅.

- <img width="677" height="627" alt="2026승부예측" src="https://github.com/user-attachments/assets/f6d3910e-d0ba-4f71-af56-fc24e30d9b38" />


## 🔥 트러블슈팅 및 문제 해결

**1. 신규 진출국 데이터 결측치(Cold Start) 극복**
- **문제:** 2026년 신규 진출국(예: 스코틀랜드, 콜롬비아 등)은 2022년 학습 데이터에 존재하지 않아 모델 추론 시 에러가 발생.
- **해결:** `Mean Imputation with Penalty` 기법 도입. 데이터가 없는 국가는 기존 진출국 평균 스탯의 **90% 전력(10% 페널티)**을 가지도록 수리적 가중치를 부여하여 100% 승률 예측 방어 성공.

**2. 인프라 보안 및 KST 타임존 동기화**
- **보안:** API Key, Webhook URL 등 민감 정보는 `.env` 및 K8s `Secret` 리소스로 분리 격리하여 보안성 강화. (`.gitignore` 적용)
- **타임존:** K8s CronJob 기본 시간이 UTC로 설정되어 배치 작업이 어긋나는 현상을 `CRON_TZ=Asia/Seoul` 명시를 통해 해결.

## 📂 디렉토리 구조
```text
football-prediction-pipeline/
├── src/
│   ├── collector.py        # API 통신 및 Raw 데이터 추출 (Season 1)
│   ├── transformer.py      # 데이터 가공 및 파생 변수 생성 (Season 1)
│   ├── kaggledata.py       # Kaggle 과거 스탯 데이터 수집 (Season 2)
│   ├── preprocess.py       # ML 피처 전처리 및 Diff 계산 (Season 2)
│   ├── train.py            # 모델 학습 및 .pkl 생성 (Season 2)
│   └── predict_tomorrow.py # 실시간 AI 승률 예측 및 알림 (Season 2)
├── k8s/
│   ├── cronjob.yaml        # K8s 스케줄링 배치 설정
│   └── secret.yaml         # (git ignored) 환경변수 시크릿
├── data/                   # (git ignored) 머신러닝용 csv 데이터셋
├── models/                 # (git ignored) 학습된 인공지능 뇌 (.pkl)
├── Dockerfile              # 파이프라인 컨테이너 빌드 명세서
├── requirements.txt
└── README.md
