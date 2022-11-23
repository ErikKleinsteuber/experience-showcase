filepath = "C:/My_stuff/Studium/[PYTHON]Skriptsprachen/UE_03/files/"
zeroToNine = "0123456789"

# region EXPLANATION OF THE CODE:
"""


First you save a list/set/dic to a path. Then you load that specific type again via loadList(yourpath), 
loadSet or loadDic (easily managable to write a function which decides that for you but anyways).
You pick the specific function to load and it returns you a correctly parsed version of the files content
given the right types in it.

loadList(path), loadSet(path), loadDic(path) all work quite the same. The following variables
are important:

    inStrOne        -> Boolean              == We are in a 'content' type of String if True
    inStrTwo        -> Boolean              == We are in a "content" type of String if True
    piece           -> String (at first)    == helper variable to concatenate string parts
                                               is used to create the elements of our collection
    inList          -> Boolean              == we are currently in a List if True           (= [...])
    inSetOrDic      -> Boolean              == we are currently in a Set of Dic if True     (= {...})
    bracketCounter  -> int                  == counts the brackets ('[',']','{','}') specificly
    numbi           -> Boolean              == we are currently constructing an Integer element if True
    deci            -> Boolean              == we are currently constructing an Float element if True

Every of the three functions intializes a new empty one of its return kinds and fills them step by
step with the parsed elements. We iterate over every character given in the String parameter
and depending on our variables the way the loop continues changes. (case differentiation)

Saving and Printing parts should be self explainable.

"""
# endregion


def save(string, path):
    with open(path, "w") as file:
        try:
            file.write(str(string))
        except Exception:
            print("Failed saving the file. Exiting now...")


def loadList(path):
    file = open(path, "r")
    content = file.read()

    return loadListFromString(content)


def loadSet(path):
    file = open(path, "r")
    content = file.read()

    return loadSetFromString(content)


def loadDic(path):
    file = open(path, "r")
    content = file.read()

    return loadDicFromString(content)


def loadSetFromString(content):
    # print(content)
    ourSet = set()
    piece = ""
    deci = False
    numbi = False
    inStrOne = False
    inStrTwo = False

    # print("Content = " + content)

    for c in content[1:]:
        # print("piece = " + piece)
        if inStrOne is False and inStrTwo is False:  # not in a String

            if deci is True:
                if c == "," or c == "}":
                    ourSet.add(float(piece))
                    deci = False
                    numbi = False
                else:
                    piece += c
            elif numbi is True:
                if c == "," or c == "}":
                    ourSet.add(int(piece))
                    numbi = False
                elif c == ".":
                    deci = True
                    piece += c
                else:
                    piece += c
            elif c == "'":
                inStrOne = True
            elif c == '"':
                inStrTwo = True
            elif c == " ":
                piece = ""
            elif c == ".":
                deci = True
            elif c in zeroToNine:
                numbi = True
                piece += c
            elif c == ",":  # new Element
                piece = ""
            else:
                piece += c

            if piece == "None":
                ourSet.add(None)
                piece = ""
            elif piece == "True":
                ourSet.add(True)
                piece = ""
            elif piece == "False":
                ourSet.add(False)
                piece = ""

        elif inStrOne is True and c == "'":
            inStrOne = False
            ourSet.add(piece)
            piece = ""
        elif inStrTwo is True and c == '"':
            inStrTwo = False
            ourSet.add(piece)
            piece = ""
        else:  # you're in a String
            piece += c

    return ourSet


def loadListFromString(content):
    lst = []
    inStrOne = False
    inStrTwo = False
    piece = ""
    inList = False
    inSetOrDic = False
    bracketCounter = 0
    numbi = False
    deci = False

    for c in content[1:]:
        if inStrOne is False and inStrTwo is False:  # not in a String

            if bracketCounter > 0:
                piece += c
                # print("piecex = " + piece)
                if inList is True:
                    if c == "[":
                        bracketCounter += 1
                    elif c == "]":
                        bracketCounter -= 1
                    if bracketCounter == 0:
                        lst.append(loadListFromString(piece))
                        inList = False
                elif inSetOrDic is True:
                    if c == "{":
                        bracketCounter += 1
                    elif c == "}":
                        bracketCounter -= 1
                    if bracketCounter == 0:
                        if decideIfSetOrDic(piece) == "set":
                            # print("Set load with " + piece)
                            lst.append(loadSetFromString(piece))
                            inSetOrDic = False
                        else:
                            lst.append(loadDicFromString(piece))
                            inSetOrDic = False
            elif deci is True:
                if c == "," or c == "]":
                    lst.append(float(piece))
                    deci = False
                    numbi = False
                    piece = ""
                else:
                    piece += c
            elif numbi is True:
                if c == "," or c == "]":
                    lst.append(int(piece))
                    numbi = False
                    piece = ""
                elif c == ".":
                    deci = True
                    piece += c
                else:
                    piece += c
            elif piece == "True":
                lst.append(True)
                piece = ""
            elif piece == "None":
                lst.append(None)
                piece = ""
            elif piece == "False":
                lst.append(False)
                piece = ""
            elif c == "'":
                inStrOne = True
            elif c == '"':
                inStrTwo = True
            elif c == "{":
                inSetOrDic = True
                piece += c
                bracketCounter += 1
            elif c == "[":
                inList = True
                bracketCounter += 1
                piece += c
            elif c == ".":
                deci = True
                piece += c
            elif c in zeroToNine:
                numbi = True
                piece += c
            elif c == ",":
                # value = piece  #SUSSSSSPICIOUS
                piece = ""
            elif c == " ":
                piece = ""
            else:
                piece += c
        elif inStrOne is True and c == "'":
            inStrOne = False
            if inList is True or inSetOrDic is True:
                piece += c
            else:
                lst.append(piece)
        elif inStrTwo is True and c == '"':
            inStrTwo = False
            if inList is True or inSetOrDic is True:
                piece += c
            else:
                lst.append(piece)
        else:
            piece += c

        # print("bracketCounter = " + str(bracketCounter))
        # print("piece = " + piece)

    return lst


