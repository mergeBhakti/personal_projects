# import requests, json
# import time


# def get_score():
#     url = "https://www.cricbuzz.com/api/cricket-match/commentary/119834"  # replace matchId
#     res = requests.get(url)
#     data = res.json()
#     ms = data["miniscore"]

#     score_msg = (
#         f"{ms['batTeam']['teamScore']} / {ms['batTeam']['teamWkts']} in {ms['overs']} overs\n"
#         f"Striker: {ms['batsmanStriker']['batName']} {ms['batsmanStriker']['batRuns']}({ms['batsmanStriker']['batBalls']})\n"
#         f"Non-Striker: {ms['batsmanNonStriker']['batName']} {ms['batsmanNonStriker']['batRuns']}({ms['batsmanNonStriker']['batBalls']})\n"
#         f"Partnership: {ms['partnerShip']['runs']}({ms['partnerShip']['balls']})\n"
#         f"Bowler: {ms['bowlerStriker']['bowlName']} {ms['bowlerStriker']['bowlOvs']} overs, {ms['bowlerStriker']['bowlWkts']} wkts\n"
#         f"Econ: {ms['bowlerStriker']['bowlEcon']}\n"
#         f"Last Ball: {ms['event']}\n"
#         f"Recent Overs: {ms['recentOvsStats']}\n"
#         f"CRR: {ms['currentRunRate']} | RRR: {ms['requiredRunRate']}\n"
#         f"Status: {ms['status']}"
#     )

#     return score_msg


# def send_telegram(message):
#     TOKEN = "8289359101:AAGR8NcMxZG3cUieCMBsL5aQJSU4w38ZfLU"
#     CHAT_ID = "-4614838359"  # private, group (-1234), or channel (@name or -100xxxx)
#     url = f"https://api.telegram.org/bot8289359101:AAGR8NcMxZG3cUieCMBsL5aQJSU4w38ZfLU/sendMessage"
#     params = {"chat_id": CHAT_ID,"text": message}
#     res = requests.get(url, params=params)
#     return res.json()

# ADMIN_ID = 5876368685  # replace with your own Telegram user ID

# def check_commands(last_update_id=0):
#     url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
#     params = {"offset": last_update_id + 1}
#     res = requests.get(url, params=params).json()
    
#     new_update_id = last_update_id
#     command = None

#     if "result" in res and len(res["result"]) > 0:
#         for update in res["result"]:
#             text = update["message"]["text"].strip().lower()
#             sender_id = update["message"]["from"]["id"]
#             new_update_id = update["update_id"]

#             if sender_id == ADMIN_ID and text in ["/stop", "/start"]:
#                 command = text
#             elif text in ["/stop","/start"]:
#                 send_telegram("Only Admin can command!")
#     return command, new_update_id



# def run_updates(interval=30):
#     last_msg = None
#     running = True
#     last_update_id = 0

#     while True:
#         # Check if commands came in
#         command , last_update_id = check_commands(last_update_id)
#         if command == "/stop":
#             running = False
#             send_telegram("⏹ Stopped live updates.")

#         elif command == "/start":
#             running = True
#             send_telegram("▶️ Resumed live updates.")

#         # only fetch and send score if running
#         if running:
#             msg = get_score()
#             if msg != last_msg:   # deduplication check
#                 send_telegram(msg)
#                 last_msg = msg
#                 print("Sent new update ✅")
#             else:
#                 print("No change, skipping…")
                
#         time.sleep(interval)

# if __name__ == "__main__":
#     run_updates(30)  # check every 30 seconds

#-------------------------------------------------------------------------------------


# Code for sending only important events during the match

# def job():
#     global last_msg
#     res = requests.get("https://www.cricbuzz.com/api/cricket-match/commentary/119834")
#     data = res.json()
#     ms = data["miniscore"]

#     event = ms.get("event", "")
#     status = ms.get("status", "")
#     alerts = []

#     # --- Wicket ---
#     if "WICKET" in event.upper():
#         alerts.append(f"❌ WICKET! {event}")

#     # --- Four / Six ---
#     elif "FOUR" in event.upper():
#         alerts.append(f"🏏 FOUR! {event}")
#     elif "SIX" in event.upper():
#         alerts.append(f"💥 SIX! {event}")

#     # --- Milestones ---
#     striker = ms["batsmanStriker"]
#     if striker["batRuns"] in [50, 100]:
#         alerts.append(f"🎉 {striker['batName']} reaches {striker['batRuns']} runs!")

