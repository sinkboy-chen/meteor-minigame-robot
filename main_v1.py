import time
import requests
from requests.structures import CaseInsensitiveDict
import json
import os

account_1 = os.environ["account_1"]
account_2 = os.environ["account_2"]
account_1 = json.loads(account_1)
account_2 = json.loads(account_2)

def get_cookie():
    url = "https://meteor.today/board/all"
    resp = requests.get(url)
    cookie = resp.headers['set-cookie'].split(";")[0]
    return cookie

def login(account):
    url = "https://meteor.today/user/login_v2"
    headers = CaseInsensitiveDict()
    headers["cookie"] = account["cookie"]
    data = account["account_data"]
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code!=200:
        print(resp.status_code)
        print(resp.text)
        print("login error")
        exit()

def get_mini_game_id(account):
    url = "https://meteor.today/miniGame/get_active_miniGame_by_type"

    headers = CaseInsensitiveDict()
    headers["content-type"] = "application/json;charset=UTF-8"
    headers["cookie"] = account["cookie"]
    data = '{"type":"dailyLogin"}'
    resp = requests.post(url, headers=headers, data=data)
    mini_game_id = resp.text
    mini_game_id = mini_game_id.split('miniGameId":"')[1]
    mini_game_id = mini_game_id.split('"')[0]
    return mini_game_id

def play_mini_game(account, mini_game_id):
    url = "https://meteor.today/minigame/play_miniGame"
    data = '{"miniGameId":"' + mini_game_id + '","userId":"' + account["user_id"] + '"}'
    for i in range(10):
        resp = requests.post(url, data=data)
        print(f"attempt {i+1}: {resp.status_code} {resp.text}")
        if resp.status_code != 400:
            return
        time.sleep(min(i*5+1, 30))

print("getting cookie")
account_1["cookie"] = get_cookie()
print("logging in account")
login(account_1)
print("getting minigame id")
mini_game_id = get_mini_game_id(account_1)

time.sleep(1)
print("playing minigame for account 1 1st time")
play_mini_game(account_1, mini_game_id)
time.sleep(1)
print("playing minigame for account 1 2nd time")
play_mini_game(account_1, mini_game_id)

print("playing minigame for account 2 1st time")
play_mini_game(account_2, mini_game_id)
time.sleep(1)
print("playing minigame for account 2 2nd time")
play_mini_game(account_2, mini_game_id)
