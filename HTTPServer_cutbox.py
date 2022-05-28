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
results = {
    '_id': 123456789,
    'hwid': "B33585AE",
    'vendorHwid': "600031",
    'description': "裁票機",
    'locate': "中山店",
    'model': "alfabox_v2_wifi"
}
source = {
    "_id": 123456789,
    "position": True
 }
events = "ticketPower"
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
            self.wfile.write(bytes('\t"result": {\n', "utf-8"))
            self.wfile.write(bytes('\t\t"_id": '+ str(results["_id"])+',\n', "utf-8"))
            self.wfile.write(bytes('\t\t"hwid": "'+ results["hwid"]+'",\n', "utf-8"))
            self.wfile.write(bytes('\t\t"vendorHwid": "'+str(results["vendorHwid"])+'",\n', "utf-8"))
            self.wfile.write(bytes('\t\t"_description": "'+ results["description"]+'",\n', "utf-8"))
            self.wfile.write(bytes('\t\t"locate": "'+ results["locate"]+'",\n', "utf-8"))
            self.wfile.write(bytes('\t\t"model": "'+ results["model"]+'"\n\t}\n}', "utf-8"))
#-------裁票機開/關機---------------------------------------------
        if change == "b":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes('{\n\t"events": "'+events+'",\n', "utf-8"))
            self.wfile.write(bytes('\t"timestamp": "'+str(timestamp) +'",\n', "utf-8"))
            self.wfile.write(bytes('\t"source": {\n', "utf-8"))
            self.wfile.write(bytes('\t\t"_id": '+ str(source["_id"])+',\n', "utf-8"))
            self.wfile.write(bytes('\t\t"position ": "'+ str(source["position"])+'"\n\t}\n}', "utf-8"))
        '''self.wfile.write(bytes("<html><body><script>HELLO WORD</h1></body></html>", "utf-8"))'''

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        '''date = time.strftime("%Y-%m %H:%M:", time.localtime(time.time()))
        self.wfile.write(bytes('{"time":"'+ date +'"}', "utf-8"))'''
change = input("請輸入你要的模式，查詢單一機台資訊請按a，裁票機開/關機請按b")
server = HTTPServer((HOST, PORT), NeuralHttp)
print ("Server now running...")
server.serve_forever()
server.server_close()
print ("Server stopped...")

