import tkinter as tk 
import tkinter.font as tkFont
import random
from tkinter import ttk

#--------------機台一號--------------------
coin1 = 0
startbox_1 = 0
def startbox1():
    global startbox_1
    if startbox_1 == 0 :
        startbox_1 = 1
        game1_box.config(bg="#33CCFF")
    else :
        startbox_1 = 0
        game1_box.config(bg="#FFBB66")
def coin1add(): #投幣
    global coin1
    global startbox_1
    if startbox_1 == 1 : 
        coin1+=1
        game1_coin.config(text=coin1)

def coin1sub(): #玩一場
    global coin1
    global startbox_1
    ticket1 = random.randrange(1, 100)
    if startbox_1 == 1 :
        if coin1 >= 2 :
            coin1-=2
            game1_coin.config(text=coin1)
            game1_ticket.config(text=ticket1)

def coin1break(): #退幣
    global coin1
    global startbox_1
    if startbox_1 == 1 :
        if coin1 > 0 :
            coin1 = 0
            game1_coin.config(text=coin1)
#--------------機台二號--------------------
coin2 = 0
startbox_2 = 0
def startbox2():
    global startbox_2
    if startbox_2 == 0 :
        startbox_2 = 1
        game2_box.config(bg="#CCEEFF")
    else :
        startbox_2 = 0
        game2_box.config(bg="#FFBB66")
def coin2add(): #投幣
    global coin2
    global startbox_2
    if startbox_2 == 1 : 
        coin2+=1
        game2_coin.config(text=coin2)

def coin2sub(): #玩一場
    global coin2
    global startbox_2
    ticket2 = random.randrange(1, 100)
    if startbox_2 == 1 :
        if coin2 >= 2 :
            coin2-=2
            game2_coin.config(text=coin2)
            game2_ticket.config(text=ticket2)

def coin2break(): #退幣
    global coin2
    global startbox_2
    if startbox_2 == 1 :
        if coin2 > 0 :
            coin2 = 0
            game2_coin.config(text=coin2)

#--------------機台三號--------------------
coin3 = 0
startbox_3 = 0
def startbox3():
    global startbox_3
    if startbox_3 == 0 :
        startbox_3 = 1
        game3_box.config(bg="#33CCFF")
    else :
        startbox_3 = 0
        game3_box.config(bg="#FFBB66")
def coin3add(): #投幣
    global coin3
    global startbox_3
    if startbox_3 == 1 : 
        coin3+=1
        game3_coin.config(text=coin3)

def coin3sub(): #玩一場
    global coin3
    global startbox_3
    ticket3 = random.randrange(1, 100)
    if startbox_3 == 1 :
        if coin3 >= 3 :
            coin3-=3
            game3_coin.config(text=coin3)
            game3_ticket.config(text=ticket3)

def coin3break(): #退幣
    global coin3
    global startbox_3
    if startbox_3 == 1 :
        if coin3 > 0 :
            coin3 = 0
            game3_coin.config(text=coin3)

#--------------機台四號--------------------
coin4 = 0
startbox_4 = 0
def startbox4():
    global startbox_4
    if startbox_4 == 0 :
        startbox_4 = 1
        game4_box.config(bg="#CCEEFF")
    else :
        startbox_4 = 0
        game4_box.config(bg="#FFBB66")
def coin4add(): #投幣
    global coin4
    global startbox_4
    if startbox_4 == 1 : 
        coin4+=1
        game4_coin.config(text=coin4)

def coin4sub(): #玩一場
    global coin4
    global startbox_4
    ticket4 = random.randrange(1, 100)
    if startbox_4 == 1 :
        if coin4 >= 4 :
            coin4-=4
            game4_coin.config(text=coin4)
            game4_ticket.config(text=ticket4)

def coin4break(): #退幣
    global coin4
    global startbox_4
    if startbox_4 == 1 :
        if coin4 > 0 :
            coin4 = 0
            game4_coin.config(text=coin4)

