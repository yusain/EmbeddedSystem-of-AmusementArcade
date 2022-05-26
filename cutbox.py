import tkinter as tk 
import tkinter.font as tkFont
win = tk.Tk()
win.geometry("1000x450+200+50")
win.minsize(width=1000,height=450)
win.maxsize(width=1000,height=450)
win.config(bg="#CCEEFF")

#-------副函式--------------------------
def ok():
    t = ticket_entry.get()
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

win.mainloop()