def loadDicFromString(content):

    dic = {}
    inStrOne = False
    inStrTwo = False
    piece = ""
    inList = False
    inSetOrDic = False
    bracketCounter = 0
    numbi = False
    deci = False
    key = ""
    value = ""

    for c in content[1:]:

        if inStrOne is False and inStrTwo is False:  # not in a String

            if bracketCounter > 0:
                piece += c
                # print("piecex = " + piece)
                if inList is True:
                    if c == "[":
                        bracketCounter += 1
                    elif c == "]":
                        bracketCounter -= 1
                    if bracketCounter == 0:
                        value = loadListFromString(piece)
                elif inSetOrDic is True:
                    if c == "{":
                        bracketCounter += 1
                    elif c == "}":
                        bracketCounter -= 1
                    if bracketCounter == 0:
                        if decideIfSetOrDic(piece) == "set":
                            # print("Set load with " + piece)
                            value = loadSetFromString(piece)
                        else:
                            value = loadDicFromString(piece)
            elif deci is True:
                if c == "," or c == "}":
                    value = float(piece)
                    deci = False
                    numbi = False
                    piece = ""
                elif c == ":":
                    key = float(piece)
                    piece = ""
                    deci = False
                    numbi = False
                else:
                    piece += c
            elif numbi is True:
                if c == "," or c == "}":
                    value = int(piece)
                    numbi = False
                    piece = ""
                elif c == ":":
                    key = int(piece)
                    piece = ""
                    numbi = False
                elif c == ".":
                    deci = True
                    piece += c
                else:
                    piece += c
            elif piece == "True":
                if key == "":
                    key = True
                    piece = ""
                else:
                    value = True
                    piece = ""
            elif piece == "None":
                if key == "":
                    key = None
                    piece = ""
                else:
                    value = None
                    piece = ""
            elif piece == "False":
                if key == "":
                    key = False
                    piece = ""
                else:
                    value = False
                    piece = ""
            elif c == "'":
                inStrOne = True
            elif c == '"':
                inStrTwo = True
            elif c == "{":
                inSetOrDic = True
                piece += c
                bracketCounter += 1
            elif c == "[":
                inList = True
                bracketCounter += 1
                piece += c
            elif c == ".":
                deci = True
                piece += c
            elif c in zeroToNine:
                numbi = True
                piece += c
            elif c == ",":
                value = piece
                piece = ""
            elif c == ":":
                key = piece
                piece = ""
            elif c == " ":
                piece = ""
            else:
                piece += c
        elif inStrOne is True and c == "'":
            inStrOne = False
            if inList is True or inSetOrDic is True:
                piece += c
            else:
                if key == "":
                    key = piece
                else:
                    value = piece
        elif inStrTwo is True and c == '"':
            inStrTwo = False
            if inList is True or inSetOrDic is True:
                piece += c
            else:
                if key == "":
                    key = piece
                else:
                    value = piece
        else:
            piece += c

        if key != "" and value != "":

            try:
                # print("Key: " + str(key) + " Value: " + str(value))
                dic[key] = value
                key = ""
                value = ""
                piece = ""
                deci = False
                numbi = False
                inList = False
                inSetOrDic = False
            except Exception:
                pass

        # print("bracketCounter = " + str(bracketCounter))
        # print("piece = " + piece)

    return dic


def decideIfSetOrDic(string):
    inStrOne = False
    inStrTwo = False
    for c in string:

        if inStrOne is False and inStrTwo is False:
            if c == "'":
                inStrOne = True
            elif c == '"':
                inStrTwo = True
            elif c == ":":
                return "dic"
        elif inStrOne is True and c == "'":
            inStrOne = False
        elif inStrTwo is True and c == '"':
            inStrTwo = False

    return "set"


# region initialization
# Integer, Float, String, Bool, None, List, Set, Dictionary

