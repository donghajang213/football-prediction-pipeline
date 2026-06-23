import sys
import os
from collector import fetch_data
from transformer import calculate_power_index
from google.cloud import bigquery

def main():
    print("🚀 파이프라인 가동", flush=True)
    raw_df = fetch_data()
    if raw_df is None or raw_df.empty:
        sys.exit(0)
    processed_df = calculate_power_index(raw_df)
    client = bigquery.Client()
    table_id = "football_prediction.wc_power_ranking"
    job = client.load_table_from_dataframe(
        processed_df, table_id, 
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    )
    job.result()
    print("🎉 BigQuery 적재 성공!", flush=True)

if __name__ == "__main__":
    main()