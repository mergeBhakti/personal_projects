

#-------------------------------------------------------------------------------------





import requests, json, schedule, time

# --- CONFIG ---
TOKEN = "8289359101:AAGR8NcMxZG3cUieCMBsL5aQJSU4w38ZfLU"
CHAT_IDS = ["5876368685"]  # group, private, or channel
ADMIN_ID = 5876368685  # replace with your own Telegram user ID
URL = f"https://api.telegram.org/bot8289359101:AAGR8NcMxZG3cUieCMBsL5aQJSU4w38ZfLU"

# --- FUNCTIONS ---

def get_score():
    url = "https://www.cricbuzz.com/api/cricket-match/commentary/113274"  # replace matchId
    res = requests.get(url)
    data = res.json()
    ms = data["miniscore"]

    score_msg = (
        f"{ms['batTeam']['teamScore']} / {ms['batTeam']['teamWkts']} in {ms['overs']} overs\n"
        f"Striker: {ms['batsmanStriker']['batName']} {ms['batsmanStriker']['batRuns']}({ms['batsmanStriker']['batBalls']})\n"
        f"Non-Striker: {ms['batsmanNonStriker']['batName']} {ms['batsmanNonStriker']['batRuns']}({ms['batsmanNonStriker']['batBalls']})\n"
        f"Partnership: {ms['partnerShip']['runs']}({ms['partnerShip']['balls']})\n"
        f"Bowler: {ms['bowlerStriker']['bowlName']} {ms['bowlerStriker']['bowlOvs']} overs, {ms['bowlerStriker']['bowlWkts']} wkts\n"
        f"Econ: {ms['bowlerStriker']['bowlEcon']}\n"
        f"Last Ball: {ms['event']}\n"
        f"Recent Overs: {ms['recentOvsStats']}\n"
        f"CRR: {ms['currentRunRate']} | RRR: {ms['requiredRunRate']}\n"
        f"Status: {ms['status']}"
    )
    return score_msg


def send_telegram(message):
    for cid in CHAT_IDS:
        params = {"chat_id": cid, "text": message}
        requests.get(f"{URL}/sendMessage", params=params)


# Deduplication tracker
last_msg = None
running = True
last_update_id = 0


def job():
    global last_msg
    if not running:
        return
    msg = get_score()
    if msg != last_msg:
        send_telegram(msg)
        last_msg = msg
        print("✅ Sent new update")
    else:
        print("⏸ No change, skipped")


def check_commands():
    """Poll Telegram for admin commands"""
    global running, last_update_id
    r = requests.get(f"{URL}/getUpdates", params={"offset": last_update_id + 1}).json()
    if "result" in r and len(r["result"]) > 0:
        for update in r["result"]:
            last_update_id = update["update_id"]
            message = update.get("message", {})
            text = message.get("text", "").strip().lower()
            sender_id = message.get("from", {}).get("id")

            if text in ["/stop", "/start"]:
                if sender_id == ADMIN_ID:
                    if text == "/stop" and running:
                        running = False
                        send_telegram("⏹ Updates stopped by admin.")
                    elif text == "/start" and not running:
                        running = True
                        send_telegram("▶️ Updates resumed by admin.")
                else:
                    send_telegram("⚠️ Only the admin can control start/stop.")


# --- SCHEDULER SETUP ---
schedule.every(10).seconds.do(job)  # frequent updates
schedule.every(5).minutes.do(job)   # summary update


print("🏏 Cricket alerts bot with admin control is running...")
while True:
    schedule.run_pending()
    check_commands()
    time.sleep(1)
