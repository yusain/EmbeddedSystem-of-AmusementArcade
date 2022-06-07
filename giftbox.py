import tkinter as tk 
import tkinter.font as tkFont
import random
import http.client
import pprint
import json
import sys
import requests
#設定
conn = http.client.HTTPConnection("163.13.133.185", port=80) 
headers = {'Content-type': 'application/json'}

#--------隱藏登入顯示票數和禮品-------------------------------------------
def ok():
   #包裝
   foo = {'登入狀況':'登入'}
   json_data = json.dumps(foo)
   #格式
   conn.request('POST', '/post', json_data, headers)
   r1 = conn.getresponse()
   print(r1.read().decode())   
   conn.close()
   #隱藏開始鍵
   start_button.place_forget()
   break_start_button.grid(row=0, column=0,columnspan=2,sticky=tk.E+tk.W)
   blue_box.grid(row=0, column=2,columnspan=3,sticky=tk.E+tk.W+tk.S+tk.N)
   change_button.grid(row=0, column=5,columnspan=2,sticky=tk.E+tk.W)
   #禮品介紹的位置
   box_op.grid(row=1, column=0, sticky=tk.E+tk.W)
   box_ticket_op.grid(row=1, column=1, sticky=tk.E+tk.W)
   box_amount_bug_op.grid(row=1, column=2, sticky=tk.E+tk.W)
   box_add_butto_op.grid(row=1, column=3)
   box_sub_button_op.grid(row=1, column=4)
   box_amount_op.grid(row=1, column=5, sticky=tk.E+tk.W)
   box_ticket_bug_end_op.grid(row=1, column=6, sticky=tk.E+tk.W)
   #禮品一號位置
   box1.grid(row=2, column=0, sticky=tk.E+tk.W)
   box1_ticket.grid(row=2, column=1, sticky=tk.E+tk.W)
   box1_amount_bug.grid(row=2, column=2, sticky=tk.E+tk.W)
   box1_add_button.grid(row=2, column=3, sticky=tk.E+tk.W)
   box1_sub_button.grid(row=2, column=4, sticky=tk.E+tk.W)
   box1_amount.grid(row=2, column=5, sticky=tk.E+tk.W)
   box1_ticket_bug_end.grid(row=2, column=6, sticky=tk.E+tk.W)
   #禮品二號位置
   box2.grid(row=3, column=0, sticky=tk.E+tk.W)
   box2_ticket.grid(row=3, column=1, sticky=tk.E+tk.W)
   box2_amount_bug.grid(row=3, column=2, sticky=tk.E+tk.W)
   box2_add_button.grid(row=3, column=3, sticky=tk.E+tk.W+tk.S+tk.N)
   box2_sub_button.grid(row=3, column=4, sticky=tk.E+tk.W+tk.S+tk.N)
   box2_amount.grid(row=3, column=5, sticky=tk.E+tk.W)
   box2_ticket_bug_end.grid(row=3, column=6, sticky=tk.E+tk.W)
   #禮品三號位置
   box3.grid(row=4, column=0, sticky=tk.E+tk.W)
   box3_ticket.grid(row=4, column=1, sticky=tk.E+tk.W)
   box3_amount_bug.grid(row=4, column=2, sticky=tk.E+tk.W)
   box3_add_button.grid(row=4, column=3, sticky=tk.E+tk.W+tk.S+tk.N)
   box3_sub_button.grid(row=4, column=4, sticky=tk.E+tk.W+tk.S+tk.N)
   box3_amount.grid(row=4, column=5, sticky=tk.E+tk.W)
   box3_ticket_bug_end.grid(row=4, column=6, sticky=tk.E+tk.W)
   #擁有票數，所需總票數，剩餘票數介面
   ticket_op2.grid(row=5, column=0,columnspan=2,sticky=tk.E+tk.W)
   buy_ticket_op2.grid(row=5, column=2,columnspan=3,sticky=tk.E+tk.W) 
   last_ticket_op2.grid(row=5, column=5,columnspan=2,sticky=tk.E+tk.W)
   #擁有票數，所需總票數，剩餘票數數值
   ticket.grid(row=6, column=0,columnspan=2,sticky=tk.E+tk.W)
   total_ticket_buy_end.grid(row=6, column=2,columnspan=3,sticky=tk.E+tk.W)
   ticket_last.grid(row=6, column=5,columnspan=2,sticky=tk.E+tk.W)
