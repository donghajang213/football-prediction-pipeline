# 🏆 2026 World Cup Real-time Power Ranking Pipeline

## 📌 프로젝트 소개
본 프로젝트는 2026 북중미 월드컵 경기 데이터를 실시간으로 수집, 변환하여 클라우드 데이터 웨어하우스에 적재하고, 이를 기반으로 국가별 파워 지수(Power Index)를 계산해 대시보드로 시각화하는 **End-to-End 데이터 파이프라인**입니다.

모든 과정은 Kubernetes 환경에서 컨테이너 기반으로 스케줄링되며, 파이프라인 실행 결과는 메신저(Discord) 웹훅을 통해 실시간으로 모니터링됩니다.

## 🏗 아키텍처 및 기술 스택
- **Language:** Python 3.10+ (Pandas, Requests)
- **Infrastructure & Container:** Docker, Google Kubernetes Engine (GKE)
- **Data Warehouse:** Google BigQuery
- **Data Visualization:** Looker Studio
- **Monitoring & Alert:** Discord Webhook API
- **Data Source:** Football-Data API (v4)

## 💡 핵심 구현 사항
1. **데이터 수집 및 변환 (ETL / ELT):** 
   - `collector.py`: API 연동을 통해 종료된(FINISHED) 매치 데이터 추출.
   - `transformer.py`: 전반전/풀타임 득점 데이터를 결합하여 국가별 '파워 지수(평균 득점력)' 등 파생 변수 생성.
2. **인프라 컨테이너화 및 스케줄링 자동화:**
   - 파이썬 환경과 의존성을 `Dockerfile`로 격리하여 배포.
   - Kubernetes `CronJob`을 활용하여 매일 자정(KST) 최신 데이터 자동 갱신.
3. **보안 및 자격 증명 관리 (Security):**
   - API Key 및 Webhook URL 등 민감한 정보는 소스코드에 하드코딩하지 않고, Kubernetes `Secret` 리소스로 분리하여 컨테이너 환경 변수(`env`)로 안전하게 주입.
   - `.gitignore`를 통한 로컬 `.env` 파일 추적 영구 차단.
4. **실시간 모니터링 파이프라인:**
   - BigQuery 적재 성공 및 에러 발생 시, Discord Bot을 통해 파이프라인 상태 알림 자동 전송.

## 📊 시각화 대시보드 (Looker Studio)
- 수집된 Data Mart를 기반으로 실시간 랭킹 변동 및 득점 통계 시각화 완료.
- [(https://datastudio.google.com/reporting/a800d198-88de-4704-8b72-507807603408)]
