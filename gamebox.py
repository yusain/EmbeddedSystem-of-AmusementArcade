import tkinter as tk 
import tkinter.font as tkFont
import random
#--------------機台一號--------------------
coin1 = 0
def coin1add(): #投幣
    global coin1
    coin1+=1
    game1_coin.config(text=coin1)

def coin1sub(): #玩一場
    global coin1
    ticket1 = random.randrange(1, 100)
    if coin1 >= 2 :
        coin1-=2
        game1_coin.config(text=coin1)
        game1_ticket.config(text=ticket1)

def coin1break(): #退幣
    global coin1
    if coin1 > 0 :
        coin1 = 0
        game1_coin.config(text=coin1)

#--------------機台二號--------------------

coin2 = 0
def coin2add():
    global coin2
    coin2+=1
    game2_coin.config(text=coin2)

def coin2sub():
    global coin2
    ticket2 = random.randrange(1, 100)
    if coin2 >= 2 :
        coin2-=2
        game2_coin.config(text=coin2)
        game2_ticket.config(text=ticket2)

def coin2break():
    global coin2
    if coin2 > 0 :
        coin2 = 0
        game2_coin.config(text=coin2)

#--------------機台三號--------------------
coin3 = 0
def coin3add():
    global coin3
    coin3+=1
    game3_coin.config(text=coin3)

def coin3sub():
    global coin3
    ticket3 = random.randrange(1, 100)
    if coin3 >= 2 :
        coin3-=2
        game3_coin.config(text=coin3)
        game3_ticket.config(text=ticket3)

def coin3break():
    global coin3
    if coin3 > 0 :
        coin3 = 0
        game3_coin.config(text=coin3)

#--------------機台四號--------------------
coin4 = 0
def coin4add():
    global coin4
    coin4+=1
    game4_coin.config(text=coin4)

def coin4sub():
    global coin4
    ticket4 = random.randrange(1, 100)
    if coin4 >= 2 :
        coin4-=2
        game4_coin.config(text=coin4)
        game4_ticket.config(text=ticket4)

def coin4break():
    global coin4
    if coin4 > 0 :
        coin4 = 0
        game4_coin.config(text=coin4)

win = tk.Tk()
win.geometry("480x360+400+200")
win.minsize(width=480,height=360)
win.maxsize(width=480,height=360)

#--------------機台五號--------------------
coin5 = 0
def coin5add():
    global coin5
    coin5+=1
    game5_coin.config(text=coin5)

def coin5sub():
    global coin5
    ticket5 = random.randrange(1, 100)
    if coin5 >= 2 :
        coin5-=2
        game5_coin.config(text=coin5)
        game5_ticket.config(text=ticket5)

def coin5break():
    global coin5
    if coin5 > 0 :
        coin5 = 0
        game5_coin.config(text=coin5)


#--------------機台一號--------------------
game1_box = tk.Label(bg="#003C9D",fg="white",text=1,font="40",width=2,height=1)
game1_box.place(x=48,y=36)

game1_coin = tk.Label(bg="#003C9D",fg="white",text=0,font="40",width=8,height=1)
game1_coin.place(x=96,y=36)

game1_button = tk.Button(text="+",bg="#33FF33",width=3,height=2,font="1",command=coin1add)
game1_button.place(x=200,y=36)

game1_start = tk.Button(text="start",bg="#33FF33",width=3,height=2,font="1",command=coin1sub)
game1_start.place(x=260,y=36)

game1_break = tk.Button(text="break",bg="#33FF33",width=3,height=2,font="1",command=coin1break)
game1_break.place(x=320,y=36)

game1_ticket = tk.Label(bg="#003C9D",fg="white",text=0,font="40",width=8,height=1)
game1_ticket.place(x=380,y=36)

#--------------機台二號--------------------

game2_box = tk.Label(bg="#003C9D",fg="white",text=2,font="40",width=2,height=1)
game2_box.place(x=48,y=90)

game2_coin = tk.Label(bg="#003C9D",fg="white",text=0,font="40",width=8,height=1)
game2_coin.place(x=96,y=90)

game2_button = tk.Button(text="+",bg="#33FF33",width=3,height=2,font="1",command=coin2add)
game2_button.place(x=200,y=90)

game2_start = tk.Button(text="start",bg="#33FF33",width=3,height=2,font="1",command=coin2sub)
game2_start.place(x=260,y=90)

game2_break = tk.Button(text="break",bg="#33FF33",width=3,height=2,font="1",command=coin2break)
game2_break.place(x=320,y=90)

game2_ticket = tk.Label(bg="#003C9D",fg="white",text=0,font="40",width=8,height=1)
game2_ticket.place(x=380,y=90)

#--------------機台三號--------------------
game3_box = tk.Label(bg="#003C9D",fg="white",text=3,font="40",width=2,height=1)
game3_box.place(x=48,y=144)

game3_coin = tk.Label(bg="#003C9D",fg="white",text=0,font="40",width=8,height=1)
game3_coin.place(x=96,y=144)

game3_button = tk.Button(text="+",bg="#33FF33",width=3,height=2,font="1",command=coin3add)
game3_button.place(x=200,y=144)

game3_start = tk.Button(text="start",bg="#33FF33",width=3,height=2,font="1",command=coin3sub)
game3_start.place(x=260,y=144)

game3_break = tk.Button(text="break",bg="#33FF33",width=3,height=2,font="1",command=coin3break)
game3_break.place(x=320,y=144)

game3_ticket = tk.Label(bg="#003C9D",fg="white",text=0,font="40",width=8,height=1)
game3_ticket.place(x=380,y=144)

#--------------機台四號--------------------
game4_box = tk.Label(bg="#003C9D",fg="white",text=4,font="40",width=2,height=1)
game4_box.place(x=48,y=198)

game4_coin = tk.Label(bg="#003C9D",fg="white",text=0,font="40",width=8,height=1)
game4_coin.place(x=96,y=198)

game4_button = tk.Button(text="+",bg="#33FF33",width=3,height=2,font="1",command=coin4add)
game4_button.place(x=200,y=198)

game4_start = tk.Button(text="start",bg="#33FF33",width=3,height=2,font="1",command=coin4sub)
game4_start.place(x=260,y=198)

game4_break = tk.Button(text="break",bg="#33FF33",width=3,height=2,font="1",command=coin4break)
game4_break.place(x=320,y=198)

game4_ticket = tk.Label(bg="#003C9D",fg="white",text=0,font="40",width=8,height=1)
game4_ticket.place(x=380,y=198)

#--------------機台五號--------------------
game5_box = tk.Label(bg="#003C9D",fg="white",text=5,font="40",width=2,height=1)
game5_box.place(x=48,y=252)

game5_coin = tk.Label(bg="#003C9D",fg="white",text=0,font="40",width=8,height=1)
game5_coin.place(x=96,y=252)

game5_button = tk.Button(text="+",bg="#33FF33",width=3,height=2,font="1",command=coin5add)
game5_button.place(x=200,y=252)

game5_start = tk.Button(text="start",bg="#33FF33",width=3,height=2,font="1",command=coin5sub)
game5_start.place(x=260,y=252)

game5_break = tk.Button(text="break",bg="#33FF33",width=3,height=2,font="1",command=coin5break)
game5_break.place(x=320,y=252)

game5_ticket = tk.Label(bg="#003C9D",fg="white",text=0,font="40",width=8,height=1)
game5_ticket.place(x=380,y=252)













win.mainloop()