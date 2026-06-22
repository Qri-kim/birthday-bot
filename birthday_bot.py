import os
import csv
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 환경변수에서 토큰 가져오기
token = os.environ["SLACK_BOT_TOKEN"]
channel_id = os.environ["SLACK_CHANNEL_ID"]
client = WebClient(token=token)

# 오늘 날짜
today = datetime.now()
today_month = today.month
today_day = today.day

# 생일자 찾기
birthdays_today = []
with open("birthdays.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            # 데이터 양쪽의 공백을 제거(.strip())한 뒤 숫자로 변환합니다.
            # 만약 빈 칸('')이거나 숫자가 아니면 자동으로 에러를 감지하고 다음 행으로 넘어갑니다.
            row_month = int(str(row["생일_월"]).strip())
            row_day = int(str(row["생일_일"]).strip())
            
            if (
                row_month == today_month
                and row_day == today_day
                and row["재직여부"] == "Y"
            ):
                birthdays_today.append(row)
                
        except (ValueError, TypeError, KeyError):
            # 유령 행(빈 줄), 공백 데이터, 혹은 칸 이름이 맞지 않는 경우 에러를 내지 않고 패스합니다.
            continue

# 슬랙 메시지 전송
if birthdays_today:
    message = "🎂 *오늘의 발렌 생일자를 소개합니다!* <!channel>\n\n"
    for person in birthdays_today:
        message += f"🎉 *{person['부서']}* {person['이름']} 님, 생일을 축하합니다!\n"
    message += "\n모두 함께 축하해 주세요 🥳"

    try:
        client.chat_postMessage(channel=channel_id, text=message)
        print("✅ 슬랙 메시지 전송 완료")
    except SlackApiError as e:
        print(f"❌ 오류 발생: {e.response['error']}")
else:
    print("오늘 생일자 없음")
