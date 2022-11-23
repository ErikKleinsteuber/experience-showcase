import re

file_object = open(
    "C:/My_stuff/Studium/[PYTHON]Skriptsprachen/UE_04/python_website.html", "r"
)

webLink = re.compile(r"www.(\S)*|http(s)?:(\S)*")
webLinkList = []

pythonCounter = 0
pthnCdeLneCounter = 0
picLinkCounter = 0

for line in file_object:

    # jeder match in jeder line zaehlt den pythonCounter hoch
    for x in re.finditer("python", line, re.IGNORECASE):
        pythonCounter += 1

    # adde je ein match (weblink) zu der weblinkliiste hinzu
    for x in re.finditer(webLink, line):
        # das group(0) sorgt hierbei dafuer dass nicht das match-object, sondern
        # der darin enthaltene String in die Liste abgespeichert wird
        webLinkList.append(x.group(0))

    # zaehlt die lines of python code, ist aber leider fehlerhaft <_<
    # habe auch nicht wirklich eine Idee wie ich das anders machen soellte
    # >>> oder ... ist der indikator für die python code zeilen
    if re.match("&gt;", line) != None:
        pthnCdeLneCounter += 1

    # zaehlt die .png Vorkommen, das kann man auch akkurater machen, aber hat zu Problemen gefuehrt <_<...
    # sehr naiver Ansatz
    for x in re.finditer(r".png", line, re.IGNORECASE):
        picLinkCounter += 1

print(f"Das Wort Python kommt {pythonCounter} mal vor.")
print(f"Es kommen insgesamt {pthnCdeLneCounter} Zeilen PythonCode vor.")
print(f"Es kommen insgesamt {picLinkCounter} Bildlinks vor.")

# da es ein paar viele webLinks sind, have ich die Zeile mal auskommentiert
# print(f"Hier sind alle weblinks:\n\n {webLinkList} \n")

# Anzahl webLinks
# print(len(webLinkList))

# schoenerer print der webLinks
# print die Liste aller Weblinks
# for x in webLinkList:
#    print(x)
