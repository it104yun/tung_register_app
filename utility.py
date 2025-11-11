from datetime import datetime, timezone, timedelta

def this_time():
    # 建立一個 UTC+8 的時區物件, 8 小時的偏移量
    tz_utc_plus_8 = timezone(timedelta(hours=8))

    # 獲取帶有時區的當前時間 (如果系統時間是 naive)
    # 1. 獲取當前 naive datetime
    naive_now = datetime.now()

    # 2. 將 naive datetime 加上時區資訊 (假設系統時間就是 UTC+8)
    aware_now_taiwan = naive_now.astimezone(tz_utc_plus_8) 

    # 3. 獲取真正的 UTC 時間
    utc_now = datetime.now(timezone.utc)

    # return (f"創建的時區物件: {tz_utc_plus_8}")
    return (f"{aware_now_taiwan.strftime('%Y-%m-%d %H:%M:%S')}")
    # return (f"當前 UTC 時間: {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")

