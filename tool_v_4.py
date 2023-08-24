from tkinter import *
from tkinter import Button
from functools import partial
import cx_Oracle 
import mysql.connector 
import numpy as np 
import pandas as pd  
import datetime  
from decimal import Decimal 
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os.path
import xlwt  
from xlwt import Workbook
from psycopg2 import sql  

def get_all_tables(D,d_name): 
    if(d_name == "oracle") :
        q = "SELECT table_name FROM user_tables" 
    elif(d_name == "mysql") :
        q = "SHOW TABLES"  
    else:
        pass 
    cur = D.cursor() 
    cur.execute(q) 
    l = []
    for i in cur.fetchall():
        l.append(i[0].upper())
    return   l 
def get_all_rows_of_table(D,d_name,t_name) :
    cur = D.cursor() 
    cur.execute(f'select * from {t_name}')    
    rows = cur.fetchall() 
    return rows
def get_all_columns_of_table(D,d_name,t_name):
    cur = D.cursor()   
    if(d_name == "oracle") :
        cur.execute(f'select * from {t_name}')
        cols = np.array(cur.description)[::,0] 
    elif(d_name == "mysql") :
        cur.execute(f"desc {t_name}")  
        cols = np.array(cur.fetchall())[::,0] 
    else:
        pass
    return cols 
def get_all_constraints(D,d_name,t_name) :
    cur = D.cursor() 
    if(d_name == "oracle") :
        cur.execute("SELECT  column_name, constraint_type  from user_constraints natural join user_cons_columns where table_name = :e",{'e':t_name.upper()})  
        c = {}
        for i in cur.fetchall():
            i = list(i)
            if(i[1] == 'P') :
                i[1] = 'PRIMARY' 
            if(i[1] == 'C') :
                i[1] = 'CHECK' 
            if(i[1] == 'R'):
                i[1] = 'FORIEGN' 
            if(i[1] == 'U'):
                i[1] = 'UNIQUE' 
            c[i[0]] = i[1]  
    elif(d_name == "mysql") :
        cur.execute("""select COLUMN_NAME, CONSTRAINT_NAME from information_schema.KEY_COLUMN_USAGE where TABLE_NAME ='{}'  """.format(t_name.upper()) )
        c = {}
        for i in cur.fetchall(): 
            i = list(i)
            if(i[0] == i[1]):
                i[1] = 'UNIQUE'
            i[0] = i[0].upper() 
            c[i[0]] = i[1]  
    else :
        pass 
    return c
def get_mismatch_datatypes(D1,D2,C1,C2,t1_name,t2_name): 
    message = ""
    l = []
    count = 0
    for i in range(len(D1[0])) :
        if(type(D1[0][i]) == type(D2[0][i])) :
            pass 
        else:
            count+=1  
            l.append([t1_name,t2_name,'Mismatched datatype','-',i,C1[i],str(type(D1[0][i])),str(type(D2[0][i]))])  
            message += t1_name.ljust(20," ")+t2_name.ljust(20," ")+"Mismatched datatype".ljust(30," ") + "-".ljust(5," ")+str(i+1).ljust(10," ") + C1[i].ljust(20," ")+str(type(D1[0][i])).ljust(40," ") +str(type(D2[0][i])).ljust(40," ")+"\n"
    return message,l,count  

def get_mismatch_constraints(d1,d2,d1_name,d2_name,t1_name,t2_name) :  
    c11 = get_all_constraints(d1,d1_name,t1_name)
    c22 = get_all_constraints(d2,d2_name,t2_name) 
    set1 = set(c11.keys()) 
    set2 = set(c22.keys()) 
    count = 0
    message = ""
    l = []
    for i in set1-set2 :  
        count+=1 
        l.append([t1_name,t2_name,'Mismatched constraint','-','-',i,c11[i],"NO CONSTRAIN"]) 
        message+=t1_name.ljust(20," ")+t2_name.ljust(20," ")+ "Mismatched Constraint".ljust(30," ") + "-".ljust(5," ")+"-".ljust(10," ") + i.ljust(20," ")+c11[i].ljust(40," ") +"NO CONSTRAIN".ljust(40," ")+"\n" 
    for i in set2-set1 :
        count+=1
        l.append([t1_name,t2_name,'Mismatched constraint','-','-',i,"NO CONSTRAIN",c22[i]]) 
        message+=t1_name.ljust(20," ")+t2_name.ljust(20," ")+ "Mismatched Constraint".ljust(30," ") + "-".ljust(5," ")+"-".ljust(10," ") + i.ljust(20," ")+"NO CONSTRAIN".ljust(40," ")+c22[i].ljust(40," ")+"\n" 
    for i in set1&set2 :
        if(c11[i] != c22[i]):
            count+=1 
            l.append([t1_name,t2_name,'Mismatched constraint','-','-',i,c11[i],c22[i]]) 
            message+=t1_name.ljust(20," ")+t2_name.ljust(20," ")+ "Mismatched Constraint".ljust(30," ") + "-".ljust(5," ")+"-".ljust(10," ") + i.ljust(20," ")+c11[i].ljust(40," ")+c22[i].ljust(40," ")+"\n"
    return message,l,count  
