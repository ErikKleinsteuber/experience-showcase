import os
import re

testpath = "C:/My_stuff/Studium/[PYTHON]Skriptsprachen/UE_05/testdir_A2"


def file_search(path, pattern):

    walker = os.walk(path)
    flPaths = []
    for element in walker:
        #    print(element[2])                                              #files-list
        for datei in element[2]:
            if bool(re.findall(pattern, datei)):  # boolean ist überflüssig
                # print(f"{datei}")                                      #file
                # print(element[0])                                      #path
                tPath = (
                    element[0].replace("/", "\\") + "\\" + datei
                )  # concatenating path and file
                flPaths.append(tPath)

    return flPaths


for path in file_search(testpath, "peter"):
    print(path)
