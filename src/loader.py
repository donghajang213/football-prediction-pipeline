import sys
import os
import requests
from collector import fetch_data
from transformer import calculate_power_index
from google.cloud import bigquery

def send_discord_message(msg):
    """디스코드로 알림을 보냅니다."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        payload = {"content": msg}
        requests.post(webhook_url, json=payload)

def main():
    print("🚀 파이프라인 가동", flush=True)

    try:
        # 1. 수집
        raw_df = fetch_data()
        if raw_df is None or raw_df.empty:
            send_discord_message("⚠️ [2026 월드컵 파이프라인] 오늘 수집된 새로운 경기 데이터가 없습니다.")
            sys.exit(0)
            
        # 2. 변환
        processed_df = calculate_power_index(raw_df)
        match_count = len(raw_df)
        top_team = processed_df.iloc[0]['Team']
        top_power = processed_df.iloc[0]['PowerIndex']
        
        # 3. 적재
        client = bigquery.Client()
        table_id = "football_prediction.wc_power_ranking"
        job = client.load_table_from_dataframe(
            processed_df, table_id, 
            job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        )
        job.result()
        
        # 4. 성공 알림 송신
        success_msg = f"✅ **[2026 월드컵 파이프라인 성공]**\n- 현재까지 총 {match_count}개 경기 적재 완료\n- 현재 파워 지수 1위: **{top_team}** ({top_power}점)"
        send_discord_message(success_msg)
        print("🎉 BigQuery 적재 및 알림 송신 성공!", flush=True)

    except Exception as e:
        # 에러 발생 시 알림 송신
        error_msg = f"🚨 **[2026 월드컵 파이프라인 에러 발생]**\n- 에러 내용: {str(e)}"
        send_discord_message(error_msg)
        print(f"에러 발생: {e}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()