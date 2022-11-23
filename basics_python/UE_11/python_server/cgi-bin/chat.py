#!C:\Users\Flat Erik\AppData\Local\Programs\Python\Python37\python.exe

import cgi
import cgitb
import datetime

cgitb.enable()

formData = cgi.FieldStorage()
text = formData.getvalue('beitrag')
name = formData.getvalue('user')

if text != None:
    with open('C:\\My_stuff\\Studium\\[PYTHON]Skriptsprachen\\UE_11\\python_server\\chatlog.txt','a') as chatlog:
        chatlog.write(f'{name} :{datetime.datetime.now().time()}: {text}\n<br>\n')

chatlog = open('C:\\My_stuff\\Studium\\[PYTHON]Skriptsprachen\\UE_11\\python_server\\chatlog.txt').readlines()

print('<!DOCTYPE html>')
print('Content-Type: text/html; char-set-utf-8\n')
print('<html> <head> <title> Mein Python Chatroom </title>')
print('</head>')
print('<body>')
print(f'<h1>Willkommen im Python Chatroom, {name}!</h1>')
print('<br>')
print('<form method="post" action="chat.py">')
print(f'<input type="hidden" name="user" value="{name}">')
print('<input type="Text" name="beitrag" size="140" maxlength="140">')
print('<input type="submit" value="Absenden">')
print('</form>')
print('<br>')

print('<form method="post" action="logout.py">')
print(f'<input type="hidden" name="username" value="{name}">')
print('<input type="submit" value="Abmelden">')
print('</form>')

if (len(chatlog)> 0):
    print('<p style="border:3px; border-color:#008000; padding: 1em;">')
    for line in chatlog:
        nameHelper = 0
        for char in line:
            if char == " ":
                break
            else:
                nameHelper = nameHelper + ord(char)

        nameHelper = (nameHelper * 30481) % 16777215
        if nameHelper < 1118481:
            nameHelper = nameHelper + 1118481

        nameHex = '#'+ str(nameHelper)[2:]

        print(f'<font color="{nameHex}">') 
        print(line)
        print('</font>')

print('<br>')

#liste aller online user
clientList = open('C:\\My_stuff\\Studium\\[PYTHON]Skriptsprachen\\UE_11\\python_server\\cgi-bin\\online.txt').readlines()

for user in clientList:
    print(f'{user[:-1]}')
            

print('</p> </body> </html>')