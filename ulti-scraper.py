import requests
from bs4 import BeautifulSoup
import pandas as pd

max_id = 100  # adjust upward as needed
miss_limit = 10  # stop if 10 consecutive invalid/missing pages
miss_count = 0

headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": "PHPSESSID=YOUR_SESSION_ID"
}

writer = pd.ExcelWriter("ultifresh_all_inventory.xlsx", engine="openpyxl")

for pid in range(1, max_id + 1):
    url = f"https://ultifresh.com.my/en/productdetail/{pid}"
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        miss_count += 1
        print(f"⚠️ ID {pid} – status {resp.status_code}, skip")
        if miss_count >= miss_limit:
            print("🛑 Too many misses—stopping early.")
            break
        continue

    miss_count = 0  # reset on success
    soup = BeautifulSoup(resp.content, "html.parser")
    table = soup.select_one("table.table-bordered")
    if not table:
        print(f"❌ ID {pid} – no table, skip")
        continue

    # extract headers and rows
    headers_list = [th.get_text(strip=True) for th in table.select("thead th")]
    rows = [[td.get_text(strip=True) for td in tr.find_all("td", recursive=False)]
            for tr in table.select("tbody tr")
            if len(tr.find_all("td", recursive=False)) == len(headers_list)]

    if not rows:
        print(f"⚠️ ID {pid} – table found but empty rows, skip")
        continue

    # name sheet using product ID
    sheet = f"PID{pid}"
    df = pd.DataFrame(rows, columns=headers_list)
    df.to_excel(writer, sheet_name=sheet, index=False)
    print(f"✅ ID {pid} – extracted to sheet {sheet}")

writer.close()
print("✅ All done! Data saved in 'ultifresh_all_inventory.xlsx'")
