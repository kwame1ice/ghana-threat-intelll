import csv
import datetime
import requests
from pathlib import Path

# Replace this with your Discord Webhook URL later
WEBHOOK_URL = import os
WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1404560131416526898/D7A_0ywlo10cLLO_Btj8xHuPTr89Vd2oXUI_0DtrowT2FBifTJRviHfYYUcUcszl2tq3")


# Example data for now
ioc_data = [
    {"Type":"Domain","Value":"police.gov.gh","Risk":"Critical","Source":"darkforums.st","Description":"Compromised police system"},
    {"Type":"Telegram","Value":"https://t.me/example","Risk":"High","Source":"Telegram","Description":"Actor channel"}
]

def save_iocs(iocs):
    today = datetime.date.today().isoformat()
    filename = f"extracted_iocs_{today}.csv"
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["Type","Value","Risk","Source","Description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in iocs:
            writer.writerow(i)
    print("[+] Saved IOCs to", filename)
    return filename

def send_discord_alert(iocs):
    if not WEBHOOK_URL or "PASTE-YOUR-WEBHOOK" in WEBHOOK_URL:
        print("[!] No webhook URL configured. Skipping Discord alert.")
        return
    content = "**New Ghana IOCs collected**\n"
    for i in iocs:
        content += f"- [{i['Risk']}] {i['Type']}: {i['Value']}\n"
    payload = {"content": content}
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if r.status_code in (200,204):
            print("[+] Alert sent to Discord.")
        else:
            print("[!] Discord responded:", r.status_code, r.text)
    except Exception as e:
        print("[!] Error sending Discord alert:", e)

if __name__ == "__main__":
    Path(".").mkdir(exist_ok=True)
    save_iocs(ioc_data)
    send_discord_alert(ioc_data)