# lists can save dictionaries as well as sets and all the other data types (as well as lists in lists)
# testListInteger = [0,1,2,3,4,6,7,8]
# testListFloat = [0.1,0.2,0.3,0.4,0.6,0.7,0.8]
# testListString = ["1","2","3",",,,,,,''''''''4",'6"-"-"""""""""""-""""<O.o_o.o_o.O>""""""-',"7","8"]
# testListBoolean = [True,True,True,False,True,False]
# testListNone = [None,None,None]

testList = [
    [1, 2],
    [3, 4],
    [5, 6],
    [[4, 4, 4], [5, 5]],
    [[[[42, 42]]]],
    {1, 2, 3},
    {1: "hallo"},
    "''HALLO'",
    '">-<"',
    1,
    True,
    False,
    None,
    1.555,
]

# the ultimate testList <_<
# testListSuperList = [[[testListInteger, testListFloat, testListString, testListBoolean, testListNone, [testList]]]]

# set can not save lists nor dics nor itself (sets)
testSet = {10, True, 2, 3, "True False None", "''''", '""""', False, None, 1.555}

testDic = {
    True: 1,
    2: 2,
    3: 3,
    False: 5,
    None: None,
    6: False,
    4: True,
    "Hallo": "Goodbye",
    "'''''": '""',
    "Float:": 1.555,
    "List: ": [[[1, 2, 3]]],
    "Set: ": {1, 2, 3},
    "Dic: ": {"Dic": {"Dic": {}}},
    1.556: 1.666,
}
# endregion

# region Test set and dict for hashability of the different data types (no running code here)
# setWithList = {[],2,3,4}
# TypeError: unhashable type: 'list'

# setWithDict = {{},2,3,4}
# TypeError: unhashable type: 'dict'

# dicWithLstAsKey = {[]:2}       #TypeError: unhashable type: 'list'
# dicWithLstAsValue = {2:[]}     #possible

# print(dicWithLstAsValue)

# dicWithDicAsKey = {{}:2}       #TypeError: unhashable type: 'dict'
# dicWithDicAsValue = {2:{}}     #possible

# print(dicWithDicAsKey)
# print(dicWithDicAsValue)

# dicWithSetAsKey = {{1,2,3}:2}  #TypeError: unhashable type: 'set'
# dicWithSetAsValue = {2:{1,2,3}}#possible

# print(dicWithSetAsValue)

# dictionaries can take sets, but not lists and also not itself
# dic = {{}:{}}

# listWithSet = [{1,2,3}]         #possible
# print(listWithSet)

# listWithDic = [{1:1}]           #possible
# print(listWithDic)

# endregion

# region Saving Lists,Sets,Dics for the first time
# saveList(testListInteger, filepath + "intList.txt")
# saveList(testListFloat, filepath + "floatList.txt")
# saveList(testListString, filepath + "stringList.txt")
# saveList(testListBoolean, filepath + "boolList.txt")
# saveList(testListNone, filepath + "noneList.txt")
save(testList, filepath + "testList.txt")

save(testSet, filepath + "testSet.txt")

save(testDic, filepath + "testDic.txt")
# endregion

# region Loading and printing as well as printing the types

print("\nThe List: \n")
lstLoaded = loadList(filepath + "testList.txt")
print(str(lstLoaded))
print("\nis of type " + str(type(lstLoaded[0])))

for element in lstLoaded:
    print("The element " + str(element) + " is of type " + str(type(element)))


print("\nThe Set: \n")
setLoaded = loadSet(filepath + "testSet.txt")
print(str(setLoaded))
print("\nis an unordered collection of unique items <_<! following right now: \n")

for element in setLoaded:
    print("The element " + str(element) + " is of type " + str(type(element)))

print("\nThe Dic: \n")
dicLoaded = loadDic(filepath + "testDic.txt")
print(dicLoaded)
print(
    "\nis a collection which is unordered, changeable and indexed."
    + "It contains key value pairs with the following data types: "
)

for key, value in dicLoaded.items():
    print(
        "key "
        + str(key)
        + " has datatype "
        + str(type(key))
        + ". value "
        + str(value)
        + " has datatype "
        + str(type(value))
        + ". "
    )

# endregion

# region advanced Testing
"""
ultraDic = {1:setLoaded,2:lstLoaded, 3:dicLoaded}
ultraLst = [setLoaded,lstLoaded,dicLoaded]

save(ultraDic, filepath + "ultraDic.txt")
save(ultraLst, filepath + "ultraLst.txt")

uDicLoaded = loadDic(filepath + "ultraDic.txt")

print("\nThe List: \n")
uLstLoaded = loadList(filepath + "ultraLst.txt")
print(str(uLstLoaded))
print("\nis of type " + str(type(uLstLoaded[0])))

for element in uLstLoaded:
    print("The element " + str(element) + " is of type " + str(type(element)))

print("\nThe Dic: \n")
uDicLoaded = loadDic(filepath + "ultraDic.txt")
print(uDicLoaded)
print("\nis a collection which is unordered, changeable and indexed." + 
    "It contains key value pairs with the following data types: ")

for key, value in uDicLoaded.items():
    print("key " + str(key) + " has datatype " + 
    str(type(key)) + ". value " + str(value) + " has datatype " + str(type(value)) + ". ")
"""
# endregion
