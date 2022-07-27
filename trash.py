# Use this token to access the HTTP API:
# 5501225728:AAH6g1riVNnGBOaH31G6ByCe3XpE3UFTtE0


import requests


API_link = "https://api.telegram.org/bot5501225728:AAH6g1riVNnGBOaH31G6ByCe3XpE3UFTtE0"
update = requests.get(API_link + "/getUpdates?offset=-1").json()
print(update)

message = update["result"][0]["message"]
chat_id = message["from"]["id"]
nikname = message["from"]["first_name"] + ' ' + message["from"]["last_name"]
text = message["text"]

print(message)
print(chat_id)
print(text)
print(nikname)

send_message = requests.get(API_link + f"/sendMessage?chat_id={chat_id}&text=hi boss")