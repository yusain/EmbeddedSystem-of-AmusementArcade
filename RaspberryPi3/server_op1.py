from http.server import HTTPServer, BaseHTTPRequestHandler
from pyexpat import model
from urllib.parse import parse_qs, urlparse
from platform import java_ver
from datetime import datetime
from time import sleep
import requests
import json
import RPi.GPIO as GPIO  
HOST = "localhost"   
PORT = 3001
respfoo = {}
params ={}
battery_data= 4
coin_data  = 17
lottery_in= 27
lottery_out=22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(battery_data, GPIO.OUT)
GPIO.setup(lottery_in, GPIO.OUT)
GPIO.setup(lottery_out, GPIO.IN)
GPIO.setup(coin_data , GPIO.IN)


url = ""
#---------------------------#寫入timestamp#---------------------------#
def timestampWrite(): 
    now = datetime.now()
    timestamp = int(datetime.timestamp(now)*1000)
    print("timestamp =", timestamp)
    with open("config_data_1.json", "r", encoding='utf-8')as r:
        dict = json.load(r)
        dict["webhook"]["events"][0]["timestamp"] = timestamp
    with open("config_data_1.json", "w", encoding='utf-8')as w: 
        w.write(json.dumps(dict, ensure_ascii=False, indent=2))
#---------------------------#觸發投幣訊號#---------------------------#
def coinPulse():
    timestampWrite()
    headers = {'Content-type': 'application/json'}
    #讀出數值
    with open("config_data_1.json", "r", encoding='utf-8')as r:
        coinPulse = json.load(r)
        coinPulse["webhook"]["events"][0]["type"] = "coinPulse"
        coinPulse["webhook"]["events"][0]["source"]["vendorHwid"] = "dj12300211"
        coinPulse["webhook"]['events'][0]["source"]["count"] = 1
        coinPulse["coinvalue"]["count"] += 1
    #寫入type、coin變值
    print("Coin write...")
    with open("config_data_1.json", "w", encoding='utf-8')as w: 
        w.write(json.dumps(coinPulse, ensure_ascii=False, indent=2))
    #包裝
    respfoo =coinPulse["webhook"]
    json_data = json.dumps(respfoo,ensure_ascii=False, indent=2)
    #格式
    response = requests.post( url + '/webhook', json_data, headers)
    print("state: ",response.status_code ," response: " , response.json())
#---------------------------#觸發出票訊號#---------------------------#
def lotteryPulse(count):
    timestampWrite()
    headers = {'Content-type': 'application/json'}
    #讀出數值
    with open("config_data_1.json", "r", encoding='utf-8')as r:
        lotteryPulse = json.load(r)
        lotteryPulse["webhook"]["events"][0]["type"] = "lotteryPulse"
        lotteryPulse["webhook"]["events"][0]["source"]["vendorHwid"] = "dj12300221"
        lotteryPulse["webhook"]['events'][0]["source"]["count"] = count
    #GPIO輸出票
    GPIO.output(lottery_in, GPIO.HIGH)
    count_N = a = b = 0
    while True:
        if(count_N < count):
            sleep(0.01) #取樣1次/1ms
            b = a
            a = GPIO.input(lottery_out)
            if(a == 1 and b == 0):  #負緣觸發
                count_N = count_N + 1
        else:
            break
    GPIO.output(lottery_in, GPIO.LOW)
    #寫入type
    with open("config_data_1.json", "w", encoding='utf-8')as w: 
        w.write(json.dumps(lotteryPulse, ensure_ascii=False, indent=2))
    #包裝
    respfoo =lotteryPulse["webhook"]
    json_data = json.dumps(respfoo,ensure_ascii=False, indent=2)    
    #格式
    response = requests.post( url + '/webhook', json_data, headers)
    print("state: ",response.status_code ," response: " , response.json())
#---------------------------#投幣機輸入偵測#---------------------------#
def coininput():
    print("#-----------------------------CoinMachineRun--------------------#")
    while True:
        #讀出json硬幣
        with open("config_data_1.json", "r", encoding='utf-8')as r:
            foo = json.load(r)
            coin_count = foo["coinvalue"]['count']
        #變數設定
        last_status = data_status
        data_status = GPIO.input(coin_data)

        if data_status == 0 and last_status == 1:
            timestampWrite()    #寫入timestamp
            coinPulse()         #寫入投幣數值
            print("目前總硬幣量:",coin_count)
        sleep(0.05)        
