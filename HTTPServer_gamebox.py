from email import message
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import sys
import json
from turtle import delay
from unittest import result
HOST = "163.13.133.182"
PORT = 9999

#--------------------------------------------------------
with open('gamebox.json','r',encoding='utf-8') as file:
    gamebox_string = json.load(file)
# ---------------------------------------------------

class NeuralHttp(BaseHTTPRequestHandler):
    def do_GET(self):
#-------查詢單一機台資訊----------------------------------------
        if change =='a':
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(gamebox_string['查詢單一機台資訊']), "utf-8"))
#-------要求遠端開/關機----------------------------------------
    def do_POST(self):
        if change =='b':
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(gamebox_string['要求遠端開/關機']), "utf-8"))

change = input("請輸入你要的模式，查詢單一機台資訊請按a，要求遠端開/關機請按b: ")
server = HTTPServer((HOST, PORT), NeuralHttp)
print ("Server now running...")
server.serve_forever()
server.server_close()
print ("Server stopped...")

