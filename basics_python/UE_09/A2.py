from tkinter import *
import random
import _thread

window = Tk()

# set window title
window.wm_title("Bälle")

# fensterdimensionen
window.geometry("600x600")

# canvas
c = Canvas(window, height=600, width=600)

# liste um die Bälle abzuspeichern für einfachere Abarbeitung
balls = []

for x in range(random.randrange(4, 20)):
    size = random.randrange(5, 30)

    rndHex = "#" + str(hex(random.randint(1118481, 16777215)))[2:]
    # print(rndHex)

    ball = c.create_oval(
        300 - (size / 2),
        300 - (size / 2),
        300 + (size / 2),
        300 + (size / 2),
        fill=rndHex,
        outline="",
    )
    balls.append(ball)

# macht dass das canvas sich automatisch an die fenstergröße anpasst
c.pack(fill="both", expand=True)


def moveBalls():
    global balls

    # da ein thread hier alle Bälle simuliert, indem er über die Liste iteriert, kommen keine unterschiedlichen Bewegungsgeschwindigkeiten zustande
    # allerdings werden die Bälle aufgrund ihrer unterschiedlichen Größe und eventuellen Rundungsfehlern, nicht im gleichen Moment zurückgesetzt,
    # deswegen bewegen sie sich unterschiedlich schnell. Als Rücksetzpunkt wurde der Mittelpunkt des Kreises gewählt. Überschreitet dieser
    # die Screenborder (egal ob horizontal oder vertikal), so wird der Ball in die relative Mitte zurückgesetzt.
    while True:
        for b in balls:

            # Bewegungsrichtung

            # die pseudo random number generation scheint ziemlich stark in die negativen Werte abzudriften. Praktisch alle Kugeln tendieren zur linken oberen Ecke
            # wenn man von -4,5 oder wählt scheint es zufälliger zu sein
            c.move(b, random.randrange(-4, 5), random.randrange(-4, 5))

            # c.move(b,2,2)

            # größe des aktuell betrachteten balles (da es eine statische Größe ist könnte man diese auch mit in die Liste abspeichern)
            size = (c.coords(b)[2] - c.coords(b)[0]) / 2

            # out of border
            if (
                (c.coords(b)[0] + size / 2) > window.winfo_width()
                or (c.coords(b)[1] + size / 2) > window.winfo_height()
                or (c.coords(b)[0] + size / 2) < 0
                or (c.coords(b)[1] + size / 2) < 0
            ):

                # setze ball in die Mitte zurück
                c.coords(
                    b,
                    window.winfo_width() / 2 - size,
                    window.winfo_height() / 2 - size,
                    window.winfo_width() / 2 + size,
                    window.winfo_height() / 2 + size,
                )


def moveBall(b):
    while True:
        # Bewegungsrichtung
        # c.move(b,random.randrange(-5,5),random.randrange(-5,5))
        c.move(b, 3, 3)
        # größe des aktuell betrachteten balles (da es eine statische Größe ist könnte man diese auch mit in die Liste abspeichern)
        size = (c.coords(b)[2] - c.coords(b)[0]) / 2

        # out of border
        if (
            (c.coords(b)[0] + size / 2) > window.winfo_width()
            or (c.coords(b)[1] + size / 2) > window.winfo_height()
            or (c.coords(b)[0] + size / 2) < 0
            or (c.coords(b)[1] + size / 2) < 0
        ):

            # setze ball in die Mitte zurück
            c.coords(
                b,
                window.winfo_width() / 2 - size,
                window.winfo_height() / 2 - size,
                window.winfo_width() / 2 + size,
                window.winfo_height() / 2 + size,
            )


_thread.start_new_thread(moveBalls, ())

# für jeden Ball einen Thread aufzumachen scheint wieder nicht allzu dufte zu funktionieren...
# es hängt sich praktisch jedes mal die mainloop auf, das programm und fenster freezen...
# for b in balls:
#    _thread.start_new_thread(moveBall,(b,))

window.mainloop()