#--------返回登入畫面-----------------------------
def gostart():

   #包裝
   foo = {'登入狀況':'登出'}
   json_data = json.dumps(foo)
   #格式
   conn.request('POST', '/post', json_data, headers)
   r1 = conn.getresponse()
   print(r1.read().decode())   
   conn.close()
   total_ticket_buy_end.config(text=0)
   global myticket
   ticket_last.config(text=myticket)
   #禮品一號-----重置禮品數，所需票數-----------
   global box1_box_amount
   global box1_ticket_end_buy
   box1_ticket_end_buy = 0
   box1_box_amount = 0
   box1_amount_bug.config(text=0)
   box1_ticket_bug_end.config(text=0)
   #禮品二號-----重置禮品數，所需票數-----------
   global box2_box_amount
   global box2_ticket_end_buy
   box2_ticket_end_buy = 0
   box2_box_amount = 0
   box2_amount_bug.config(text=0)
   box2_ticket_bug_end.config(text=0)
   #禮品三號-----重置禮品數，所需票數-----------
   global box3_box_amount
   global box3_ticket_end_buy
   box3_ticket_end_buy = 0
   box3_box_amount = 0
   box3_amount_bug.config(text=0)
   box3_ticket_bug_end.config(text=0)
   #結算畫面隱藏
   break_start_button.grid_forget()
   change_button.grid_forget()
   #禮品介紹的位置隱藏
   box_op.grid_forget()
   box_ticket_op.grid_forget()
   box_amount_bug_op.grid_forget()
   box_add_butto_op.grid_forget()
   box_sub_button_op.grid_forget()
   box_amount_op.grid_forget()
   box_ticket_bug_end_op.grid_forget()
   #禮品一號位置隱藏
   box1.grid_forget()
   box1_ticket.grid_forget()
   box1_amount_bug.grid_forget()
   box1_add_button.grid_forget()
   box1_sub_button.grid_forget()
   box1_amount.grid_forget()
   box1_ticket_bug_end.grid_forget()
   #禮品二號位置隱藏
   box2.grid_forget()
   box2_ticket.grid_forget()
   box2_amount_bug.grid_forget()
   box2_add_button.grid_forget()
   box2_sub_button.grid_forget()
   box2_amount.grid_forget()
   box2_ticket_bug_end.grid_forget()
   #禮品三號位置隱藏
   box3.grid_forget()
   box3_ticket.grid_forget()
   box3_amount_bug.grid_forget()
   box3_add_button.grid_forget()
   box3_sub_button.grid_forget()
   box3_amount.grid_forget()
   box3_ticket_bug_end.grid_forget()
   #擁有票數，所需總票數，剩餘票數介面隱藏
   ticket_op2.grid_forget()
   buy_ticket_op2.grid_forget()
   last_ticket_op2.grid_forget()
   #擁有票數，所需總票數，剩餘票數數值隱藏
   ticket.grid_forget()
   total_ticket_buy_end.grid_forget()
   ticket_last.grid_forget()
   start_button.place(relwidth=1, relheight=1)
#-------------------GUI-----------------------------
win = tk.Tk()
win.geometry("1000x450+200+50")
win.minsize(width=1000,height=450)
win.maxsize(width=1000,height=450)
win.config(bg="#CCEEFF")

#--------------禮品一號--------------------
box1_ticket_end_buy = 0 #最後購買的實際總票數
box1_box_amount = 0 #最後購買的實際數量
box1_box = 20

def box1_add_button():
   global box1_box_amount
   global box1_box
   global box1_ticket_end_buy
   if box1_box_amount < box1_box :
      box1_box_amount+=1
      box1_amount_bug.config(text=box1_box_amount)
      box1_ticket_end_buy = box1_box_amount * 5
      box1_ticket_bug_end.config(text=box1_ticket_end_buy)
      total_account()
def box1_sub_button():
   global box1_box_amount
   global box1_ticket_end_buy
   if 0 < box1_box_amount :
      box1_box_amount-=1
      box1_amount_bug.config(text=box1_box_amount)
      box1_ticket_end_buy = box1_box_amount * 5
      box1_ticket_bug_end.config(text=box1_ticket_end_buy)
      total_account()
