import tkinter as tk 
import tkinter.font as tkFont
import random

#--------隱藏登入顯示票數和禮品-------------------------------------------
def ok():
   #隱藏開始鍵
   start_button.place_forget()
   
   ticket.place(x=0,y=0)
   total_button.place(x=100,y=0)
   break_start_button.place(x=200,y=0)
   #禮品一號位置
   box1.place(x=0,y=80)
   box1_ticket.place(x=93,y=80)
   box1_amount_bug.place(x=120,y=80)
   box1_add_button.place(x=143,y=80)
   box1_sub_button.place(x=173,y=80)
   box1_amount.place(x=205,y=80)
   #禮品二號位置
   box2.place(x=0,y=160)
   box2_ticket.place(x=93,y=160)
   box2_amount_bug.place(x=120,y=160)
   box2_add_button.place(x=143,y=160)
   box2_sub_button.place(x=173,y=160)
   box2_amount.place(x=205,y=160)
   #禮品三號位置
   box3.place(x=0,y=240)
   box3_ticket.place(x=93,y=240)
   box3_amount_bug.place(x=120,y=240)
   box3_add_button.place(x=143,y=240)
   box3_sub_button.place(x=173,y=240)
   box3_amount.place(x=205,y=240)
#--------返回登入畫面-----------------------------
def gostart():

   #-----重置禮品數-----------
   global box1_box_amount
   global box2_box_amount
   global box3_box_amount
   box1_box_amount = 0
   box2_box_amount = 0
   box3_box_amount = 0
   box1_amount_bug.config(text=box1_box_amount)
   box2_amount_bug.config(text=box2_box_amount)
   box3_amount_bug.config(text=box3_box_amount)
   #隱藏第二階段的物件
   ticket.place_forget()
   total_button.place_forget()
   break_start_button.place_forget()
   
   box1.place_forget()
   box1_ticket.place_forget()
   box1_amount_bug.place_forget()
   box1_add_button.place_forget()
   box1_sub_button.place_forget()
   box1_amount.place_forget()
   box2.place_forget()
   box2_ticket.place_forget()
   box2_amount_bug.place_forget()
   box2_add_button.place_forget()
   box2_sub_button.place_forget()
   box2_amount.place_forget()
   box3.place_forget()
   box3_ticket.place_forget()
   box3_amount_bug.place_forget()
   box3_add_button.place_forget()
   box3_sub_button.place_forget()
   box3_amount.place_forget()
   #顯示開始鍵
   start_button.place(x=180,y=120)
#--------進入結算隱藏票數和禮品-------------------------------------------

def ok2():
   global total_ticket
   global last_ticket
   global myticket
   #禮品一號
   global box1_end_buy
   global box1_ticket_end_buy
   #禮品二號
   global box2_end_buy
   global box2_ticket_end_buy
   #禮品三號
   global box3_end_buy
   global box3_ticket_end_buy
   #隱藏第二階段
   ticket.place_forget()
   total_button.place_forget()
   break_start_button.place_forget()
   #禮品一號
   box1.place_forget()
   box1_ticket.place_forget()
   box1_amount_bug.place_forget()
   box1_add_button.place_forget()
   box1_sub_button.place_forget()
   box1_amount.place_forget()
   #禮品二號
   box2.place_forget()
   box2_ticket.place_forget()
   box2_amount_bug.place_forget()
   box2_add_button.place_forget()
   box2_sub_button.place_forget()
   box2_amount.place_forget()
   #禮品三號
   box3.place_forget()
   box3_ticket.place_forget()
   box3_amount_bug.place_forget()
   box3_add_button.place_forget()
   box3_sub_button.place_forget()
   box3_amount.place_forget()
   #存取購買的數量
   box1_end_buy = box1_box_amount
   box2_end_buy = box2_box_amount
   box3_end_buy = box3_box_amount
   #結算畫面
   ticket.place(x=0,y=200)
   total_ticket_buy_end.place(x=125,y=200)
   ticket_last.place(x=220,y=200)
   change_button.place(x=240,y=100)
   break_2_button.place(x=360,y=0)
   #禮品一號位置
   box1_end.place(x=0,y=0)
   box1_amount_bug_end.place(x=95,y=0)
   box1_ticket_bug_end.place(x=125,y=0)

   box1_ticket_end_buy = box1_end_buy * 5
   box1_ticket_bug_end.config(text=box1_ticket_end_buy)
   box1_amount_bug_end.config(text=box1_end_buy)

   #禮品二號位置
   box2_end.place(x=0,y=30)
   box2_amount_bug_end.place(x=95,y=30)
   box2_ticket_bug_end.place(x=125,y=30)

   box2_ticket_end_buy = box2_end_buy * 12
   box2_ticket_bug_end.config(text=box2_ticket_end_buy)
   box2_amount_bug_end.config(text=box2_end_buy)

   #禮品三號位置
   box3_end.place(x=0,y=60)
   box3_amount_bug_end.place(x=95,y=60)
   box3_ticket_bug_end.place(x=125,y=60)

   box3_ticket_end_buy = box3_end_buy * 100
   box3_ticket_bug_end.config(text=box3_ticket_end_buy)
   box3_amount_bug_end.config(text=box3_end_buy)

   #總結
   total_ticket = box1_ticket_end_buy + box2_ticket_end_buy +box3_ticket_end_buy
   total_ticket_buy_end.config(text=total_ticket)
   #餘額
   last_ticket = myticket - total_ticket
   ticket_last.config(text=last_ticket)



