#!C:\Users\Flat Erik\AppData\Local\Programs\Python\Python37\python.exe

import cgi
import cgitb
import os
from http.cookies import SimpleCookie

cgitb.enable()

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
if form.getvalue('subject'):
   subject = form.getvalue('subject')
else:
   subject = "Not set"

c = SimpleCookie()
c['frage1'] = subject
#muss in den html teil

#print('<!DOCTYPE html>')
print('Content-Type: text/html; char-set-utf-8\n')
print('<html>')
print('<head>')
print('<title> Mein Python Chatroom </title>')
print('</head>')
print('<body>')
print('<form action = "/cgi-bin/frage3.py" method = "post" target = "_blank">')
print('<h3>Welches der beiden Fächer mögen sie lieber?</h3>')
print('<input type = "radio" name = "subject" value = "Ethik" /> Ethik')
print('<input type = "radio" name = "subject" value = "Religion" /> Religion')
print('<input type = "submit" value = "Select Subject" />')
print('</form>')
print('</body>')
print('</html>')