# --------HTTPServer-----------------------------------------------
class NeuralHttp(BaseHTTPRequestHandler):
    #GET request
    def do_GET(self):
        #URL解析
        path = urlparse(self.path).path                 #url.path
        params = parse_qs(urlparse(self.path).query)    #url.query
# --------查詢單一機台資訊-------------------------------------------  
        if path == "/request/state": #這是PORT之後的子網域  
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()            
            with open('config_data_1.json','r',encoding='utf-8') as file:
                foo = json.load(file)
                id = str(params["_id"])[-4:-2]
                print(id)
                for i in range(0, len(foo["Machinestate"]['results']["model"])):
                    if foo["Machinestate"]['results']["model"][i]["_id"] == int(id):
                        model = foo["Machinestate"]['results']["model"][i]
                        foo["Machinestate"]['results']["vendorHwid"] += str(model["_id"])
                        del (foo["Machinestate"]['results']["model"],model["_id"])
                        pulse = foo["Machinestate"]
                        pulse['results'].update(model)
                        print(pulse)
                        break
                    else :
                        pulse = {'code' : 'error'}
            json_data = json.dumps(pulse, indent=4, ensure_ascii=False)        
            self.wfile.write(bytes(str(json_data), "utf-8"))
#-------要求遠端開/關機---------------------------------------------
        elif path == "/request/power":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            print(params["position"])
            if str(params["position"]) == "['1']" :    #開機
                foo = {"code": "Success", "message": "ok", "results": {}}
                GPIO.output(battery_data, GPIO.HIGH)
            elif str(params["position"]) == "['0']" :  #關機
                foo = {"code": "Success", "message": "ok", "results": {}}
                GPIO.output(battery_data, GPIO.LOW)
            else :
                foo = {'code' : 'error'}
            json_data = json.dumps(foo, indent=4, ensure_ascii=False)        
            self.wfile.write(bytes(str(json_data), "utf-8"))
        else:#clientResponseError
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            foo = {'code' : 'error',"nothepage":404}
            json_data = json.dumps(foo, indent=4, ensure_ascii=False)        
            self.wfile.write(bytes(str(json_data), "utf-8"))
    #POST request
    def do_POST(self):
        self.coinpluse = False
        self.lotterypluse = False
#-------要求遠端投幣/出票---------------------------------
        if self.path == "/request/gameMachine/pulse":
            #receive parameters
            self.data_string = self.rfile.read(int(self.headers['Content-Length'])).decode(encoding='utf-8')
            params = json.loads(self.data_string)  
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers() 
            with open('config_data_1.json','r',encoding='utf-8') as file:
                foo = json.load(file)["Machinepulse"]
            if params["_id"][-2] == "1" :
                self.count = params["count"]
                self.coinpluse = True
            elif params["_id"][-2] == "2" :               
                self.count = params["count"]
                self.lotterypluse = True
            else :
                foo = {"code": "Success", "message": "ok", "results": {"ack": 0}}
            #packet return
            json_data = json.dumps(foo, indent=4, ensure_ascii=False)        
            self.wfile.write(bytes(str(json_data), "utf-8"))
#-------GPIOResponse-----------------------------------------------------
        elif self.path == "/webhook":
            self.data_string = self.rfile.read(int(self.headers['Content-Length'])).decode(encoding='utf-8')
            params = json.loads(self.data_string)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            foo = {'code': 'Success','message': 'ok', 'results': 'coinPulse'}
            json_data = json.dumps(foo, indent=4, ensure_ascii=False)        
            self.wfile.write(bytes(str(json_data), "utf-8"))
        else:#clientResponseError
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            foo = {'code' : 'error',"nothepage":404}
            json_data = json.dumps(foo, indent=4, ensure_ascii=False)        
            self.wfile.write(bytes(str(json_data), "utf-8"))
#---------------------------------------------------------------------
        if self.coinpluse == True :
            for i in range(self.count):
                coinPulse()
            self.count = 0
            self.coinpluse = False
        if self.lotterypluse == True :
            lotteryPulse(self.count)
            self.count = 0
            self.lotterypluse = False

server = HTTPServer((HOST, PORT), NeuralHttp)
try:
    GPIO.output(battery_data, GPIO.LOW)
    GPIO.output(lottery_in, GPIO.LOW)
    print ("Server now running...")
    server.serve_forever()
finally:
    server.server_close()
    print ("Server stopped...")
    GPIO.cleanup()