import tkinter as tk 
from tkinter import ttk 
from tkinter import *
from tkinter.filedialog import asksaveasfile
import cx_Oracle
import mysql.connector

frame = Tk()
frame.title("TextBox Input")
width= frame.winfo_screenwidth()
height= frame.winfo_screenheight()
print(width,height)
#setting tkinter window size
frame.geometry("%dx%d" % (width, height))
frame.configure(bg='beige')

def printInput1():
    inp = inputtxt1.get()
    print(type(inp))
    query="SELECT * FROM "+inp
    return inp

def printInput2():
    inp = inputtxt2.get()
    print(type(inp))
    query="SELECT * FROM "+inp
    return inp

def connect_orcl():
    q=printInput1()
    query="SELECT * FROM "+q
    con=cx_Oracle.connect('system/dheeraj@localhost:1521/system')
    cursor = con.cursor()
    cursor.execute(query)
    Data1=cursor.fetchall()
    print(Data1)
    i=0 
    for k1 in cursor: 
        for j in range(len(k1)):
            f = tk.Entry(frame, width=10, fg='blue')
            f.grid(row=i, column=j,sticky=NSEW) 
            f.insert(END, k1[j])
        i=i+1
    inf_query="select column_name, data_type, data_length from user_tab_columns where table_name="+"\'"+q+"\'"
    cursor.execute(inf_query)
    List1 = cursor.fetchall()
    print(List1)
    return Data1,List1,q

def connect_mysql():
    checkButton = tk.Button(frame,text = "COMPARE",height=1,width=8,bg="green",fg="white",font="LucidaConsole 11 bold",borderwidth=3, command =lambda: [check()]).place(x=600,y=170)
    q=printInput2()
    query="SELECT * FROM "+q
    print(query)
    conn = mysql.connector.connect(
    host="localhost",
    user="root", 
    passwd="",
    database="mysql"
    )
    my_conn = conn.cursor()
    my_conn.execute(query)
    Data2=my_conn.fetchall()
    print(Data2)
    i=0 
    for k2 in my_conn: 
        for j in range(len(k2)):
            e = tk.Entry(frame, width=10, fg='red') 
            e.grid(row=i, column=j+4) 
            e.insert(frame, k2[j])
        i=i+1
    inf_query="SELECT COLUMN_NAME,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name ="+"\'"+q+"\'"
    my_conn.execute(inf_query)
    List2 = my_conn.fetchall()
    print(List2)
    return Data2,List2

def save_file(s,c,q):
    f=asksaveasfile(initialfile=q+'_errors.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    f.write("ERRORS")
    f.write("\n")
    f.write("\n")
    f.write("Attribute Errors:\n")
    for i in range(len(s)):
        f.write(str(s[i]))
        f.write("\n")
    f.write("\n")
    f.write("Data Errors:\n")
    for i in range(len(c)):
        f.write(str(c[i]))
        f.write("\n")

l =tk.Label(text = "Compare Tool", font=("Times",32),fg="blue",bg='beige').place(relx = 0.5,rely = 0,anchor = 'n')

l1 = tk.Label(frame,text = "Enter Oracle Table Name", font="Times",bg='beige')
l1.place(x=150,y=30)
inputtxt1 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
inputtxt1.place(x=150,y=70)

l2 = tk.Label(frame,text = "Enter MYSQL Table Name", font="Times",bg='beige')
l2.place(x=900,y=30)
inputtxt2 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
inputtxt2.place(x=900,y=70)

printButton = tk.Button(frame,text = "SUBMIT" ,height=1,width=8,bg="black",fg="white",font="LucidaConsole 11 bold",borderwidth=3,command =lambda: [connect_orcl(),connect_mysql()]).place(x=600,y=100)




def check():
    (D1,L1,Q)=connect_orcl()
    (D2,L2)=connect_mysql()
    print("D1",D1)
    print("L1",L1)
    print("D2",D2)
    print("L2",L2)
    s=[]
    c=[]
    for i in range(len(D1)):
        if(D1[i]!=D2[i]):
            c.append((D2[i],"at line",i))
        if(L1[i][0]!=L2[i][0]):
            s.append((L2[i][0],i))
    print("S",s)
    print("C",c)
    if(s==[]):
        print("No errors in structure")
    else:
        print("Structure Error",s)
    if(c==[]):
        print("No errors")
    else:
        print("Error!",c)
    if(c!=[] or s!=[]):
        e=tk.Label(frame,text ="Errors Found:",font=("Times",24,UNDERLINE),fg="red",bg='beige').place(x=300,y=260)
        e1=tk.Label(frame,text ="[Structure Errors]",font=("Times",20),fg="dark orange",bg='beige').place(x=550,y=260)
        e2=tk.Label(frame,text ="[Data Errors]",font=("Times",20),fg="dark orange",bg='beige').place(x=800,y=260)
        for i in range(len(s)):
            E= tk.Label(frame,text = s[i],font=("Times",16),bg='beige').place(x=550,y=290+len(D1)+i*25)
        for i in range(len(c)):
            E= tk.Label(frame,text = c[i],font=("Times",16),bg='beige').place(x=800,y=290+len(D1)+i*25)
    else:
        e=tk.Label(frame,text ="No Errors Found",font=("Times",24,UNDERLINE),fg="green",bg='beige').place(x=540,y=260)
    
    if(c!=[] or s!=[]):
        btn=Button(frame,text="SAVE FILE",command=lambda:[save_file(s,c,Q)],height=1,width=8,bg="cyan",fg="blue",font="LucidaConsole 11 bold",borderwidth=3).place(x=600,y=600)


frame.mainloop()