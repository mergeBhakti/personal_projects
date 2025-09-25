
#Code for sending only important events during the match
import requests, json, schedule, time


def send_telegram(message):
    for cid in CHAT_IDS:
        params = {"chat_id": cid, "text": message}
        requests.get(f"{URL}/sendMessage", params=params)


def job():
    global last_msg
    res = requests.get("https://www.cricbuzz.com/api/cricket-match/commentary/119834")
    data = res.json()
    ms = data["miniscore"]

    event = ms.get("event", "")
    status = ms.get("status", "")
    alerts = []

    # --- Wicket ---
    if "WICKET" in event.upper():
        alerts.append(f"❌ WICKET! {event}")

    # --- Four / Six ---
    elif "FOUR" in event.upper():
        alerts.append(f"🏏 FOUR! {event}")
    elif "SIX" in event.upper():
        alerts.append(f"💥 SIX! {event}")

    # --- Milestones ---
    striker = ms["batsmanStriker"]
    if striker["batRuns"] in [50, 100]:
        alerts.append(f"🎉 {striker['batName']} reaches {striker['batRuns']} runs!")

    non_striker = ms["batsmanNonStriker"]
    if non_striker["batRuns"] in [50, 100]:
        alerts.append(f"🎉 {non_striker['batName']} reaches {non_striker['batRuns']} runs!")

    # --- End of Over ---
    if "OVER" in event.upper():
        scoreline = f"{ms['batTeam']['teamScore']}/{ms['batTeam']['teamWkts']} in {ms['overs']} overs"
        alerts.append(f"🔄 End of Over {ms['overs']} → {scoreline}")

    # --- Match End ---
    if "won" in status.lower() or "match over" in status.lower():
        alerts.append(f"🏆 {status}")

    # --- Send alerts ---
    for msg in alerts:
        if msg != last_msg:  # deduplication
            send_telegram(msg)
            last_msg = msg
            print("✅ Sent:", msg)
        else:
            print("⏸ Duplicate skipped")