def get_mismatch_data(D1,D2,C1,C2,t1_name,t2_name):
    message = ""
    l = []
    count = 0
    for i in range(len(D1)) :
        for j in range(len(D1[0])):
            if(type(D2[0][j]) == datetime.date) : 
                if(D1[i][j].date() != D2[i][j]):
                    count+=1 
                    l.append([t1_name,t2_name,'Mismatched data',i+1,j+1,C1[j],str(D1[i][j]),str(D2[i][j])]) 
                    message+=t1_name.ljust(20," ")+t2_name.ljust(20," ")+ "Mismatched Data".ljust(30," ") + str(i+1).ljust(5," ")+str(j+1).ljust(10," ") + C1[j].ljust(20," ")+str(D1[i][j]).ljust(40," ")+str(D2[i][j]).ljust(40," ")+"\n"        
            elif(type(D1[0][j]) == float):
                if(D1[i][j] != float(D2[i][j])):
                    count+=1 
                    l.append([t1_name,t2_name,'Mismatched data',i+1,j+1,C1[j],str(D1[i][j]),str(D2[i][j])]) 
                    message+=t1_name.ljust(20," ")+t2_name.ljust(20," ")+ "Mismatched Data".ljust(30," ") + str(i+1).ljust(5," ")+str(j+1).ljust(10," ") + C1[j].ljust(20," ")+str(D1[i][j]).ljust(40," ")+str(D2[i][j]).ljust(40," ")+"\n"  
            else:
                if(D1[i][j] != D2[i][j]):
                    count+=1 
                    l.append([t1_name,t2_name,'Mismatched data',i+1,j+1,C1[j],str(D1[i][j]),str(D2[i][j])]) 
                    message+=t1_name.ljust(20," ")+t2_name.ljust(20," ")+ "Mismatched Data".ljust(30," ") + str(i+1).ljust(5," ")+str(j+1).ljust(10," ") + C1[j].ljust(20," ")+str(D1[i][j]).ljust(40," ")+str(D2[i][j]).ljust(40," ")+"\n"     
    return message,l,count 
def compare_table(d1,d2,d1_name,d2_name,t1_name,t2_name) : 

    rows1 = get_all_rows_of_table(d1,d1_name,t1_name)
    rows2 = get_all_rows_of_table(d2,d2_name,t2_name) 
    cols1 = get_all_columns_of_table(d1,d1_name,t1_name) 
    cols2 = get_all_columns_of_table(d2,d2_name,t2_name)  

    if(len(rows1) == len(rows2) and len(cols1) == len(cols2)) : 
        a = get_mismatch_datatypes(rows1,rows2,cols1,cols2,t1_name,t2_name) 
        b = get_mismatch_constraints(d1,d2,d1_name,d2_name,t1_name,t2_name) 
        c = get_mismatch_data(rows1,rows2,cols1,cols2,t1_name,t2_name)
        mismatches_list = a[1]+b[1]+c[1]  
        mismatches_message = a[0]+b[0]+c[0] 
        count = a[2]+b[2]+c[2]  
        return mismatches_message,mismatches_list,count 
    else :
        message = ""
        message += "Sorry Two schemas are not matcheing "+"\n" 
        message += "In   "+d1_name + "   ("+str(len(rows1)) +","+str(len(cols1)) +")"+"\n" 
        message += "In   "+d2_name + "   ("+str(len(rows2)) +","+str(len(cols2)) +")"+"\n" 
        return message,[],0 