#--------------禮品二號--------------------
box2_end_buy = 0 
box2_ticket_end_buy = 0
box2_box = 12
box2_box_amount = 0
def box2_add_button():
   global box2_box_amount
   global box2_box
   global box2_ticket_end_buy
   if box2_box_amount < box2_box :
      box2_box_amount+=1
      box2_amount_bug.config(text=box2_box_amount)
      box2_ticket_end_buy = box2_box_amount * 12
      box2_ticket_bug_end.config(text=box2_ticket_end_buy)
      total_account()
def box2_sub_button():
   global box2_box_amount
   global box2_ticket_end_buy
   if 0 < box2_box_amount :
      box2_box_amount-=1
      box2_amount_bug.config(text=box2_box_amount)
      box2_ticket_end_buy = box2_box_amount * 12
      box2_ticket_bug_end.config(text=box2_ticket_end_buy)
      total_account()
#--------------禮品三號--------------------
box3_end_buy = 0 
box3_ticket_end_buy = 0
box3_box = 5
box3_box_amount = 0
def box3_add_button():
   global box3_box_amount
   global box3_box
   global box3_ticket_end_buy
   if box3_box_amount < box3_box :
      box3_box_amount+=1
      box3_amount_bug.config(text=box3_box_amount)
      box3_ticket_end_buy = box3_box_amount * 100
      box3_ticket_bug_end.config(text=box3_ticket_end_buy)
      total_account()
def box3_sub_button():
   global box3_box_amount
   global box3_ticket_end_buy
   if 0 < box3_box_amount :
      box3_box_amount-=1
      box3_amount_bug.config(text=box3_box_amount)
      box3_ticket_end_buy = box3_box_amount * 100
      box3_ticket_bug_end.config(text=box3_ticket_end_buy)
      total_account()
#---------------計算所需總票數，剩餘票數------------------
total_ticket = 0
last_ticket = 0
def total_account():
   global box1_ticket_end_buy
   global box2_ticket_end_buy
   global box3_ticket_end_buy
   global myticket
   global last_ticket
   global total_ticket
   #總結
   total_ticket = box1_ticket_end_buy + box2_ticket_end_buy + box3_ticket_end_buy
   total_ticket_buy_end.config(text=total_ticket)
   #餘額
   last_ticket = myticket - total_ticket
   ticket_last.config(text=last_ticket)

#---------------最後兌換----------------------
   
def goend():
   global myticket
   global last_ticket
   global total_ticket
   global box1_ticket_end_buy
   global box2_ticket_end_buy
   global box3_ticket_end_buy

   box1_ticket_end_buy = 0
   box1_amount_bug.config(text=0)
   box2_ticket_end_buy = 0
   box2_amount_bug.config(text=0)
   box3_ticket_end_buy = 0
   box3_amount_bug.config(text=0)
   if last_ticket >= 0 and total_ticket > 0:
      global box1_box
      global box1_box_amount
      global box2_box
      global box2_box_amount
      global box3_box
      global box3_box_amount
      #包裝
      foo = {'彩票數量狀況':'使用了{}張彩票'.format(total_ticket),'禮品一號':'減少{}'.format(box1_box_amount),'禮品二號':'減少{}'.format(box2_box_amount),'禮品三號':'減少{}'.format(box3_box_amount)}
      json_data = json.dumps(foo)
      #格式
      conn.request('POST', '/post', json_data, headers)
      r1 = conn.getresponse()
      print(r1.read().decode())   
      conn.close()
      total_ticket = 0
      myticket = last_ticket
      ticket.config(text=myticket)
      total_ticket_buy_end.config(text=0)
      #禮品一號
      box1_box-=box1_box_amount
      box1_amount.config(text=box1_box)
      #-----重置禮品數，所需票數-----------
      box1_box_amount = 0
      box1_amount_bug.config(text=box1_box_amount)
      box1_ticket_bug_end.config(text=0)
      #禮品二號
      box2_box-=box2_box_amount
      box2_amount.config(text=box2_box)
      #-----重置禮品數，所需票數-----------
      box2_box_amount = 0
      box2_amount_bug.config(text=box2_box_amount)
      box2_ticket_bug_end.config(text=0)
      #禮品三號
      box3_box-=box3_box_amount
      box3_amount.config(text=box3_box)
      #-----重置禮品數所需票數-----------
      box3_box_amount = 0
      box3_amount_bug.config(text=box3_box_amount)
      box3_ticket_bug_end.config(text=0)
      
      #結算畫面隱藏
      break_start_button.grid_forget()
      change_button.grid_forget()
      #禮品介紹的位置隱藏
      box_op.grid_forget()
      box_ticket_op.grid_forget()
      box_amount_bug_op.grid_forget()
      box_add_butto_op.grid_forget()
      box_sub_button_op.grid_forget()
      box_amount_op.grid_forget()
      box_ticket_bug_end_op.grid_forget()
      #禮品一號位置隱藏
      box1.grid_forget()
      box1_ticket.grid_forget()
      box1_amount_bug.grid_forget()
      box1_add_button.grid_forget()
      box1_sub_button.grid_forget()
      box1_amount.grid_forget()
      box1_ticket_bug_end.grid_forget()
      #禮品二號位置隱藏
      box2.grid_forget()
      box2_ticket.grid_forget()
      box2_amount_bug.grid_forget()
      box2_add_button.grid_forget()
      box2_sub_button.grid_forget()
      box2_amount.grid_forget()
      box2_ticket_bug_end.grid_forget()
      #禮品三號位置隱藏
      box3.grid_forget()
      box3_ticket.grid_forget()
      box3_amount_bug.grid_forget()
      box3_add_button.grid_forget()
      box3_sub_button.grid_forget()
      box3_amount.grid_forget()
      box3_ticket_bug_end.grid_forget()
      #擁有票數，所需總票數，剩餘票數介面隱藏
      ticket_op2.grid_forget()
      buy_ticket_op2.grid_forget()
      last_ticket_op2.grid_forget()
      #擁有票數，所需總票數，剩餘票數數值隱藏
      ticket.grid_forget()
      total_ticket_buy_end.grid_forget()
      ticket_last.grid_forget()
      start_button.place(relwidth=1, relheight=1)
      
