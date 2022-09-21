import tkinter as tk 
import tkinter.font as tkFont
import http.client
import pprint
import json
import sys
import requests
win = tk.Tk()
win.geometry("1000x450+200+50")
win.minsize(width=1000,height=450)
win.maxsize(width=1000,height=450)
win.config(bg="#CCEEFF")
#設定
conn = http.client.HTTPConnection("163.13.133.185", port=80) 
headers = {'Content-type': 'application/json'}

#-------副函式--------------------------
def ok():
    t = ticket_entry.get()
    if t == "" :
        ticket_amount.config(text=0)
    else :
        ticket_amount.config(text=t)
        #包裝
        foo = {'裁票量':'{}'.format(t)}
        json_data = json.dumps(foo)
        #格式
        conn.request('POST', '/post', json_data, headers)
        r1 = conn.getresponse()
        print(r1.read().decode())   
        conn.close()

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

#包裝
foo = {'麻煩':'開機'}
json_data = json.dumps(foo)
#格式
conn.request('POST', '/post', json_data, headers)
r1 = conn.getresponse()
print(r1.read().decode())   
conn.close()

win.mainloop()