def compare_only_column(d1,d2,d1_name,d2_name,table_name1,table_name2,s):   
    cols1 = get_all_columns_of_table(d1,d1_name,table_name1) 
    cols2 = get_all_columns_of_table(d2,d2_name,table_name2)  
    index = list(cols1).index(s)
    rows1 =  get_all_rows_of_table(d1,d1_name,table_name1)
    rows2 =  get_all_rows_of_table(d2,d2_name,table_name2)
    a = get_mismatch_datatypes(rows1,rows2,cols1,cols2,table_name1,table_name2) 
    b = get_mismatch_constraints(d1,d2,d1_name,d2_name,table_name1,table_name2) 
    rows1 = [[i[index]] for i in get_all_rows_of_table(d1,d1_name,table_name1)]
    rows2 = [[i[index]] for i in get_all_rows_of_table(d2,d2_name,table_name2)]
    c = get_mismatch_data(rows1,rows2,[s.upper()],[s.upper()],table_name1,table_name2)
    mismatches_list = a[1]+b[1]+c[1]  
    mismatches_message = a[0]+b[0]+c[0] 
    count = a[2]+b[2]+c[2]  
    return mismatches_message,mismatches_list,count 
def make_excel(l,count,d1,d2) :
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    sheet1.write(0, 0, 'Table Name1 ')
    sheet1.write(0, 1, 'Table Name2 ')
    sheet1.write(0, 2, 'Mismatch Type')
    sheet1.write(0, 3, 'Row No')
    sheet1.write(0, 4, 'Column No')
    sheet1.write(0,5,'Column Name') 
    sheet1.write(0, 6, "In"+ d1)
    sheet1.write(0, 7, "In"+d2)  
    for i in range(0,count) :
        for j in range(len(l[0])) :
            sheet1.write(i+1, j,l[i][j])  
    return wb
def save_file(l,count,d1,d2,filename): 
    wb = make_excel(l,count,d1,d2)
    folder = filedialog.askdirectory()    
    completeName1 = os.path.join(folder,filename.get()+".xls" )  
    wb.save(completeName1)  

def solve(d1,d2,d1_name,d2_name,table_name1,table_name2,t,compare_type):
    s = compare_type.get() 
    message=("TableName 1").ljust(20," ")+("TableName 2").ljust(20," ")+ "Mismatched Type".ljust(30," ") + "R No".ljust(5," ")+"C No".ljust(10," ") + "Column Name".ljust(20," ")+("In "+d1_name).ljust(40," ")+("In "+d2_name).ljust(40," ")+"\n" +"-"*180 +"\n"
    if(s == "all columns"): 
        print("all columns") 
        if(d1_name == "mysql") :
            a = compare_table(d2,d1,d2_name,d1_name,table_name2,table_name1) 
        else:
            a = compare_table(d1,d2,d1_name,d2_name,table_name1,table_name2) 
    else: 
        a = compare_only_column(d1,d2,d1_name,d2_name,table_name1,table_name2,s)
    T2 = Text(t, height = 25, width = 180)
    T2.insert(tk.END, message+a[0])  
    T2.place(x=25,y=150) 
    Label(t, text="File name",font = ("Helvetica",20),bg="#BFC9CA").place(x = 100,y = 600) 
    username1 = StringVar()
    usernameEntry = Entry(t ,textvariable=username1,font = ("Helvetica",20)).place(x = 370,y = 600) 
    save_file1 = partial(save_file,a[1],a[2],d1_name,d2_name,username1) 
    btn = Button(t, text = 'save file',font=("Helvetica", 15),command = save_file1).place(x=750,y=600)
def compare_single_table(d1,d2,d1_name,d2_name,table_name1,table_name2,t) : 
    t_name1 = table_name1.get() 
    t_name2 = table_name2.get()  
    rows1 = get_all_rows_of_table(d1,d1_name,t_name1)
    rows2 = get_all_rows_of_table(d2,d2_name,t_name2) 
    cols1 = get_all_columns_of_table(d1,d1_name,t_name1) 
    cols2 = get_all_columns_of_table(d2,d2_name,t_name2)   
    if(len(rows1) == len(rows2) and len(cols1) == len(cols2)) :  
        x = list(cols1) + ["all columns"] 
        n = tk.StringVar()  
        compare_type = ttk.Combobox(t, font=("Helvetica", 10),width = 30, textvariable = n,height = 250)  
        compare_type['values'] = tuple(x) 
        compare_type.place(x = 1250,y = 50)
        compare_type.current()
        solve1 = partial(solve,d1,d2,d1_name,d2_name,t_name1,t_name2,t,compare_type) 
        btn = Button(t, text = 'start',font=("Helvetica", 10),command = solve1).place(x=1400,y=80) 
    else: 
        message = ""
        message += "Sorry Two schemas are not matching "+"\n" 
        message += "In   "+d1_name + "   ("+str(len(rows1)) +","+str(len(cols1)) +")"+"\n" 
        message += "In   "+d2_name + "   ("+str(len(rows2)) +","+str(len(cols2)) +")"+"\n"
        T2 = Text(t, height = 25, width = 180)
        T2.insert(tk.END, message) 
        T2.place(x=35,y=150)
    
