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
    balls.append(ball)

    # Abstände
    lineDistance += 50

# canvas dynamisch packen
c.pack(fill="both", expand=True)


def moveball(ball):
    speed = 0.0
    while True:
        # wenn man dieses print auskommentiert, funktioniert auf magische art und weise nichts mehr (weil dann anscheinend der mainloop festhängt)
        print("lol")
        c.move(ball, 0, speed)

        # simulierte gravitation
        speed += 0.001
        size = c.coords(ball)[3] - c.coords(ball)[1]
        # print(speed)
        if c.coords(ball)[3] >= 600:
            c.coords(ball, c.coords(ball)[0], 600 - size, c.coords(ball)[2], 600)
            speed = speed * -0.9

        # window.update() -> ganz schlechte Idee


# die threads wirken alle schon ziemlich synchron, aber ich habe nichts dafür getan, also ist das ja praktisch gar nicht möglich
# eigentlich sollte man hier eine priority queue ansetzen wenn mich nicht alles täuscht
dreads = []
for b in balls:
    dreads.append(Thread(target=moveball, args=([b]), daemon=True))

for dread in dreads:
    dread.daemon = True
    dread.start()
    # dread.join()   #-> bringt random Fehler mit sich die ich nicht gefixed bekomme

# wenn ich die mainloop als thread starte, bekomme ich einen fehler <_<, das war laut Internet so von den tkinter Programmierern gewollt
# ne Möglichkeit das zu umgehen habe ich nicht gefunden
window.mainloop()
