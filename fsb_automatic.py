import requests
import json
import os
import time
import datetime
from pyobigram.client import ObigramClient

HOST_ = os.environ.get('host',f'http://freechunkdl.s3.ydns.eu/')
BOT_TOKEN = os.environ.get('bot_token',f'7071804471:AAEiuDNB-YEhRRtBLWuTyW3CxAuZEAs5p0o')
USER_SAVED = os.environ.get('u_s',f'5776065676')
TIME_SLEEP = os.environ.get('t_s',6)

def get_users(db):
    resp = requests.request('GET',HOST_+'user/gets',data={'db':db})
    if resp.status_code==200:
        return resp.text
    return None

def update_user(username,data,db):
	return requests.post(HOST_+'user/update/'+username,json={'db':db,'userplan':data});

DB_I = 0
def save():
    global DB_I
    try:
        DB_I+=1
        max = 10
        if DB_I>=max:
            DB_I = 0
            print('Sleeping...')
            time.sleep(60*60*TIME_SLEEP)
            return
        db = f'db{DB_I}'
        users = get_users(db)
        if len(json.loads(users))>1:
            with open(f'{db}.json','w') as f:
                f.write(users)
                print('users.json Saved!')
            obigram = ObigramClient(BOT_TOKEN)
            if DB_I==1:
                msg = obigram.send_message(USER_SAVED,f'#update {datetime.datetime.now()}')
            obigram.send_file(USER_SAVED,f'{db}.json')
            print('sending to chat!')
    except:
        DB_I = 0
        time.sleep(60*60*TIME_SLEEP)
    

while True:
    try:
        save()
    except:pass



