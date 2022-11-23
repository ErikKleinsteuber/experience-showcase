import os
import sys
from operator import itemgetter

# sysargs

help = False
dir = False
sort = False
folder = False
fles = False
path = "."
flsLst = []

for argument in sys.argv:
    # print(argument)

    if help:
        break

    if dir:
        path = argument
        dir = False

    if argument == "-help":
        help = True
    if argument == "-dir":
        dir = True
    if argument == "-sort":
        sort = True
    if argument == "-folder":
        folder = True
    if argument == "-file":
        fles = True

if help:
    # print help text here and close program afterwards

    # HELPTEXT
    print(
        "Welcome Newbee ( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°). You've stumbled upon some dank python script here. \n\nFunctioning as follows: \n"
    )
    print(
        "You open your console at the directory and run this script as usual via the commans 'python listfiles.py'."
    )
    print(
        "So far so good. After the listfiles.py you can also do a blankspace and send some fancy arguments on the way."
    )
    print(
        "I assume you already know the -help command bcs otherwise you would not see this message here. ƪ(˘⌣˘)ʃ\n"
    )
    print(
        "-dir is another argument to which a valid path of your system has to follow. Otherwhise there will be furios errors. So take care ╚(ಠ_ಠ)=┐ !!"
    )
    print(
        "If -dir is not set, the script will show the content of the directory it is currently run in. \n"
    )
    print(
        "-fles and -folder will either only list the files (-fles) or the directorys/folder (-folder) of the path. This one is self explanatory. \n"
    )
    print(
        "And finally -sort will sort all listing according to their creation date (starting with the oldest). \n"
    )
    print("Hope you are prepared now young traveller. CYA ^̮^")

    # close program
    sys.exit(0)

# logic

hlpLst = []
if sort:
    for element in os.listdir(path):
        hlpLst.append([element, os.path.getmtime((f"{path}/{element}"))])

    hlpLst = sorted(hlpLst, key=itemgetter(1))

    for element in hlpLst:
        flsLst.append(element[0])
else:
    flsLst = os.listdir(path)


for element in flsLst:

    # nur Dateien
    if fles:
        if os.path.isfile(f"{path}/{element}"):
            print(element)
    elif folder:
        if os.path.isdir(f"{path}/{element}"):
            print(element)
    else:
        print(element)
