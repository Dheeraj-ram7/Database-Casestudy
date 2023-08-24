import tkinter as tk 
from tkinter import ttk 
from tkinter import *
from tkinter.filedialog import asksaveasfile
import cx_Oracle
import mysql.connector
import functools  
import operator 
import xlwt
from xlwt import Workbook
import csv
frame = Tk()
frame.title("TextBox Input")
width= frame.winfo_screenwidth()
height= frame.winfo_screenheight()
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


def excel(se,cer1,cer2,ced1,ced2,q):
    f=asksaveasfile(initialfile=q+'_errors.csv',defaultextension=".csv",filetypes=[("All Files","*.*"),("csv file","*.csv")])
    write = csv.writer(f) 
    s=['ERRORS']
    write.writerow(s)
    s1=['ATTRIBUTE','ERRORS']
    write.writerow(s1)
    write.writerow(se)
    s2=['DATA','ERRORS']
    write.writerow(s2)
    s3=['ORACLE','TABLE']
    write.writerow(s3)
    write.writerow(cer1)
    write.writerows(ced1)
    s4=['MYSQL','TABLE']
    write.writerow(s4)
    write.writerow(cer2)
    write.writerows(ced2)




l =tk.Label(text = "Compare Tool", font=("Times",32),fg="blue",bg='lightcyan1').place(relx = 0.5,rely = 0,anchor = 'n')

l1=tk.Label(frame,text = " DB credentials", font="Times",bg='lightcyan1').place(x=200,y=60)
u1 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
u1.place(x=400,y=60)
p1 = tk.Entry(frame,width=30, font=('Arial 12'),show='*',highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
p1.place(x=700,y=60)

l2=tk.Label(frame,text = " DB credentials", font="Times",bg='lightcyan1').place(x=200,y=90)
u2 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
u2.place(x=400,y=90)
p2 = tk.Entry(frame,width=30, font=('Arial 12'),show='*',highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
p2.place(x=700,y=90)

lo = tk.Label(frame,text = "Enter Oracle Table Name", font="Times",bg='lightcyan1')
lo.place(x=30,y=130)
inputtxt1 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
inputtxt1.place(x=240,y=130)

lm = tk.Label(frame,text = "Enter MYSQL Table Name", font="Times",bg='lightcyan1')
lm.place(x=530,y=130)
inputtxt2 = tk.Entry(frame,width=30, font=('Arial 12'),highlightthickness=2,highlightbackground = "black", highlightcolor= "red")
inputtxt2.place(x=760,y=130)

printButton = tk.Button(frame,text = "SUBMIT" ,height=1,width=8,bg="black",fg="white",font="LucidaConsole 11 bold",borderwidth=3,command =lambda: [connect_orcl(),connect_mysql()])
printButton.place(x=1100,y=125)

n = tk.StringVar()
db1 = ttk.Combobox(frame, width = 27, textvariable = n)
db1['values']=('oracle','mysql')
db1.place(x=20,y=60)


n = tk.StringVar()
db2 = ttk.Combobox(frame, width = 27, textvariable = n)
db2['values']=('oracle','mysql')
db2.place(x=20,y=90)

def check():
    next = Tk()
    next.title("TextBox Input")
    width= next.winfo_screenwidth()
    height= next.winfo_screenheight()
    #setting tkinter window size
    next.geometry("%dx%d" % (width, height))
    next.configure(bg='lightcyan1')
    (D1,L1,Q)=connect_orcl()
    (D2,L2)=connect_mysql()
    print("D1",D1)
    print("L1",L1)
    print("D2",D2)
    print("L2",L2)
    s=[]
    c=[]
    se=[]
    cer1=[]
    cer2=[]
    ced1=[]
    ced2=[]
    for i in range(len(D1)):
        cer1.append(L1[i][0])#table 1 rows
        cer2.append(L2[i][0])#table 2 rows
        if(D1[i]!=D2[i]):
            ced1.append(list(D1[i]))#table 1 error data
            ced2.append(list(D2[i]))#table 2 error data
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
    cols1=[]
    cols2=[]
    for i in range(len(cer1)):
        cols1.append("#"+str(i))
    treev = ttk.Treeview(next, columns=tuple(cols1))
    vsb = ttk.Scrollbar(next, orient="vertical", command=treev.yview)
    #vsb.place(x=30+200+2, y=95, height=200+20)
    treev.configure(yscrollcommand=vsb.set)
    treev.column("#0", width=0)
    for i in range(len(cer1)):
        treev.column("#"+str(i),anchor=CENTER)
    for i in range(len(cer1)):
        treev.heading(str(i), text =str(cer1[i]))
    k=0
    for i in range(len(ced1)):
        treev.insert('', 'end',text=str(k),values=ced1[i])
        k+=1
    treev.place(x=20,y=30)

    for i in range(len(cer2)):
        cols2.append("#"+str(i))
    treev2 = ttk.Treeview(next, columns=tuple(cols2))
    vsb = ttk.Scrollbar(next, orient="vertical", command=treev.yview)
    #vsb.place(x=30+200+2, y=95, height=200+20)
    treev2.configure(yscrollcommand=vsb.set)
    treev2.column("#0", width=0)
    for i in range(len(cer2)):
        treev2.column("#"+str(i),anchor=CENTER)
    for i in range(len(cer2)):
        treev2.heading(str(i), text =str(cer2[i]))
    k=0
    for i in range(len(ced2)):
        treev2.insert('', 'end',text=str(k),values=ced2[i])
        k+=1
    treev2.place(x=650,y=30)
    if(s==[]):
        print("No errors in structure")
    else:
        print("Structure Error",s)
    if(c==[]):
        print("No errors")
    else:
        print("Error!",c)
    if(c!=[] or s!=[]):
        text= Text(next, width= 110, height= 10, background="lightcyan1",font=("Times",12))
        text.place(x=200,y=360)
        #text.insert(INSERT, "Write Something About Yourself")
        e=tk.Label(next,text ="Errors Found:",font=("Times",24,UNDERLINE),fg="red",bg='lightcyan1').place(x=100,y=300)
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
        e=tk.Label(next,text ="No Errors Found",font=("Times",24,UNDERLINE),fg="green",bg='lightcyan1').place(x=540,y=260)
    
    if(c!=[] or s!=[]):
        btn=Button(next,text="SAVE FILE",command=lambda:[excel(se,cer1,cer2,ced1,ced2,Q)],height=1,width=8,bg="cyan",fg="blue",font="LucidaConsole 11 bold",borderwidth=3).place(x=600,y=600)


frame.mainloop()