# Code for Summary as well as important alerts:


import requests, schedule, time

TOKEN = "YOUR_BOT_TOKEN"
CHAT_IDS = ["-4614838359", "5876368685"]
URL = f"https://api.telegram.org/bot{TOKEN}"

last_msg = None

def send_telegram(message):
    for cid in CHAT_IDS:
        params = {"chat_id": cid, "text": message}
        requests.get(f"{URL}/sendMessage", params=params)


def get_score():
    url = "https://www.cricbuzz.com/api/cricket-match/commentary/119834"  # replace with matchId
    res = requests.get(url)
    return res.json()


def job():
    """Send event-based alerts"""
    global last_msg
    data = get_score()
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


def summary():
    """Send a summary update every few minutes"""
    data = get_score()
    ms = data["miniscore"]
    msg = (
        f"📊 Score Update\n"
        f"{ms['batTeam']['teamScore']}/{ms['batTeam']['teamWkts']} in {ms['overs']} overs\n"
        f"Striker: {ms['batsmanStriker']['batName']} {ms['batsmanStriker']['batRuns']}({ms['batsmanStriker']['batBalls']})\n"
        f"Non-Striker: {ms['batsmanNonStriker']['batName']} {ms['batsmanNonStriker']['batRuns']}({ms['batsmanNonStriker']['batBalls']})\n"
        f"CRR: {ms['currentRunRate']} | RRR: {ms['requiredRunRate']}\n"
        f"Status: {ms['status']}"
    )
    send_telegram(msg)
    print("📊 Summary sent")


# 🔹 Schedule jobs
schedule.every(30).seconds.do(job)   # event-based checks
schedule.every(5).minutes.do(summary)  # periodic summary


print("🏏 Bot running with events + summary...")
while True:
    schedule.run_pending()
    time.sleep(1)