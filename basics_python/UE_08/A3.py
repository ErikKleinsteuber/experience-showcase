from tkinter import *


dollarOut = 0
pfundOut = 0
bitcoinOut = 0

fenster = Tk()


def rechneclicked():
    betrag = float(inp.get())

    global dollarOut, pfundOut, bitcoinOut

    dollarOut = 0.8974 * betrag
    pfundOut = 0.8330 * betrag
    bitcoinOut = 6382.18 * betrag  # korrigieren

    dollar.configure(text=dollarOut)
    pfund.configure(text=pfundOut)
    bitcoin.configure(text=bitcoinOut)

    fenster.update()  # unnötig


inp = Entry(fenster, bd=3)
inp.place(x=20, y=20)

# button fürs Rechnen
rechnebtn = Button(fenster, text="Rechne", command=rechneclicked)
rechnebtn.place(x=200, y=20)

# DOllar
dlr = Label(fenster, text="dollar")
dlr.place(x=20, y=50)

dollar = Label(fenster, text=dollarOut)
dollar.place(x=100, y=50)

# Pfund
pnd = Label(fenster, text="pfund")
pnd.place(x=20, y=100)

pfund = Label(fenster, text=pfundOut)
pfund.place(x=100, y=100)

# Bitcoin
btc = Label(fenster, text="bitcoin")
btc.place(x=20, y=150)

bitcoin = Label(fenster, text=bitcoinOut)
bitcoin.place(x=100, y=150)


fenster.geometry("640x480")
fenster.mainloop()