#----------返回第二步驟-------------------
def go2():
   #隱藏結算畫面
   ticket.place_forget()
   total_ticket_buy_end.place_forget()
   ticket_last.place_forget()
   change_button.place_forget()
   break_2_button.place_forget()
   #隱藏一號禮品位置
   box1_end.place_forget()
   box1_amount_bug_end.place_forget()
   box1_ticket_bug_end.place_forget()
   #隱藏二號禮品位置
   box2_end.place_forget()
   box2_amount_bug_end.place_forget()
   box2_ticket_bug_end.place_forget()
   #隱藏三號禮品位置
   box3_end.place_forget()
   box3_amount_bug_end.place_forget()
   box3_ticket_bug_end.place_forget()
   ticket.place(x=0,y=0)
   total_button.place(x=100,y=0)
   break_start_button.place(x=200,y=0)
   
   #禮品一號位置
   box1.place(x=0,y=80)
   box1_ticket.place(x=93,y=80)
   box1_amount_bug.place(x=120,y=80)
   box1_add_button.place(x=143,y=80)
   box1_sub_button.place(x=173,y=80)
   box1_amount.place(x=205,y=80)
   #禮品二號位置
   box2.place(x=0,y=160)
   box2_ticket.place(x=93,y=160)
   box2_amount_bug.place(x=120,y=160)
   box2_add_button.place(x=143,y=160)
   box2_sub_button.place(x=173,y=160)
   box2_amount.place(x=205,y=160)
   #禮品三號位置
   box3.place(x=0,y=240)
   box3_ticket.place(x=93,y=240)
   box3_amount_bug.place(x=120,y=240)
   box3_add_button.place(x=143,y=240)
   box3_sub_button.place(x=173,y=240)
   box3_amount.place(x=205,y=240)

win = tk.Tk()
win.geometry("480x360+400+200")
win.minsize(width=480,height=360)
win.maxsize(width=480,height=360)
#--------------禮品一號--------------------
box1_end_buy = 0 #最後購買的實際數量
box1_ticket_end_buy = 0 #最後購買的實際總票數
box1_box_amount = 0
box1_box = 20
def box1_add_button():
    global box1_box_amount
    global box1_box
    if box1_box_amount < box1_box :
      box1_box_amount+=1
      box1_amount_bug.config(text=box1_box_amount)
def box1_sub_button():
    global box1_box_amount
    if 0 < box1_box_amount :
      box1_box_amount-=1
      box1_amount_bug.config(text=box1_box_amount)
#--------------禮品二號--------------------
box2_end_buy = 0 
box2_ticket_end_buy = 0
box2_box = 12
box2_box_amount = 0
def box2_add_button():
    global box2_box_amount
    global box2_box
    if box2_box_amount < box2_box :
      box2_box_amount+=1
      box2_amount_bug.config(text=box2_box_amount)
def box2_sub_button():
    global box2_box_amount
    if 0 < box2_box_amount :
      box2_box_amount-=1
      box2_amount_bug.config(text=box2_box_amount)
#--------------禮品三號--------------------
box3_end_buy = 0 
box3_ticket_end_buy = 0
box3_box = 5
box3_box_amount = 0
def box3_add_button():
    global box3_box_amount
    global box3_box
    if box3_box_amount < box3_box :
      box3_box_amount+=1
      box3_amount_bug.config(text=box3_box_amount)
def box3_sub_button():
    global box3_box_amount
    if 0 < box3_box_amount :
      box3_box_amount-=1
      box3_amount_bug.config(text=box3_box_amount)

#---------------最後兌換----------------------
   
def goend():
   global myticket
   global last_ticket
   global total_ticket
   if last_ticket >= 0 and total_ticket > 0:
      myticket = last_ticket
      ticket.config(text=myticket)
      #禮品一號
      global box1_box
      global box1_end_buy
      box1_box-=box1_end_buy
      box1_amount.config(text=box1_box)
      #禮品一號位置隱藏
      box1_end.place_forget()
      box1_amount_bug_end.place_forget()
      box1_ticket_bug_end.place_forget()
      #-----重置禮品數-----------
      global box1_box_amount
      box1_box_amount = 0
      box1_amount_bug.config(text=box1_box_amount)
      #禮品二號
      global box2_box
      global box2_end_buy
      box2_box-=box2_end_buy
      box2_amount.config(text=box2_box)
      #禮品二號位置隱藏
      box2_end.place_forget()
      box2_amount_bug_end.place_forget()
      box2_ticket_bug_end.place_forget()
      #-----重置禮品數-----------
      global box2_box_amount
      box2_box_amount = 0
      box2_amount_bug.config(text=box2_box_amount)
      #禮品三號
      global box3_box
      global box3_end_buy
      box3_box-=box3_end_buy
      box3_amount.config(text=box3_box)
      #禮品三號位置隱藏
      box3_end.place_forget()
      box3_amount_bug_end.place_forget()
      box3_ticket_bug_end.place_forget()
      start_button.place(x=180,y=120)
      #-----重置禮品數-----------
      global box3_box_amount
      box3_box_amount = 0
      box3_amount_bug.config(text=box3_box_amount)
      #結算畫面隱藏
      ticket.place_forget()
      total_ticket_buy_end.place_forget()
      ticket_last.place_forget()
      change_button.place_forget()
      break_2_button.place_forget()
             
