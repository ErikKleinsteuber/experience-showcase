#!C:\Users\Flat Erik\AppData\Local\Programs\Python\Python37\python.exe

import cgi
import cgitb
import os


cgitb.enable()

formData = cgi.FieldStorage()
name = formData.getvalue('user')
pw = formData.getvalue('pass')

knownUsers = {'erik':'tee', 'nils':'eyesky', 'Melinda':'pip', 'Kinkazu':'poop'}
#
if (name not in knownUsers or pw != knownUsers[name]):
    print('Content-Type: text/html; char-set-utf-8\n')
    print('<html> <body>\n')
    print('<h2>Benutzername oder Passwort falsch!</h2>\n')
    print('</body> </html>\n')
else:
    #check if already online
    onlineUsers = open('C:\\My_stuff\\Studium\\[PYTHON]Skriptsprachen\\UE_11\\python_server\\cgi-bin\\online.txt').readlines()
    userOnline = False
    for user in onlineUsers:
        if user == f"{name}\n":
            userOnline = True

    if userOnline == False:
        #write name to file
        with open('C:\\My_stuff\\Studium\\[PYTHON]Skriptsprachen\\UE_11\\python_server\\cgi-bin\\online.txt','a') as onlineUsers:
            onlineUsers.writelines(f"{name}\n")
        print('<!DOCTYPE html>')
        print('Content-Type: text/html; char-set-utf-8\n')
        print('<html>')
        print('<head>')
        print('<title> Mein Python Chatroom </title>')
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
        print('<br>')
        if (os.path.exists('C:\\My_stuff\\Studium\\[PYTHON]Skriptsprachen\\UE_11\\python_server\\chatlog.txt')):
            chatlog= open('C:\\My_stuff\\Studium\\[PYTHON]Skriptsprachen\\UE_11\\python_server\\chatlog.txt').readlines()
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

            print('</p> </body> </html>')

        #Liste aller online User
        clientList = open('C:\\My_stuff\\Studium\\[PYTHON]Skriptsprachen\\UE_11\\python_server\\cgi-bin\\online.txt').readlines()

        for user in clientList:
            print(f'{user[:-1]}')

    #user is alread online
    else:
        print('Content-Type: text/html; char-set-utf-8\n')
        print('<html> <body>\n')
        print(f'<h2>Benutzer {name} ist leider schon online.</h2>\n')
        print('</body> </html>\n')