#填滿
blue_box = tk.Label(bg="#00BBFF",text=" ",font=('Arial', 25))
#--------登入--------------------------------------------------
start_button = tk.Button(text="登入",bg="#33CCFF",width=10,height=5,font=('Arial', 70),command=ok)
start_button.place(relwidth=1, relheight=1)
#--------票數和禮品------------------------------------------------
myticket = 500
ticket = tk.Label(bg="#CCEEFF",text=myticket,font=('Arial', 25),borderwidth = 1,relief="solid")
#--------返回------------------------------------------------------
break_start_button = tk.Button(text="返回",bg="#00BBFF",font=('Arial', 25),command=gostart)
#禮品標題 
box_op = tk.Label(bg="#33CCFF",text="    商品名稱    ",font=('Arial', 25),borderwidth = 1,relief="solid")
box_ticket_op = tk.Label(bg="#33CCFF",text="  兌換票數  ",font=('Arial', 25),borderwidth = 1,relief="solid")
box_amount_bug_op = tk.Label(bg="#33CCFF",text="  選擇數量  ",font=('Arial', 25),borderwidth = 1,relief="solid")
box_add_butto_op = tk.Label(bg="#33CCFF",text="增",font=('Arial', 25),borderwidth = 1,relief="solid")
box_sub_button_op = tk.Label(bg="#33CCFF",text="減",font=('Arial', 25),borderwidth = 1,relief="solid")
box_amount_op = tk.Label(bg="#33CCFF",text="  禮品數量  ",font=('Arial', 25),borderwidth = 1,relief="solid")
box_ticket_bug_end_op = tk.Label(bg="#33CCFF",text="  所需票數  ",font=('Arial', 25),borderwidth = 1,relief="solid")

