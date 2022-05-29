from email import message
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import sys
import json
from turtle import delay
from unittest import result
HOST = "192.168.1.101"
PORT = 9999

#--------------------------------------------------------
change = 1
success = 0
Message = "success"
timestamp = 1653457092123
events = "ticketPower"
with open('cutbox.json','r',encoding='utf-8') as file:
    json_string = json.load(file)
# ---------------------------------------------------

class NeuralHttp(BaseHTTPRequestHandler):
    def do_GET(self):
#-------查詢單一機台資訊----------------------------------------
        if change == "a":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes('{\n\t"return": "'+ str(success)+'",\n', "utf-8"))
            self.wfile.write(bytes('\t"Message": "'+ Message+'",\n', "utf-8"))
            self.wfile.write(bytes('\t"result": '+ str(json_string['result'])+'\n}', "utf-8"))
#-------裁票機開/關機---------------------------------------------
        if change == "b":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes('{\n\t"events": "'+events+'",\n', "utf-8"))
            self.wfile.write(bytes('\t"timestamp": "'+str(timestamp) +'",\n', "utf-8"))
            self.wfile.write(bytes('\t"source": '+ str(json_string['source-openclose'])+'\n}', "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

change = input("請輸入你要的模式，查詢單一機台資訊請按a，裁票機開/關機請按b")
server = HTTPServer((HOST, PORT), NeuralHttp)
print ("Server now running...")
server.serve_forever()
server.server_close()
print ("Server stopped...")

