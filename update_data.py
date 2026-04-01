import pandas as pd
from datetime import datetime
import random
import os

file_path = "data/traffic.csv"

print("👉 FILE USED:", os.path.abspath(file_path))

data = pd.read_csv(file_path)

data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

today = datetime.today().strftime('%Y-%m-%d')

if today not in data['Date'].astype(str).values:
    new_row = {
        "Date": today,
        "Users": 999,   # 👈 fixed number to easily see
        "PageViews": 999,
        "BounceRate": 99,
        "Source": "TEST"
    }

    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

    data.to_csv(file_path, index=False)
    print("✅ SAVED SUCCESSFULLY")

else:
    print("⚠ ALREADY EXISTS")
