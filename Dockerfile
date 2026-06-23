# 1. 파이썬 베이스 이미지
FROM python:3.12-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 라이브러리 설치
RUN pip install --no-cache-dir \
    requests \
    pandas \
    google-cloud-bigquery \
    python-dotenv \
    pyarrow \
    pandas-gbq

# 4. 소스 코드 전부 복사 (src 폴더만 복사하지 말고 전체를 복사해야 함)
COPY . .

# 5. [핵심] 파이썬이 모듈을 찾을 수 있게 경로 지정
ENV PYTHONPATH=/app/src

# 6. 파이썬 버퍼링을 끄고 실행 (로그가 바로 나오게 함)
CMD ["python", "-u", "src/loader.py"]