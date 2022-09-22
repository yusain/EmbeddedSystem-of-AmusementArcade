from ast import While
import http.client, urllib.parse
import pprint
import json
import socket
import sys
import requests
from datetime import datetime
from time import sleep
import time
#define value
dict = {}
pulse = {}
foo = {}
url = "https://b645-60-248-161-128.jp.ngrok.io"
#url = "https://f0ca-163-13-133-72.jp.ngrok.io"

globaLotteryMotor = 2
print("[main.GPIOPop.model = 出票口] timeout : gpio",globaLotteryMotor,"無法取樣")
'''
timeout = time.time() + 5#(count+0.8)*(1/12)
print(time.time() > timeout)
while True:
    if time.time() > timeout:
        print("[main.GPIOPop.model = 出票口] timeout : gpio")
        break 
'''


'''
with open("config_data_1.json", "r", encoding='utf-8')as r:
    dict = json.load(r)
    for i in range(0, len(dict["Machinestate"]['results']["model"])):
        if dict["Machinestate"]['results']["model"][i]["_id"] == 21:
            foo = dict["Machinestate"]['results']["model"][i]
            dict["Machinestate"]['results']["vendorHwid"] += str(foo["_id"])
            del (dict["Machinestate"]['results']["model"],foo["_id"])
            pulse = dict["Machinestate"]
            pulse['results'].update(foo)
            print(pulse)
            break
'''
'''
# 当前日期和时间
def timestampWrite(): 
    now = datetime.now()
    timestamp = int(datetime.timestamp(now)*1000)
    print("时间戳 =", timestamp)

    with open("config_data_1.json", "r", encoding='utf-8')as r:
        dict = json.load(r)
        dict["webhook"]['events'][0]['timestamp'] = timestamp

    with open("config_data_1.json", "w", encoding='utf-8')as w: 
        w.write(json.dumps(dict, ensure_ascii=False, indent=2))
'''


'''
#數值回傳測試(v2.0)
def coinPulse():
    headers = {'Content-type': 'application/json'}
    with open("config_data_1.json", "r", encoding='utf-8')as r:
        pulse = json.load(r)
    #包裝
    foo =pulse["webhook"]
    json_data = json.dumps(foo, ensure_ascii=False, indent=2)
    print(json_data)
    
    response = requests.post( url + '/webhook', json_data, headers)
    print("state: ",response.status_code ," response: " , response.json())
    #sleep(3)


coinPulse()
'''
'''
#數值回傳測試(v1.0)only for localhost
conn = http.client.HTTPConnection("https://f0ca-163-13-133-72.jp.ngrok.io", port=3001)
conn.request('POST', '/webhook', json_data, headers)
response = conn.getresponse()
print(response.read().decode())
conn.close()
'''

'''
#數值寫入測試
with open("test.json", "r", encoding='utf-8')as x:
    dict = json.load(x)
    dict["MachineCoinVote"]['events'][0]['source']['count'] = 11364
     #print(json.load(x))   
with open("test.json", "w", encoding='utf-8')as f: 
    f.write(json.dumps(dict, ensure_ascii=False, indent=2))
'''