#--------登入--------------------------------------------------
start_button = tk.Button(text="start",bg="#33FF33",width=10,height=5,font="1",command=ok)
start_button.place(x=180,y=120)
#--------票數和禮品------------------------------------------------
myticket = 500
ticket = tk.Label(bg="#0066FF",text=myticket,font="40",width=8,height=1)
#--------總結------------------------------------------------------
total_button = tk.Button(text="總結",bg="#FF5511",width=3,height=2,font="1",command=ok2)
#--------返回------------------------------------------------------
break_start_button = tk.Button(text="返回",bg="#FF5511",width=3,height=2,font="1",command=gostart)
#禮品一號
box1 = tk.Label(bg="#0066FF",text="禮品一號",font="40",width=8,height=1)
box1_ticket = tk.Label(bg="#0066FF",text=5,font="40",width=2,height=1)
box1_amount_bug = tk.Label(bg="#FF5511",text=0,font="40",width=2,height=1)
box1_add_button = tk.Button(bg="#0066FF",text="+",font="1",width=2,height=1,command=box1_add_button)
box1_sub_button = tk.Button(bg="#0066FF",text="-",font="1",width=2,height=1,command=box1_sub_button)
box1_amount = tk.Label(bg="#FF5511",text=box1_box,font="40",width=2,height=1)
#禮品二號
box2 = tk.Label(bg="#0066FF",text="禮品一號",font="40",width=8,height=1)
box2_ticket = tk.Label(bg="#0066FF",text=12,font="40",width=2,height=1)
box2_amount_bug = tk.Label(bg="#FF5511",text=0,font="40",width=2,height=1)
box2_add_button = tk.Button(bg="#0066FF",text="+",font="1",width=2,height=1,command=box2_add_button)
box2_sub_button = tk.Button(bg="#0066FF",text="-",font="1",width=2,height=1,command=box2_sub_button)
box2_amount = tk.Label(bg="#FF5511",text=box2_box,font="40",width=2,height=1)
#禮品三號
box3 = tk.Label(bg="#0066FF",text="禮品一號",font="40",width=8,height=1)
box3_ticket = tk.Label(bg="#0066FF",text=100,font="40",width=2,height=1)
box3_amount_bug = tk.Label(bg="#FF5511",text=0,font="40",width=2,height=1)
box3_add_button = tk.Button(bg="#0066FF",text="+",font="1",width=2,height=1,command=box3_add_button)
box3_sub_button = tk.Button(bg="#0066FF",text="-",font="1",width=2,height=1,command=box3_sub_button)
box3_amount = tk.Label(bg="#FF5511",text=box3_box,font="40",width=2,height=1)

#--------結算畫面---------------------------------------------------------------
#禮品一號
box1_end = tk.Label(bg="#0066FF",text="禮品一號",font="40",width=8,height=1)
box1_amount_bug_end = tk.Label(bg="#FF5511",text=box1_end_buy,font="40",width=2,height=1)
box1_ticket_end_buy = box1_end_buy * 5
box1_ticket_bug_end = tk.Label(bg="#0066FF",text=box1_ticket_end_buy,font="40",width=8,height=1)
#禮品二號
box2_end = tk.Label(bg="#0066FF",text="禮品二號",font="40",width=8,height=1)
box2_amount_bug_end = tk.Label(bg="#FF5511",text=box2_end_buy,font="40",width=2,height=1)
box2_ticket_end_buy = box2_end_buy * 5
box2_ticket_bug_end = tk.Label(bg="#0066FF",text=box2_ticket_end_buy,font="40",width=8,height=1)
#禮品三號
box3_end = tk.Label(bg="#0066FF",text="禮品三號",font="40",width=8,height=1)
box3_amount_bug_end = tk.Label(bg="#FF5511",text=box3_end_buy,font="40",width=2,height=1)
box3_ticket_end_buy = box3_end_buy * 5
box3_ticket_bug_end = tk.Label(bg="#0066FF",text=box3_ticket_end_buy,font="40",width=8,height=1)
#返回鍵
break_2_button = tk.Button(text="返回",bg="#FF5511",width=3,height=2,font="1",command=go2)
#總計票數
total_ticket = 0
total_ticket_buy_end = tk.Label(bg="#0066FF",text=total_ticket,font="40",width=8,height=1)
#剩餘票數
last_ticket = 0
ticket_last = tk.Label(bg="#FF5511",text=last_ticket,font="40",width=8,height=1)
#確定更換
change_button = tk.Button(bg="#0066FF",text="確定更換",font="1",width=8,height=2,command=goend)
win.mainloop()