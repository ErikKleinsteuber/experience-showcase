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
c['frage3'] = subject

x = SimpleCookie()
x.load(os.environ['HTTP_COOKIE'])
#x.load('HTTP_COOKIE')
#print(x)
print(x['frage1'].value())
print(x['frage2'].value())
print(x['frage3'].value())
print('<!DOCTYPE html>')
print('Content-Type: text/html; char-set-utf-8\n')
print('<html>')
print('<head>')
print('<title> Mein Python Chatroom </title>')
print('</head>')
print('<html> <body>\n')
print(f'<h2>{x}</h2>\n')
print('</body> </html>\n')