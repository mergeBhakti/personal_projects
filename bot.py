import requests

TOKEN = "8289359101:AAGR8NcMxZG3cUieCMBsL5aQJSU4w38ZfLU"
CHAT_ID = "-4614838359"
msg = "Now I am a group admin 😈"

url = f"https://api.telegram.org/bot8289359101:AAGR8NcMxZG3cUieCMBsL5aQJSU4w38ZfLU/sendMessage"
params = {"chat_id": CHAT_ID, "text": msg}

r = requests.get(url, params=params)
print(r.json())  # should return ok: true