def compare_all_tables(d1,d2,d1_name,d2_name,all_tables,t): 
    message = ""
    l = []
    count = 0 
    for i in all_tables:
        print(i)
        a = compare_table(d1,d2,d1_name,d2_name,i,i) 
        message +=a[0] 
        l += a[1] 
        count += a[2]  
    return message,l,count

def Go(d1,d2,d1_name,d2_name,compare_type,t,all_tables) :
    s = compare_type.get() 
    if(s == "single table") : 
        usernameLabel = Label(t, text="Table Name",font = ("Helvetica",15)).place(x = 600,y = 20) 
        n = tk.StringVar()  
        table_name = ttk.Combobox(t, font=("Helvetica", 10),width = 30, textvariable = n,height = 20)  
        table_name['values'] = tuple(all_tables) 
        table_name.place(x = 800,y = 20)
        table_name.current() 
        compare_single_table1 = partial(compare_single_table,d1,d2,d1_name,d2_name,table_name,table_name,t) 
        btn = Button(t, text = 'start',font=("Helvetica", 15),command = compare_single_table1).place(x=1050,y=20) 

        Label(t, text="Table1",font = ("Helvetica",10)).place(x = 550,y = 80) 
        d1_all_tables = get_all_tables(d1,d1_name)
        n2 = tk.StringVar()
        table_name1 = ttk.Combobox(t, font=("Helvetica", 10),width = 30, textvariable = n2,height = 80)  
        table_name1['values'] = tuple(d1_all_tables) 
        table_name1.place(x = 600,y = 80) 
        Label(t, text="Table2",font = ("Helvetica",10)).place(x = 850,y = 80)
        d2_all_tables = get_all_tables(d2,d2_name)
        n1 = tk.StringVar() 
        table_name2 = ttk.Combobox(t, font=("Helvetica", 10),width = 30, textvariable = n1,height = 80)  
        table_name2['values'] = tuple(d2_all_tables) 
        table_name2.place(x = 900,y = 80) 
        compare_single_table2 = partial(compare_single_table,d1,d2,d1_name,d2_name,table_name1,table_name2,t) 
        btn = Button(t, text = 'start',font=("Helvetica", 10),command = compare_single_table2).place(x=1200,y=80) 
    else : 
        a = compare_all_tables(d1,d2,d1_name,d2_name,all_tables,t) 
        message=("TableName 1").ljust(20," ")+("TableName 2").ljust(20," ")+ "Mismatched Type".ljust(30," ") + "RNo".ljust(5," ")+"CNo".ljust(10," ") + "Column Name".ljust(20," ")+("In "+d1_name).ljust(40," ")+("In "+d2_name).ljust(40," ")+"\n" +"-"*180 +"\n"
        T2 = Text(t, height = 25, width = 180)
        T2.insert(tk.END, message+a[0]) 
        T2.place(x=25,y=150) 

        Label(t, text="File name",font = ("Helvetica",20),bg = "#BFC9CA").place(x = 100,y = 600) 
        username1 = StringVar()
        usernameEntry = Entry(t ,textvariable=username1,font = ("Helvetica",20)).place(x = 370,y = 600) 
        save_file1 = partial(save_file,a[1],a[2],d1_name,d2_name,username1) 
        btn = Button(t, text = 'save file',font=("Helvetica", 15),command = save_file1).place(x=750,y=600) 


def compare(D1,D2,d1_name,d2_name) : 
    '''if(s == "mysql") :
        temp = d1 
        d1 = d2 
        d2 = temp''' 
    t = Toplevel()  
    t.geometry('1500x1500')  
    t.title('Comparision') 
    t.configure(bg='#BFC9CA') 
    d1_tables = set(get_all_tables(D1,d1_name) )
    d2_tables = set(get_all_tables(D2,d2_name) ) 
    all_tables = list(d1_tables&d2_tables) 
    print(all_tables) 
    Label(t,text = "Compare type :",font=("Helvetica", 20),bg = "#BFC9CA",fg = "black").place(x=30,y=50) 
    n = tk.StringVar()  
    compare_type = ttk.Combobox(t, font=("Helvetica", 10),width = 30, textvariable = n,height = 250)  
    compare_type['values'] = ('All tables','single table')  
    compare_type.place(x = 250,y = 50)
    compare_type.current()
    Go1 = partial(Go,D1,D2,d1_name,d2_name,compare_type,t,all_tables)  
    btn = Button(t, text = 'Go',font=("Helvetica", 10),command = Go1).place(x=500,y=50)  
    T2 = Text(t, height = 25, width = 180)
    T2.insert(tk.END, "") 
    T2.place(x=50,y=150) 