#     non_striker = ms["batsmanNonStriker"]
#     if non_striker["batRuns"] in [50, 100]:
#         alerts.append(f"🎉 {non_striker['batName']} reaches {non_striker['batRuns']} runs!")

#     # --- End of Over ---
#     if "OVER" in event.upper():
#         scoreline = f"{ms['batTeam']['teamScore']}/{ms['batTeam']['teamWkts']} in {ms['overs']} overs"
#         alerts.append(f"🔄 End of Over {ms['overs']} → {scoreline}")

#     # --- Match End ---
#     if "won" in status.lower() or "match over" in status.lower():
#         alerts.append(f"🏆 {status}")

#     # --- Send alerts ---
#     for msg in alerts:
#         if msg != last_msg:  # deduplication
#             send_telegram(msg)
#             last_msg = msg
#             print("✅ Sent:", msg)
#         else:
#             print("⏸ Duplicate skipped")

# -----------------------------------------------------------------------------

# Code for Summary as well as important alerts:


# import requests, schedule, time

# TOKEN = "YOUR_BOT_TOKEN"
# CHAT_IDS = ["-4614838359", "5876368685"]
# URL = f"https://api.telegram.org/bot{TOKEN}"

# last_msg = None

# def send_telegram(message):
#     for cid in CHAT_IDS:
#         params = {"chat_id": cid, "text": message}
#         requests.get(f"{URL}/sendMessage", params=params)


# def get_score():
#     url = "https://www.cricbuzz.com/api/cricket-match/commentary/119834"  # replace with matchId
#     res = requests.get(url)
#     return res.json()


# def job():
#     """Send event-based alerts"""
#     global last_msg
#     data = get_score()
#     ms = data["miniscore"]

#     event = ms.get("event", "")
#     status = ms.get("status", "")
#     alerts = []

#     # --- Wicket ---
#     if "WICKET" in event.upper():
#         alerts.append(f"❌ WICKET! {event}")

#     # --- Four / Six ---
#     elif "FOUR" in event.upper():
#         alerts.append(f"🏏 FOUR! {event}")
#     elif "SIX" in event.upper():
#         alerts.append(f"💥 SIX! {event}")

#     # --- Milestones ---
#     striker = ms["batsmanStriker"]
#     if striker["batRuns"] in [50, 100]:
#         alerts.append(f"🎉 {striker['batName']} reaches {striker['batRuns']} runs!")

#     non_striker = ms["batsmanNonStriker"]
#     if non_striker["batRuns"] in [50, 100]:
#         alerts.append(f"🎉 {non_striker['batName']} reaches {non_striker['batRuns']} runs!")

#     # --- End of Over ---
#     if "OVER" in event.upper():
#         scoreline = f"{ms['batTeam']['teamScore']}/{ms['batTeam']['teamWkts']} in {ms['overs']} overs"
#         alerts.append(f"🔄 End of Over {ms['overs']} → {scoreline}")

#     # --- Match End ---
#     if "won" in status.lower() or "match over" in status.lower():
#         alerts.append(f"🏆 {status}")

#     # --- Send alerts ---
#     for msg in alerts:
#         if msg != last_msg:  # deduplication
#             send_telegram(msg)
#             last_msg = msg
#             print("✅ Sent:", msg)
#         else:
#             print("⏸ Duplicate skipped")


# def summary():
#     """Send a summary update every few minutes"""
#     data = get_score()
#     ms = data["miniscore"]
#     msg = (
#         f"📊 Score Update\n"
#         f"{ms['batTeam']['teamScore']}/{ms['batTeam']['teamWkts']} in {ms['overs']} overs\n"
#         f"Striker: {ms['batsmanStriker']['batName']} {ms['batsmanStriker']['batRuns']}({ms['batsmanStriker']['batBalls']})\n"
#         f"Non-Striker: {ms['batsmanNonStriker']['batName']} {ms['batsmanNonStriker']['batRuns']}({ms['batsmanNonStriker']['batBalls']})\n"
#         f"CRR: {ms['currentRunRate']} | RRR: {ms['requiredRunRate']}\n"
#         f"Status: {ms['status']}"
#     )
#     send_telegram(msg)
#     print("📊 Summary sent")


# # 🔹 Schedule jobs
# schedule.every(30).seconds.do(job)   # event-based checks
# schedule.every(5).minutes.do(summary)  # periodic summary


# print("🏏 Bot running with events + summary...")
# while True:
#     schedule.run_pending()
#     time.sleep(1)

# ------------------------------------------------------------------------------


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
