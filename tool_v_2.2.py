
import tkinter as tk 
from tkinter import ttk 
from tkinter import *
from tkinter.filedialog import asksaveasfile
import cx_Oracle
import mysql.connector
import functools  
import operator 

import csv 

frame = Tk()
frame.title("TextBox Input")
width= frame.winfo_screenwidth()
height= frame.winfo_screenheight()
print(width,height)
#setting tkinter window size
frame.geometry("%dx%d" % (width, height))
frame.configure(bg='lightcyan1')

def user1():
    u=u1.get()
    return u

def user2():
    u=u2.get()
    return u

def pass1():
    p=p1.get()
    return p

def pass2():
    p=p2.get()
    return p

def printInput1():
    inp = inputtxt1.get()
    print(type(inp))
    return inp

def printInput2():
    inp = inputtxt2.get()
    print(type(inp))
    return inp

def connect_orcl():
    u=user1()
    p=pass1()
    q=printInput1()
    query="SELECT * FROM "+q
    con=cx_Oracle.connect(u+'/'+p+'@localhost:1521/'+u)
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
    u=user2()
    p=pass2()
    checkButton = tk.Button(frame,text = "COMPARE",height=1,width=8,bg="green",fg="white",font="LucidaConsole 11 bold",borderwidth=3, command =lambda: [check()])
    checkButton.place(x=600,y=170)
    q=printInput2()
    query="SELECT * FROM "+q
    print(query)
    conn = mysql.connector.connect(
    host="localhost",
    user=u, 
    passwd=p,
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

def excel(se,ce,q):
    f=asksaveasfile(initialfile=q+'_errors.csv',defaultextension=".csv",filetypes=[("All Files","*.*"),("csv file","*.csv")])
    write = csv.writer(f) 
    write.writerow(se)
    write.writerows(ce)


l =tk.Label(text = "Compare Tool", font=("Times",32),fg="blue",bg='lightcyan1').place(relx = 0.5,rely = 0,anchor = 'n')

l1=tk.Label(frame,text = "Oracle DB credentials", font="Times",bg='lightcyan1').place(x=50,y=60)
u1 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
u1.place(x=250,y=60)
p1 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
p1.place(x=550,y=60)

l2=tk.Label(frame,text = "MySQL DB credentials", font="Times",bg='lightcyan1').place(x=50,y=90)
u2 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
u2.place(x=250,y=90)
p2 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
p2.place(x=550,y=90)

lo = tk.Label(frame,text = "Enter Oracle Table Name", font="Times",bg='lightcyan1')
lo.place(x=50,y=130)
inputtxt1 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
inputtxt1.place(x=250,y=130)

lm = tk.Label(frame,text = "Enter MYSQL Table Name", font="Times",bg='lightcyan1')
lm.place(x=550,y=130)
inputtxt2 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
inputtxt2.place(x=750,y=130)

printButton = tk.Button(frame,text = "SUBMIT" ,height=1,width=8,bg="black",fg="white",font="LucidaConsole 11 bold",borderwidth=3,command =lambda: [connect_orcl(),connect_mysql()])
printButton.place(x=1100,y=125)



def check():
    (D1,L1,Q)=connect_orcl()
    (D2,L2)=connect_mysql()
    print("D1",D1)
    print("L1",L1)
    print("D2",D2)
    print("L2",L2)
    s=[]
    c=[]
    se=[]
    ce=[]
    for i in range(len(D1)):
        if(D1[i]!=D2[i]):
            ce.append([D1[i]])
            ce.append([D2[i]])
            c.append(("Oracle : ",str(D1[i])," MySQL : ",str(D2[i])," at line : ",str(i+1),"\n"))
        if(L1[i][0]!=L2[i][0]):
            k=L1[i][0]
            se.append(k)
            k=L2[i][0]
            se.append(k)
            s.append(("Oracle : ",str(L1[i][0])," MySQL : ",str(L2[i][0])," attribute : ",str(i+1),"\n"))
    print("S",s)
    print("C",c)
    print("SE",se)
    print("CE",ce)
    if(s==[]):
        print("No errors in structure")
    else:
        print("Structure Error",s)
    if(c==[]):
        print("No errors")
    else:
        print("Error!",c)
    if(c!=[] or s!=[]):
        text= Text(frame, width= 110, height= 10, background="lightcyan1",font=("Times",12))
        text.place(x=200,y=280)
        #text.insert(INSERT, "Write Something About Yourself")
        e=tk.Label(frame,text ="Errors Found:",font=("Times",24,UNDERLINE),fg="red",bg='lightcyan1').place(x=100,y=220)
        #e1=tk.Label(frame,text ="[Structure Errors]",font=("Times",20),fg="dark orange",bg='lightcyan1').place(x=550,y=260)
        text.insert(INSERT, "-------------------STRUCTURE ERRORS-------------------\n")
        #e2=tk.Label(frame,text ="[Data Errors]",font=("Times",20),fg="dark orange",bg='lightcyan1').place(x=800,y=260)
        for i in range(len(s)):
            #E= tk.Label(frame,text = s[i],font=("Times",16),bg='lightcyan1').place(x=550,y=290+len(D1)+i*25)
            t= functools.reduce(operator.add, (s[i]))
            text.insert(END,t)
        text.insert(INSERT, "\n-------------------DATA ERRORS-------------------\n")
        for i in range(len(c)):
            t= functools.reduce(operator.add, (c[i]))
            #E= tk.Label(frame,text = c[i],font=("Times",16),bg='lightcyan1').place(x=800,y=290+len(D1)+i*25)
            text.insert(END,t)
    else:
        e=tk.Label(frame,text ="No Errors Found",font=("Times",24,UNDERLINE),fg="green",bg='lightcyan1').place(x=540,y=260)
    
    if(c!=[] or s!=[]):
        btn=Button(frame,text="SAVE FILE",command=lambda:[save_file(s,c,Q),excel(se,ce,Q)],height=1,width=8,bg="cyan",fg="blue",font="LucidaConsole 11 bold",borderwidth=3).place(x=600,y=600)


frame.mainloop()