def connect_mysql(t,u,p) :
    try:
        d2 = mysql.connector.connect(
        host ="localhost",
        user =u.get(),
        passwd =p.get(),
        database = "casestudy")
        return d2 
    except Exception as e:
        Label(t,text = "check the details of mysql",font=("Helvetica", 18),bg = "#00ffff",fg = "black").place(x=300,y=700) 
        return False

def connect_oracle(t,u,p):
    s = u.get()+"/"+p.get()+"@localhost:1521/xe" 
    try:
        d1 = cx_Oracle.connect(s)
        return d1
    except Exception as e: 
        Label(t,text = "check the details of oracle",font=("Helvetica", 18),bg = "#00ffff",fg = "black").place(x=300,y=700) 
        return False
def connect_database(t,d,u,p) : 
    s = d.get() 
    if(s == "oracle") :
        return connect_oracle(t,u,p) 
    elif(s == "mysql") :
        return connect_mysql(t,u,p) 

def connect_databases(top,d1,d2,u1,u2,p1,p2): 
    d1_name = d1.get() 
    d2_name = d2.get()
    if(d1_name == d2_name) :
        Label(top,text = "Please select two different databases",font=("Helvetica", 15),bg = "#00ffff",fg = "black").place(x=300,y=700) 
    else:
        D1 = connect_database(top,d1,u1,p1)
        D2 = connect_database(top,d2,u2,p2)
        if(D1 and D2): 
            if(d1_name == "mysql") : 
                temp = D1 
                D1 = D2 
                D2 = temp 
                temp = d1_name
                d1_name = d2_name 
                d2_name = temp
            Label(top,text = " "*100 ,font=("Helvetica", 45),bg = "#BFC9CA",fg = "black").place(x=300,y=700)  
            compare1 = partial(compare,D1,D2,d1_name,d2_name) 
            btn = Button(top, text = 'Start Comparison',font=("Helvetica", 30),command = compare1).place(x=800,y=600) 


def start() : 
    top = Tk()  
    width = top.winfo_screenwidth() 
    height = top.winfo_screenheight()  

    top.geometry("%dx%d" % (width,height))  
    top.configure(bg='#BFC9CA')
    top.title("database comparator")  

    Label(top,text = "DATABASE COMPARATOR",font=("Helvetica", 45),bg = "#BFC9CA",fg = "black").place(x=300,y=50) 

    Label(top,text = "Database 1:",font=("Helvetica", 18),bg = "#BFC9CA",fg = "black").place(x=100,y=200) 
    n = tk.StringVar()  
    database1 = ttk.Combobox(top, font=("Helvetica", 10),width = 45, textvariable = n,height = 250)  
    database1['values'] = ('mysql','oracle') 
    database1.place(x = 300,y = 200)
    database1.current() 

    Label(top,text = "Database 2:",font=("Helvetica", 18),bg = "#BFC9CA",fg = "black").place(x=800,y=200)
    n2 = tk.StringVar()
    database2 = ttk.Combobox(top, font=("Helvetica", 10),width = 45, textvariable = n2,height = 250)  
    database2['values'] = ('mysql','oracle',) 
    database2.place(x = 1000,y = 200)
    database2.current()    

    Label(top, text="Username:",font = ("Helvetica",18),bg = "#BFC9CA").place(x = 100,y = 280) 
    username1 = StringVar()
    usernameEntry = Entry(top, textvariable=username1,font = ("Helvetica",20),width = 22).place(x = 300,y = 280) 

    Label(top,text="Password:",font = ("Helvetica",18),bg = "#BFC9CA").place(x = 100,y = 350)  
    password1 = StringVar()
    Entry(top, textvariable=password1, show='*',font = ("Helvetica",20),width = 22).place(x = 300,y = 350) 


    Label(top, text="Username:",font = ("Helvetica",18),bg = "#BFC9CA").place(x = 800,y = 280) 
    username2 = StringVar()
    Entry(top, textvariable=username2,font = ("Helvetica",20),width = 22).place(x = 1000,y = 280)  

    Label(top,text="Password:",font = ("Helvetica",18),bg = "#BFC9CA").place(x = 800,y = 350)  
    password2 = StringVar()
    Entry(top, textvariable=password2, show='*',font = ("Helvetica",20),width = 22).place(x = 1000,y = 350)  


    connect_databases1 = partial(connect_databases,top,database1,database2,username1,username2,password1,password2)
    btn = Button(top, text = 'Connect to databases',font=("Helvetica", 30),command = connect_databases1).place(x=350,y=600)
    top.mainloop() 
start()   