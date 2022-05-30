import tkinter as tk 
import tkinter.font as tkFont
win = tk.Tk()
win.geometry("480x360+400+200")
win.minsize(width=480,height=360)
win.maxsize(width=480,height=360)

#-------副函式--------------------------
def add_ticket():
    global ticket_access
    ticket_access+=1
    ticket_amount.config(text=ticket_access)
    
def printer():
    global ticket_access
    #隱藏第一階段
    ticket_name.pack_forget()
    ticket_amount.pack_forget()
    add_button.pack_forget()
    print_button.pack_forget()
    #顯示第二階段
    printer_ticket_button.pack(expand=True)
    printer_ticket_button.config(text=ticket_access)

def break_start():
    #隱藏第二階段
    printer_ticket_button.pack_forget()
    #顯示第一階段
    ticket_name.pack(anchor=tk.CENTER)
    ticket_amount.pack(anchor=tk.CENTER)
    add_button.pack(side=tk.LEFT)
    print_button.pack(side=tk.RIGHT)
    ticket_access = 0
    ticket_amount.config(text=ticket_access)

#--------參數---------------------------
ticket_access = 0





#--------第一階段--------------------------------------------------
ticket_name = tk.Label(bg="#003C9D",fg="white",text="讀取到的彩票數量",font="40",width=20,height=5)
ticket_amount = tk.Label(bg="#9900FF",fg="white",text=ticket_access,font="40",width=20,height=5)
add_button = tk.Button(text="+",bg="#33FF33",width=5,height=1,font="10",command=add_ticket)
print_button = tk.Button(text="QRcode",bg="#33FF33",width=5,height=1,font="10",command=printer)
ticket_name.pack(anchor=tk.CENTER)
ticket_amount.pack(anchor=tk.CENTER)
add_button.pack(side=tk.LEFT)
print_button.pack(side=tk.RIGHT)
#--------第二階段--------------------------------------------------
printer_ticket_button = tk.Button(text=ticket_access,bg="#33FF33",font="40",width=20,height=5,command=break_start)

win.mainloop()