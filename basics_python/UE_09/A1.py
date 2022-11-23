from tkinter import *
import datetime
import _thread
from time import sleep
import re

window = Tk()

# set window title
window.wm_title("Digitaluhr")


window.geometry("320x240")

seconds = datetime.datetime.now().second
minutes = datetime.datetime.now().minute
hours = datetime.datetime.now().hour
alarm = -1


def tictac():
    global seconds
    while True:
        sleep(1)
        seconds += 1
        updateClock()


clock = Label(
    window, text=f"{hours}:{minutes}:{seconds}", fg="green", font=("Times", 20)
)

clock.pack()

alarmLabel = Label(window, text="alarm not set yet")
alarmLabel.pack()


def updateClock():

    global seconds, minutes, hours, alarm

    if seconds == 60:
        seconds = 0
        minutes += 1

    if minutes == 60:
        minutes += 1
        hours = 0

    if hours == 24:
        seconds = 0
        minutes = 0
        hours = 0

    secondsdisplay = seconds
    minutesdisplay = minutes
    hoursdisplay = hours

    if seconds < 10:
        secondsdisplay = f"0{seconds}"

    if minutes < 10:
        minutesdisplay = f"0{minutes}"

    if hours < 10:
        hoursdisplay = f"0{hours}"

    clock.configure(text=f"{hoursdisplay}:{minutesdisplay}:{secondsdisplay}")

    print(f"alarm = {alarm}")
    print(f"display = {hoursdisplay}{minutesdisplay}{secondsdisplay}")

    if f"{hoursdisplay}{minutesdisplay}{secondsdisplay}" == alarm:
        print("WAKE UP!")


winp = Entry(window, width=18)
winp.pack()


def adjustAlarm():
    global alarm
    print("pressed button")
    print(winp.get())

    tInp = winp.get()

    if re.findall(r"\d\d\d\d\d\d", str(tInp)):
        if int(tInp[0]) > 2 or int(tInp[2]) > 5 or int(tInp[4]) > 5:
            print("Falsches Format")
            return False

        for digit in tInp:
            if int(digit) < 0:
                print("Falsches Format")
                return False

        print("alarm set succesfully!")
        alarm = tInp
        alarmLabel.configure(
            text=f"alarm at -> {tInp[0]}{tInp[1]}:{tInp[2]}{tInp[3]}:{tInp[4]}{tInp[5]}"
        )


submit = Button(window, text="Enter", width=5, command=adjustAlarm)
submit.pack()

_thread.start_new_thread(tictac, ())

window.mainloop()
