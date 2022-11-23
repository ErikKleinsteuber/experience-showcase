#!C:\Users\Flat Erik\AppData\Local\Programs\Python\Python37\python.exe

import cgi
import cgitb
import os

cgitb.enable()
print('<!DOCTYPE html>')
print('Content-Type: text/html; char-set-utf-8\n')
print('<html>')
print('<head>')
print('<title> Mein Python Chatroom </title>')
print('</head>')
print('<body>')
print('<form action = "/cgi-bin/frage2.py" method = "post" target = "_blank">')
print('<h3>Welches der beiden Fächer mögen sie lieber?</h3>')
print('<input type = "radio" name = "subject" value = "Mathematik" /> Mathematik')
print('<input type = "radio" name = "subject" value = "Physik" /> Physik')
print('<input type = "submit" value = "Select Subject" />')
print('</form>')
print('</body>')
print('</html>')