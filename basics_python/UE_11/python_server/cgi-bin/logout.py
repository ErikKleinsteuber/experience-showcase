#!C:\Users\Flat Erik\AppData\Local\Programs\Python\Python37\python.exe

import cgi
import cgitb
import os

cgitb.enable()

formData = cgi.FieldStorage()
name = formData.getvalue('username')

onlineUsers = open('C:\\My_stuff\\Studium\\[PYTHON]Skriptsprachen\\UE_11\\python_server\\cgi-bin\\online.txt').readlines()
usersRefreshed = ""
for user in onlineUsers:
    if user == f"{name}\n":
        pass
    else:
        usersRefreshed = usersRefreshed + user

with open('C:\\My_stuff\\Studium\\[PYTHON]Skriptsprachen\\UE_11\\python_server\\cgi-bin\\online.txt','a') as filehandler:
    filehandler.truncate(0)
    filehandler.write(usersRefreshed)