#禮品一號
box1 = tk.Label(bg="#CCEEFF",text="  禮品一號  ",font=('Arial', 25),borderwidth = 1,relief="solid")
box1_ticket = tk.Label(bg="#CCEEFF",text=5,font=('Arial', 25),borderwidth = 1,relief="solid")
box1_amount_bug = tk.Label(bg="#CCEEFF",text=0,font=('Arial', 25),borderwidth = 1,relief="solid")
box1_add_button = tk.Button(bg="#CCEEFF",text="+",font=('Arial', 16),command=box1_add_button)
box1_sub_button = tk.Button(bg="#CCEEFF",text="-",font=('Arial', 16),command=box1_sub_button)
box1_amount = tk.Label(bg="#CCEEFF",text=box1_box,font=('Arial', 25),borderwidth = 1,relief="solid")
#禮品二號
box2 = tk.Label(bg="#33CCFF",text="  禮品二號  ",font=('Arial', 25),borderwidth = 1,relief="solid")
box2_ticket = tk.Label(bg="#33CCFF",text=12,font=('Arial', 25),borderwidth = 1,relief="solid")
box2_amount_bug = tk.Label(bg="#33CCFF",text=0,font=('Arial', 25),borderwidth = 1,relief="solid")
box2_add_button = tk.Button(bg="#33CCFF",text="+",font=('Arial', 16),command=box2_add_button)
box2_sub_button = tk.Button(bg="#33CCFF",text="-",font=('Arial', 16),command=box2_sub_button)
box2_amount = tk.Label(bg="#33CCFF",text=box2_box,font=('Arial', 25),borderwidth = 1,relief="solid")
#禮品三號
box3 = tk.Label(bg="#CCEEFF",text="  禮品三號  ",font=('Arial', 25),borderwidth = 1,relief="solid")
box3_ticket = tk.Label(bg="#CCEEFF",text=100,font=('Arial', 25),borderwidth = 1,relief="solid")
box3_amount_bug = tk.Label(bg="#CCEEFF",text=0,font=('Arial', 25),borderwidth = 1,relief="solid")
box3_add_button = tk.Button(bg="#CCEEFF",text="+",font=('Arial', 16),command=box3_add_button)
box3_sub_button = tk.Button(bg="#CCEEFF",text="-",font=('Arial', 16),command=box3_sub_button)
box3_amount = tk.Label(bg="#CCEEFF",text=box3_box,font=('Arial', 25),borderwidth = 1,relief="solid")
#擁有票數，所需總票數，剩餘票數
ticket_op2 = tk.Label(bg="#33CCFF",text="擁有票數",font=('Arial', 25),borderwidth = 1,relief="solid")
buy_ticket_op2 = tk.Label(bg="#33CCFF",text="所需總票數",font=('Arial', 25),borderwidth = 1,relief="solid")
last_ticket_op2 = tk.Label(bg="#33CCFF",text="剩餘票數",font=('Arial', 25),borderwidth = 1,relief="solid")
#--------結算畫面---------------------------------------------------------------
#禮品一號
box1_end = tk.Label(bg="#33CCFF",text="禮品一號",font=('Arial', 25),borderwidth = 1,relief="solid")
box1_amount_bug_end = tk.Label(bg="#33CCFF",text=box1_box_amount,font=('Arial', 30),width=2,height=1)
box1_ticket_end_buy = box1_box_amount * 5
box1_ticket_bug_end = tk.Label(bg="#CCEEFF",text=box1_ticket_end_buy,font=('Arial', 25),borderwidth = 1,relief="solid")
#禮品二號
box2_end = tk.Label(bg="#33CCFF",text="禮品二號",font=('Arial', 25),borderwidth = 1,relief="solid")
box2_amount_bug_end = tk.Label(bg="#33CCFF",text=box2_end_buy,font=('Arial', 25),borderwidth = 1,relief="solid")
box2_ticket_end_buy = box2_end_buy * 5
box2_ticket_bug_end = tk.Label(bg="#33CCFF",text=box2_ticket_end_buy,font=('Arial', 25),borderwidth = 1,relief="solid")
#禮品三號
box3_end = tk.Label(bg="#33CCFF",text="禮品三號",font=('Arial', 25),borderwidth = 1,relief="solid")
box3_amount_bug_end = tk.Label(bg="#33CCFF",text=box3_end_buy,font=('Arial', 25),borderwidth = 1,relief="solid")
box3_ticket_end_buy = box3_end_buy * 5
box3_ticket_bug_end = tk.Label(bg="#CCEEFF",text=box3_ticket_end_buy,font=('Arial', 25),borderwidth = 1,relief="solid")
#總計票數
total_ticket = 0
total_ticket_buy_end = tk.Label(bg="#CCEEFF",text=total_ticket,font=('Arial', 25),borderwidth = 1,relief="solid")
#剩餘票數
last_ticket = 0
ticket_last = tk.Label(bg="#CCEEFF",text=last_ticket,font=('Arial', 25),borderwidth = 1,relief="solid")
#確定更換
change_button = tk.Button(bg="#00BBFF",text="確定更換",font=('Arial', 25),command=goend)
win.mainloop()