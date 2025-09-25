import requests, json
import time


def get_score():
    url = "https://www.cricbuzz.com/api/cricket-match/commentary/119834"  # replace matchId
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
    TOKEN = "8289359101:AAGR8NcMxZG3cUieCMBsL5aQJSU4w38ZfLU"
    CHAT_ID = "-4614838359"  # private, group (-1234), or channel (@name or -100xxxx)
    url = f"https://api.telegram.org/bot8289359101:AAGR8NcMxZG3cUieCMBsL5aQJSU4w38ZfLU/sendMessage"
    params = {"chat_id": CHAT_ID,"text": message}
    res = requests.get(url, params=params)
    return res.json()

ADMIN_ID = 5876368685  # replace with your own Telegram user ID

def check_commands(last_update_id=0):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"offset": last_update_id + 1}
    res = requests.get(url, params=params).json()
    
    new_update_id = last_update_id
    command = None

    if "result" in res and len(res["result"]) > 0:
        for update in res["result"]:
            text = update["message"]["text"].strip().lower()
            sender_id = update["message"]["from"]["id"]
            new_update_id = update["update_id"]

            if sender_id == ADMIN_ID and text in ["/stop", "/start"]:
                command = text
            elif text in ["/stop","/start"]:
                send_telegram("Only Admin can command!")
    return command, new_update_id



def run_updates(interval=30):
    last_msg = None
    running = True
    last_update_id = 0

    while True:
        # Check if commands came in
        command , last_update_id = check_commands(last_update_id)
        if command == "/stop":
            running = False
            send_telegram("⏹ Stopped live updates.")

        elif command == "/start":
            running = True
            send_telegram("▶️ Resumed live updates.")

        # only fetch and send score if running
        if running:
            msg = get_score()
            if msg != last_msg:   # deduplication check
                send_telegram(msg)
                last_msg = msg
                print("Sent new update ✅")
            else:
                print("No change, skipping…")
                
        time.sleep(interval)

if __name__ == "__main__":
    run_updates(30)  # check every 30 seconds