import ctypes, threading, requests, time, json
token = "token"
headers = {'authorization' : f'Bot {token}'}
dmed = []
not_dmed  = []
content = """
text
"""
msg = {"content" : content}
def title(text):
    ctypes.windll.kernel32.SetConsoleTitleW(f"{text} || @siph.er")
def date_send(text):
    print(f"[!] {text}")
def massdm(total,user, msg):
    retries = 0
    payload = {'recipient_id': user}
    src = requests.post('https://canary.discordapp.com/api/v6/users/@me/channels', headers=headers, json=payload)
    dm_json = src.json()
    if not "id" in src.json():
        not_dmed.append(user)
        date_send(f"Fail to create DM Channel with {user} || Reason: {src.json()['message']}")
        return
    while True:
        src = requests.post(f"https://canary.discordapp.com/api/v6/channels/{dm_json['id']}/messages", headers=headers, json=msg)
        if src.status_code == 200:
            dmed.append(user)
            date_send(f"Success: {user} || Message ID: {src.json()['id']}")
            break
        elif src.status_code == 429:
            retries += 1
            if retries == 10:
                not_dmed.append(user)
                date_send(f"Unable to DM {user} due to hitting max retries.")
                break
            else:
                ratelimit = int(src.json()['retry_after'])/1000
                not_dmed.append(user)
                date_send(f"Fail: {user} || Ratelimit: {ratelimit}ms")
                time.sleep(ratelimit)
        else:
            code = src.json()['message']
            not_dmed.append(user)
            date_send(f"Fail: {user} || Reason: {code}")
            break
    title(f"TOTAL: {total} || DMED : {len(dmed)} || Not DMED: {len(not_dmed)}")
users = open("ids.txt","r").read().splitlines()
blacklist = open("blacklisted.txt","r").read().splitlines()
#payload = json.loads(open("payload.json","r").read())
for user in users:
    if not user in blacklist:
        threading.Thread(target=massdm,args=[len(users),user,msg]).start()
        time.sleep(0.1)