from tkinter import *

test = [0, 0, 255]
red = 0
green = 0
blue = 0


# https://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return "#%02x%02x%02x" % (red, green, blue)


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


# TODO: andere Farben und das ganze mehr wie ein experiment aussehen lassen
# TODO: button für fertig mit dem test


def redclicked():
    pass


# button-events
def plusclicked():
    global red

    if red >= 255:
        red = 255
    elif red < 0:
        red = 0
    else:
        red = red + 1

    print(red)

    canvas.itemconfig(leftrec, fill=rgb_to_hex(red, green, blue))
    fenster.update()


def minusclicked():
    global red

    if red > 255:
        red = 255
    elif red <= 0:
        red = 0
    else:
        red = red - 1

    print(red)

    canvas.itemconfig(leftrec, fill=rgb_to_hex(red, green, blue))
    fenster.update()


fenster = Tk()
canvas = Canvas()

# das ist das viereck welches man mit den Buttons einstellen kann
leftrec = canvas.create_rectangle(0, 0, 200, 200, fill=rgb_to_hex(red, green, blue))

# hier ist das vergleichsviereck, da kann man noch einen beliebigen rot-wert setzen (bzw. random bzw. andere Farben etc.)
canvas.create_rectangle(200, 0, 400, 200, fill=rgb_to_hex(125, 0, 0))

# + und - Knopf
plusbtn = Button(fenster, text="+", command=plusclicked)
mnsbtn = Button(fenster, text="-", command=minusclicked)
plusbtn.place(x=80 - 15, y=220, height=30, width=30)
mnsbtn.place(x=120 - 15, y=220, height=30, width=30)

# farbeinstellknöpfe
# redbtn = Button(fenster, text = "red", command = redclicked)

canvas.pack(fill=BOTH, expand=1)

fenster.geometry("640x480")
fenster.mainloop()
