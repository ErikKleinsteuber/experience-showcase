from tkinter import *

red = 0
green = 0
blue = 0
fenster = Tk()

# https://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return "#%02x%02x%02x" % (red, green, blue)


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def refreshclicked():

    global red, green, blue

    red = int(redEntry.get())
    green = int(greenEntry.get())
    blue = int(blueEntry.get())

    fenster.configure(background=rgb_to_hex(red, green, blue))


redLabel = Label(fenster, text="RED")
redLabel.place(x=0, y=20)
redEntry = Entry(fenster, bd=3)
redEntry.place(x=50, y=20)

greenLabel = Label(fenster, text="GREEN")
greenLabel.place(x=0, y=50)
greenEntry = Entry(fenster, bd=3)
greenEntry.place(x=50, y=50)

blueLabel = Label(fenster, text="BLUE")
blueLabel.place(x=0, y=80)
blueEntry = Entry(fenster, bd=3)
blueEntry.place(x=50, y=80)

refreshbtn = Button(fenster, text="Refresh", command=refreshclicked)
refreshbtn.place(x=20, y=110, height=30, width=30)

fenster.configure(background=rgb_to_hex(red, green, blue))

fenster.geometry("640x480")
fenster.mainloop()
