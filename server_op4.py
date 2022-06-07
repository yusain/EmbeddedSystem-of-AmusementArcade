from email import message
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import sys
import json
from turtle import delay
from unittest import result
HOST = "163.13.133.185"   
PORT = 80
#http://163.13.133.185:9999/

# ---------------------------------------------------   
class NeuralHttp(BaseHTTPRequestHandler):
    def do_GET(self):
#-------查詢單一機台資訊-裁票機----------------------------------------
        #if self.path == "/request/cutbox/state":
        #    with open('config_data.json','r',encoding='utf-8') as file:
        #        cutbox_string = json.load(file)
        #    self.send_response(200)
        #    self.send_header("Content-Type", "application/json")
        #    self.end_headers()
        #    self.wfile.write(bytes(str(cutbox_string['查詢單一機台資訊-裁票機']), "utf-8"))
#-------查詢單一機台資訊-遊戲機---------------------------------------------
        if self.path == "/request/state": #這是PORT之後的子網域
            with open('config_data.json','r',encoding='utf-8') as file:
                cutbox_string = json.load(file)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(cutbox_string['查詢單一機台資訊-遊戲機']), "utf-8"))
#-------查詢單一機台資訊-禮品機---------------------------------------------
       #elif self.path == "/request/giftbox/state": #這是PORT之後的子網域
       #    with open('config_data.json','r',encoding='utf-8') as file:
       #        cutbox_string = json.load(file)
       #    self.send_response(200)
       #    self.send_header("Content-Type", "application/json")
       #    self.end_headers()
       #    self.wfile.write(bytes(str(cutbox_string['查詢單一機台資訊-禮品機']), "utf-8"))
#-------用來測試資料---------------------------------------------
        elif self.path == "/post/test":
            with open('test.json','r',encoding='utf-8') as file:
                cutbox_string = json.load(file)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                print(cutbox_string)
    def do_POST(self):
#-------單純接受資料---------------------------------------------
        if self.path == "/post": 
            self.data_string = self.rfile.read(int(self.headers['Content-Length'])).decode(encoding='utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = self.data_string.encode('utf-8').decode('unicode_escape')
            print(data)
#-------要求遠端投/退幣---------------------------------------------
        elif self.path == "/request/game/coin":
            self.data_string = self.rfile.read(int(self.headers['Content-Length'])).decode(encoding='utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = json.loads(self.data_string) #讀取得到的資料 -> 轉檔
            with open('test2.json','w') as file: #先打開一個json檔將資料寫入
                json.dump(data,file)
            with open('test2.json','r',encoding='utf-8') as file: #寫完再讀取
                test_b = json.load(file)
            #包裝 test_b["_id"] .format(test_b["_id"])
            foo = {'要求遠端投幣': {'return': 0, 'message': 'Success', 'results': {'_id': '{}'.format(test_b["_id"]), 'count': '{}'.format(test_b["count"]), 'outputPort': '{}'.format(test_b["outputPort"])}}}
            json_data = json.dumps(foo)
            output = json.loads(json_data)
            self.wfile.write(bytes(str(output), "utf-8"))
#-------要求遠端開/關機---------------------------------------------
        elif self.path == "/request/game/power":
            self.data_string = self.rfile.read(int(self.headers['Content-Length'])).decode(encoding='utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = json.loads(self.data_string)
            with open('test2.json','w') as file:
                json.dump(data,file)
            with open('test2.json','r',encoding='utf-8') as file:
                test_b = json.load(file)
            #包裝 test_b["_id"] .format(test_b["_id"])
            foo = {'要求遠端開關機': {'return': 0, 'message': 'Success', 'results': {'_id': '{}'.format(test_b["_id"]), 'position': '{}'.format(test_b["position"])}}}
            json_data = json.dumps(foo)
            output = json.loads(json_data)
            self.wfile.write(bytes(str(output), "utf-8"))
server = HTTPServer((HOST, PORT), NeuralHttp)
print ("Server now running...")
server.serve_forever()
server.server_close()
print ("Server stopped...")

