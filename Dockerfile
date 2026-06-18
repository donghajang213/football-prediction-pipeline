FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir requests pandas google-cloud-bigquery python-dotenv pyarrow pandas-gbq
COPY . .
ENV PYTHONPATH=/app/src
CMD ["python", "-u", "src/loader.py"]
