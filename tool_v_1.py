from tkinter import *
from tkinter.filedialog import asksaveasfile
import tkinter as tk     
import cx_Oracle
import mysql.connector

top = Tk() 
tk.Label(top,
         borderwidth = 3,
         relief="sunken",
         text="sunken & borderwidth=3")
top.title('Compare Tool') 
top.geometry("400x250")

#connecting to oracle

con=cx_Oracle.connect('system/dheeraj@localhost:1521/system')
cursor = con.cursor()
cursor.execute("SELECT * FROM student1")
Data1=cursor.fetchall()
print(Data1)
cursor.execute("SELECT * FROM student1")
i=0 
Oracle= Label(top,text = "Oracle").place(x = 60,y = 60)
for student1 in cursor: 
    for j in range(len(student1)):
        f = Entry(top, width=10, fg='blue') 
        f.grid(row=i, column=j) 
        f.insert(END, student1[j])
    i=i+1
cursor.execute("select column_name, data_type, data_length from user_tab_columns where table_name='STUDENT1'")
List1 = cursor.fetchall()
print(List1)

#connecting to mysql


MySQL= Label(top,text = "MySQL").place(x = 260,y = 60)
conn = mysql.connector.connect(
  host="localhost",
  user="root", 
  passwd="",
  database="mysql"
)
my_conn = conn.cursor()
my_conn.execute("SELECT * FROM student ")
Data2=my_conn.fetchall()
print(Data2)
my_conn.execute("SELECT * FROM student ")
i=0 
for student in my_conn: 
    for j in range(len(student)):
        e = Entry(top, width=10, fg='red') 
        e.grid(row=i, column=j+4) 
        e.insert(END, student[j])
    i=i+1
my_conn.execute("SELECT COLUMN_NAME,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'STUDENT'")
List2 = my_conn.fetchall()
print(List2)
s=[]
c=[]

for i in range(len(student)):
    if(Data1[i]!=Data2[i]):
        c.append((Data2[i],"at line",i))
    if(List1[i][0]!=List2[i][0]):
        s.append((List2[i][0],i))
        
if(s==[]):
    print("No errors in structure")
else:
    print("Structure Error",s)
if(c==[]):
    print("No errors")
else:
    print("Error!",c)
if(c!=[] or s!=[]):
    e=Label(top,text ="Errors Found:").place(x = 10,y = 100+len(student))
    e1=Label(top,text ="[Structure Errors]").place(x = 100,y = 100+len(student))
    e2=Label(top,text ="[Data Errors]").place(x = 200,y = 100+len(student))
    for i in range(len(s)):
        E= Label(top,text = s[i]).place(x = 100,y = 120+len(student)+i*20)
    for i in range(len(c)):
        E= Label(top,text = c[i]).place(x = 200,y = 120+len(student)+i*20)
else:
    e=Label(top,text ="No Errors Found").place(x = 80,y = 100)

#saving into a text file

def save_file():
    f=asksaveasfile(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    f.write("Errors")
    f.write("\n")
    f.write("\n")
    for i in range(len(s)):
        f.write(str(s[i]))
        f.write("\n")
    f.write("\n")
    for i in range(len(c)):
        f.write(str(c[i]))
        f.write("\n")

if(c!=[] or s!=[]):
    btn=Button(top,text="Save",command=lambda:save_file()).place(x = 170,y = 200+len(s)+len(c)+len(student))

top.mainloop()  