win = tk.Tk()
win.geometry("1000x450+200+50")
win.minsize(width=1000,height=450)
win.maxsize(width=1000,height=450)
win.config(bg="#CCEEFF")

#--------------機台五號--------------------
coin5 = 0
startbox_5 = 0
def startbox5():
    global startbox_5
    if startbox_5 == 0 :
        startbox_5 = 1
        game5_box.config(bg="#33CCFF")
    else :
        startbox_5 = 0
        game5_box.config(bg="#FFBB66")
def coin5add(): #投幣
    global coin5
    global startbox_5
    if startbox_5 == 1 : 
        coin5+=1
        game5_coin.config(text=coin5)

def coin5sub(): #玩一場
    global coin5
    global startbox_5
    ticket5 = random.randrange(1, 100)
    if startbox_5 == 1 :
        if coin5 >= 5 :
            coin5-=5
            game5_coin.config(text=coin5)
            game5_ticket.config(text=ticket5)

def coin5break(): #退幣
    global coin5
    global startbox_5
    if startbox_5 == 1 :
        if coin5 > 0 :
            coin5 = 0
            game5_coin.config(text=coin5)

#--------------機台介紹--------------------
gameLab_box = tk.Button(bg="#00BBFF",text="序號",font=('Arial', 30))
gameLab_coin = tk.Button(bg="#00BBFF",text="投幣數量",font=('Arial', 30))
gameLab_button = tk.Button(bg="#00BBFF",text="投幣",font=('Arial', 30))
gameLab_start = tk.Button(bg="#00BBFF",text="開始遊戲",font=('Arial', 30))
gameLab_break = tk.Button(bg="#00BBFF",text="退幣",font=('Arial', 30))
gameLab_ticket = tk.Button(bg="#00BBFF",text="彩票數量",font=('Arial', 30))
gameLab_box.grid(row=0, column=0)
gameLab_coin.grid(row=0, column=1)
gameLab_button.grid(row=0, column=2)
gameLab_start.grid(row=0, column=3)
gameLab_break.grid(row=0, column=4)
gameLab_ticket.grid(row=0, column=5)
#--------------機台一號--------------------
game1_box = tk.Button(bg="#FFBB66",text="一號",font=('Arial', 15),command=startbox1)
game1_coin = tk.Button(bg="#33CCFF",text=0,font=('Arial', 30))
game1_button = tk.Button(text="+",bg="#33CCFF",font=('Arial', 15),command=coin1add)
game1_start = tk.Button(text="遊玩",bg="#33CCFF",font=('Arial', 15),command=coin1sub)
game1_break = tk.Button(text="-",bg="#33CCFF",font=('Arial', 15),command=coin1break)
game1_ticket = tk.Button(bg="#33CCFF",text=0,font=('Arial', 30))
game1_box.grid(row=1, column=0,sticky=tk.E+tk.W+tk.N+tk.S)
game1_coin.grid(row=1, column=1,columnspan=1,sticky=tk.E+tk.W)
game1_button.grid(row=1, column=2,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game1_start.grid(row=1, column=3,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game1_break.grid(row=1, column=4,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game1_ticket.grid(row=1, column=5,columnspan=1,sticky=tk.E+tk.W)
#--------------機台二號--------------------
game2_box = tk.Button(bg="#FFBB66",text="二號",font=('Arial', 15),command=startbox2)
game2_coin = tk.Button(bg="#CCEEFF",text=0,font=('Arial', 25))
game2_button = tk.Button(text="+",bg="#CCEEFF",font=('Arial', 15),command=coin2add)
game2_start = tk.Button(text="遊玩",bg="#CCEEFF",font=('Arial', 15),command=coin2sub)
game2_break = tk.Button(text="-",bg="#CCEEFF",font=('Arial', 15),command=coin2break)
game2_ticket = tk.Button(bg="#CCEEFF",text=0,font=('Arial', 25))
game2_box.grid(row=2, column=0,sticky=tk.E+tk.W+tk.N+tk.S)
game2_coin.grid(row=2, column=1,columnspan=1,sticky=tk.E+tk.W)
game2_button.grid(row=2, column=2,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game2_start.grid(row=2, column=3,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game2_break.grid(row=2, column=4,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game2_ticket.grid(row=2, column=5,columnspan=1,sticky=tk.E+tk.W)
#--------------機台三號--------------------
game3_box = tk.Button(bg="#FFBB66",text="三號",font=('Arial', 15),command=startbox3)
game3_coin = tk.Button(bg="#33CCFF",text=0,font=('Arial', 25))
game3_button = tk.Button(text="+",bg="#33CCFF",font=('Arial', 15),command=coin3add)
game3_start = tk.Button(text="遊玩",bg="#33CCFF",font=('Arial', 15),command=coin3sub)
game3_break = tk.Button(text="-",bg="#33CCFF",font=('Arial', 15),command=coin3break)
game3_ticket = tk.Button(bg="#33CCFF",text=0,font=('Arial', 25))
game3_box.grid(row=3, column=0,sticky=tk.E+tk.W+tk.N+tk.S)
game3_coin.grid(row=3, column=1,columnspan=1,sticky=tk.E+tk.W)
game3_button.grid(row=3, column=2,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game3_start.grid(row=3, column=3,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game3_break.grid(row=3, column=4,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game3_ticket.grid(row=3, column=5,columnspan=1,sticky=tk.E+tk.W)
#--------------機台四號--------------------
game4_box = tk.Button(bg="#FFBB66",text="四號",font=('Arial', 15),command=startbox4)
game4_coin = tk.Button(bg="#CCEEFF",text=0,font=('Arial', 25))
game4_button = tk.Button(text="+",bg="#CCEEFF",font=('Arial', 15),command=coin4add)
game4_start = tk.Button(text="遊玩",bg="#CCEEFF",font=('Arial', 15),command=coin4sub)
game4_break = tk.Button(text="-",bg="#CCEEFF",font=('Arial', 15),command=coin4break)
game4_ticket = tk.Button(bg="#CCEEFF",text=0,font=('Arial', 25))
game4_box.grid(row=4, column=0,sticky=tk.E+tk.W+tk.N+tk.S)
game4_coin.grid(row=4, column=1,columnspan=1,sticky=tk.E+tk.W)
game4_button.grid(row=4, column=2,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game4_start.grid(row=4, column=3,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game4_break.grid(row=4, column=4,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game4_ticket.grid(row=4, column=5,columnspan=1,sticky=tk.E+tk.W)
#--------------機台五號--------------------
game5_box = tk.Button(bg="#FFBB66",text="五號",font=('Arial', 15),command=startbox5)
game5_coin = tk.Button(bg="#33CCFF",text=0,font=('Arial', 25))
game5_button = tk.Button(text="+",bg="#33CCFF",font=('Arial', 15),command=coin5add)
game5_start = tk.Button(text="遊玩",bg="#33CCFF",font=('Arial', 15),command=coin5sub)
game5_break = tk.Button(text="-",bg="#33CCFF",font=('Arial', 15),command=coin5break)
game5_ticket = tk.Button(bg="#33CCFF",text=0,font=('Arial', 25))
game5_box.grid(row=5, column=0,sticky=tk.E+tk.W+tk.N+tk.S)
game5_coin.grid(row=5, column=1,columnspan=1,sticky=tk.E+tk.W)
game5_button.grid(row=5, column=2,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game5_start.grid(row=5, column=3,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game5_break.grid(row=5, column=4,columnspan=1,sticky=tk.E+tk.W+tk.N+tk.S)
game5_ticket.grid(row=5, column=5,columnspan=1,sticky=tk.E+tk.W)













win.mainloop()