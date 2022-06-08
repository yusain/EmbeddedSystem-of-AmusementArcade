import http.client, urllib.parse
import pprint
import json
import sys
import requests   
chose = input("a = 查詢單一機台資訊-裁票機\nb = 查詢單一機台資訊-遊戲機\nc = 要求遠端投幣-遊戲機\nd = 要求遠端退幣-遊戲機\ne = 要求遠端開關機-遊戲機\nf = 查詢單一機台資訊-禮品機\n")
#設定
conn = http.client.HTTPConnection("163.13.133.185", port=80) 
headers = {'Content-type': 'application/json'}
if chose == 'a' :
    conn.request("GET", "/request/cutbox/state")
    r1 = conn.getresponse()
    body = r1.read()
    print(sys.getdefaultencoding())   
    body_to_unicode = body.decode(encoding='utf-8')  # 要告訴decode原本的編碼是哪種
    print(r1.status, r1.reason)
    print(body_to_unicode)
    conn.close()
elif chose == 'b' :
    conn.request("GET", "/request/state")
    r1 = conn.getresponse()
    body = r1.read()
    print(sys.getdefaultencoding())   
    body_to_unicode = body.decode(encoding='utf-8')  # 要告訴decode原本的編碼是哪種
    print(r1.status, r1.reason)
    print(body_to_unicode)
    conn.close()
elif chose == 'c' :
    print("使用預設值")
    #包裝
    foo = {'_id': 123456789,'count': 2,'outputPort':1}
    json_data = json.dumps(foo)
    #格式
    conn.request('POST', '/request/game/coin', json_data, headers)
    r1 = conn.getresponse()
    print(r1.read().decode())   
    body = r1.read() 
    body_to_unicode = body.decode(encoding='utf-8')  # 要告訴decode原本的編碼是哪種
    print(r1.status, r1.reason)
    print(body_to_unicode)
    conn.close()
elif chose == 'd' :
    print("使用預設值")
    #包裝
    foo = {'_id': 123456789,'count': -2,'outputPort':1}
    json_data = json.dumps(foo)
    #格式
    conn.request('POST', '/request/game/coin', json_data, headers)
    r1 = conn.getresponse()
    print(r1.read().decode())   
    body = r1.read() 
    body_to_unicode = body.decode(encoding='utf-8')  # 要告訴decode原本的編碼是哪種
    print(r1.status, r1.reason)
    print(body_to_unicode)
    conn.close()
elif chose == 'e' :
    print("使用預設值")
    #包裝
    foo = {'_id': 123456789,'position': 1}
    json_data = json.dumps(foo)
    #格式
    conn.request('POST', '/request/game/power', json_data, headers)
    r1 = conn.getresponse()
    print(r1.read().decode())   
    body = r1.read()
    body_to_unicode = body.decode(encoding='utf-8')  # 要告訴decode原本的編碼是哪種
    print(r1.status, r1.reason)
    conn.close()
elif chose == 'f' :
    conn.request("GET", "/request/giftbox/state")
    r1 = conn.getresponse()
    body = r1.read()
    print(sys.getdefaultencoding())   
    body_to_unicode = body.decode(encoding='utf-8')  # 要告訴decode原本的編碼是哪種
    print(r1.status, r1.reason)
    print(body_to_unicode)
    conn.close()