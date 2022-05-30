from email import message
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import sys
import json
from turtle import delay
from unittest import result
HOST = "192.168.1.101"
PORT = 9999

##-------獨處json檔的資料----------------------------------------
with open('cutbox.json','r',encoding='utf-8') as file:
    cutbox_string = json.load(file)
# ---------------------------------------------------

class NeuralHttp(BaseHTTPRequestHandler):
    def do_GET(self):
#-------查詢單一機台資訊----------------------------------------
        if change == "a":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(cutbox_string['查詢單一機台資訊']), "utf-8"))
#-------裁票機開/關機---------------------------------------------
        if change == "b":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(cutbox_string['裁票機開/關機']), "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

change = input("請輸入你要的模式，查詢單一機台資訊請按a，裁票機開/關機請按b: ")
server = HTTPServer((HOST, PORT), NeuralHttp)
print ("Server now running...")
server.serve_forever()
server.server_close()
print ("Server stopped...")

