from tkinter import *
import random
import _thread
from threading import Thread

window = Tk()

# set window title
window.wm_title("Bälle")

# fenster dimensionen
window.geometry("600x600")

# canvas zum darstellen der Bälle
c = Canvas(window, height=600, width=600)

# liste zum sammeln der Ovale (und eventuell zum dazuspeichern des speed)
balls = []

# Abstände der Bälle in x-Richtung
lineDistance = 20

for x in range(1, 10):
    size = random.randrange(5, 30)
    height = random.randrange(100, 350)

    # generate random HEX-color
    rndHex = "#" + str(hex(random.randint(1118481, 16777215)))[2:]
    # print(rndHex)

    # ball erstellen
    ball = c.create_oval(
        lineDistance - (size / 2),
        height - (size / 2),
        lineDistance + (size / 2),
        height + (size / 2),
        fill=rndHex,
        outline="",
    )

    # liste füllen
    balls.append([ball, 0.0])

    # Abstände
    lineDistance += 50

print(balls)

# canvas dynamisch packen
c.pack(fill="both", expand=True)


def moveballs():
    global balls

    while True:
        for b in balls:
            # diese Variante mit nur einem Thread, welcher sequentiell alle Bälle simuliert, brauch keinen extra print befehl
            # die bälle werden alle nacheinander abgearbeitet, sind also von vornherein schon synchron
            # warum hier der mainloop nicht freezed weiß ich jetzt auch nicht
            c.move(b[0], 0, b[1])

            # simulierte gravitation
            b[1] += 0.001

            # ermittle Ballgröße
            size = c.coords(b[0])[3] - c.coords(b[0])[1]

            # Boden habe ich mal auf 600 festgelegt
            if c.coords(b[0])[3] >= 600:
                c.coords(b[0], c.coords(b[0])[0], 600 - size, c.coords(b[0])[2], 600)
                b[1] = b[1] * -0.9

            # window.update() -> ganz schlechte Idee


_thread.start_new_thread(moveballs, ())

# wenn ich die mainloop als thread starte, bekomme ich einen fehler <_<, das war laut Internet so von den tkinter Programmierern gewollt
# ne Möglichkeit das zu umgehen habe ich nicht gefunden
window.mainloop()
