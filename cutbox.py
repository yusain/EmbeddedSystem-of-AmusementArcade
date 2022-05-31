# 這是有會員加點(QR Code)與非會員加點(熱感紙)的功能
from operator import truediv
import tkinter as tk
import tkinter.font as tkFont

win = tk.Tk()
win.geometry("1000x450+200+50")
win.minsize(width=1000,height=450)
win.maxsize(width=1000,height=450)
win.title("cutbox")
win.config(bg="#CCEEFF")
ticket = 0
#-------副函式--------------------------
def ok():
    t = ticket_entry.get()
    global ticket
    ticket = t
    #source["count"] = t
    if t == "" :
        ticket_amount.config(text=0)
    else :
        ticket_amount.config(text=t)


#--------參數---------------------------
ticket_access = 0





#--------第一階段--------------------------------------------------
ticket_amount_op = tk.Label(bg="#33CCFF" ,text="請輸入彩票數量",font=('Arial', 25),borderwidth = 1,relief="solid",width=15)
ticket_entry = tk.Entry(font=('Arial', 25),width=15)
ticket_name = tk.Label(bg="#33CCFF" ,text="讀取到的彩票數量",font=('Arial', 25),borderwidth = 1,relief="solid",width=15)
ticket_amount = tk.Label(bg="#33CCFF" ,text=0,font=('Arial', 25),borderwidth = 1,relief="solid",width=14)  
printf_button = tk.Button(bg="#33CCFF",text="印出",font=('Arial', 20),command=ok,width=12)
ticket_amount_op.grid(row=0, column=0)
ticket_entry.grid(row=0, column=1)
ticket_name.grid(row=1, column=0)
ticket_amount.grid(row=1, column=1)
printf_button.grid(row=2, column=0,columnspan=2)
#輸入你要的模式
change = input("你是Line會員嗎，是請按a，不是請按b: ")
win.mainloop()




#--------------------------------------------------
from email import message
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import sys
import json
from turtle import delay
from unittest import result
HOST = "192.168.1.101"
PORT = 9999
timestamp = 1653457092123
#-------讀取json檔的資料----------------------------------------
with open('cutbox.json','r',encoding='utf-8') as file:
    cutbox_string = json.load(file)
cutbox_string['會員加點(QR Code)']['source']['count'] = ticket
cutbox_string['非會員加點(熱感紙)']['source']['count'] = ticket
#------------------------------------------------------------
class NeuralHttp(BaseHTTPRequestHandler):
    def do_GET(self):
        if change == "a":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(cutbox_string['會員加點(QR Code)']), "utf-8"))
        if change == "b":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(str(cutbox_string['非會員加點(熱感紙)']), "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
server = HTTPServer((HOST, PORT), NeuralHttp)
print ("Server now running...")
server.serve_forever()
server.server_close()
print ("Server stopped...")


