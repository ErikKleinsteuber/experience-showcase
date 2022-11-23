import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

import tkinter as tk


def sendMail():
    global userNameInpt, pw, frmInpt, toInpt, messageField, subjInpt

    # text = MIMEText(body).as_string()
    # print(f"Username: {userNameInpt.get()}")

    # s = smtplib.SMTP('localhost')
    s = smtplib.SMTP("mail.gmx.net")  # Port = 587
    # s = smtplib.SMTP('smtp.uni-jena.de')
    message = f"""
    From: From Person <{frmInpt.get()}> 
    To: To Person <{toInpt.get()}> 
    Subject: {subjInpt.get()} 
    {messageField.get("1.0","end-1c")}"""

    print(message)

    s.sendmail(f"{frmInpt.get()}", [f"{toInpt.get()}"], message)
    s.quit()


root = tk.Tk()

title = tk.Label(root, text="Email Programm")
title.grid(row=0, column=0)

userName = tk.Label(root, text="Username: ")
userName.grid(row=1, column=0)

userNameInpt = tk.Entry(root)
userNameInpt.grid(row=1, column=1)

pwLbl = tk.Label(root, text="Password: ")
pwLbl.grid(row=2, column=0)

pw = tk.Entry(root, show="*")
pw.grid(row=2, column=1)

fromLbl = tk.Label(root, text="From: ")
fromLbl.grid(row=3, column=0)

frmInpt = tk.Entry(root)
frmInpt.grid(row=3, column=1)

toLbl = tk.Label(root, text="To: ")
toLbl.grid(row=4, column=0)

toInpt = tk.Entry(root)
toInpt.grid(row=4, column=1)

subj = tk.Label(root, text="Subject: ")
subj.grid(row=6, column=0)

subjInpt = tk.Entry(root)
subjInpt.grid(row=6, column=1)

msgLbl = tk.Label(root, text="Message: ")
msgLbl.grid(row=7, column=0)

messageField = tk.Text(root, height=20, width=50)
messageField.grid(row=7, column=1)

sendButton = tk.Button(root, text="Send E-Mail", command=sendMail)
sendButton.grid(row=8, column=0)

root.mainloop()

# AB HIER THREADEN
"""
body = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx xxxxxxxx\r\nyyyyyyy"
#text = "Subject: missing newline\r\n\r\n" + body
text = MIMEText(body).as_string()

s = smtplib.SMTP('localhost')

message = "From: From Person <erikkleinsteuber@googlemail.com> To: To Person <erikkleinsteuber@googlemail.com> Subject: SMTP e-mail test This is a test e-mail message."

s.sendmail('erikkleinsteuber@googlemail.com', ['erikkleinsteuber@googlemail.com'], message)
s.quit()
"""
