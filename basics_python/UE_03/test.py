# dicWithLstAsKey = {[]:2}       #TypeError: unhashable type: 'list'
dicWithLstAsValue = {2: []}  # possible

print(dicWithLstAsValue)

# dicWithDicAsKey = {{}:2}       #TypeError: unhashable type: 'dict'
dicWithDicAsValue = {2: {1: 1}}  # possible

# print(dicWithDicAsKey)
print(dicWithDicAsValue)

# dicWithSetAsKey = {{1,2,3}:2} #TypeError: unhashable type: 'set'
dicWithSetAsValue = {2: {1, 2, 3}}

print(dicWithSetAsValue)  # possible

listWithSet = [{1, 2, 3}]  # possible
print(listWithSet)

listWithDic = [{1: 1}]  # possible
print(listWithDic)

"""
def strToBoolLst(string):
    lst = []
    piece = ""
    for c in string:
        #print("c = " + c)
        #print("piece = " + piece)
        if(c == ","):
            if(piece == "True"):
                lst.append(True)
            else:
                lst.append(False)
            #print(piece)
            piece == ""
        elif(c == " "):
            piece = ""
        elif(c == "]"):
            if(piece == "True"):
                lst.append(True)
            else:
                lst.append(False)
            #print(piece)
        else:
            piece += c

    return lst   

def strToNneLst(string):
    lst = []
    for c in string:
        #print("c = " + c)
        if(c == "o"):
            lst.append(None)

    return lst   

def strToStrLst(string):
    lst = []
    piece = ""
    inStrTwo = False
    inStrOne = False
    for c in string:
        #print("c = " + c)
        #print("piece = " + piece)
        if (inStrOne == False and inStrTwo == False):
            if (c == "'" ):
                inStrOne = True
            elif(c == '"'):
                inStrTwo = True
            elif(c== "," or c == "]"):
                lst.append(piece)
                piece=""
            else:
                piece = ""
        elif(inStrOne == True and c == "'"):
            inStrOne = False
        elif(inStrTwo == True and c == '"'):
            inStrTwo = False
        else:
            piece += c

    return lst

def strToFltLst(string):
    lst = []
    piece = ""
    for c in string:
        #print("c = " + c)
        #print("piece = " + piece)
        if(c == ","):
            lst.append(float(piece))
            piece == ""
        elif(c== "" or c == " "):
            piece = ""
        elif(c== "]"):
            lst.append(float(piece))
        else:
            piece += c

    return lst   

def strToIntLst(string):
    lst = []
    piece = ""
    for c in string:
        #print("c = " + c)
        #print("piece = " + piece)
        if(c == ","):
            lst.append(int(piece))
            piece == ""
        elif(c== "" or c == " "):
            piece = ""
        elif(c== "]"):
            lst.append(int(piece))
        else:
            piece += c

    return lst

def strToLstLst(string):
    lst = []

    bracketCounter = 0
    inStrOne = False
    inStrTwo = False
    piece = ""
    inner = False

    for c in string:
        if (inStrOne == False and inStrTwo == False):
            if (c == "'" ):
                inStrOne = True
            elif(c == '"'):
                inStrTwo = True
            if(c=="["):
                bracketCounter += 1
            if(c=="]"):
                bracketCounter -= 1
        elif(inStrOne == True and c == "'"):
            inStrOne = False
        elif(inStrTwo == True and c == '"'):
            inStrTwo = False
        
        if (bracketCounter>0):
            inner = True
            piece += c
        elif (inner == True):
            #print(piece + "]")

            lst.append(loadListFromString(piece + "]"))

            piece = ""
            inner = False
    
    return lst
        
def loadListFroString(content):

    #hier checken ob vielleicht set oder dict

    if(content[1] == "["):
        #print("strToLstLst")
        return strToLstLst(content[1:-1])
    elif(content[1] == "{"):
        lst = []
        if(decideIfSetOrDic == "set"):
            lst.append(loadSetFromString(content[1:-1]))
            return lst
        else:
            lst.append(loadDicFromString(content[1:-1]))
            return lst
    elif(content[1:5] == "True" or content[1:6] == "False"):
        #print("strToBoolLst")
        return strToBoolLst(content[1:])
    elif(content[1:5] == "None"):
        #print("strToNneLst")
        return strToNneLst(content[1:])
    elif(content[1] == "'" or content[1] == '"'):
        #print("strToStrLst")
        return strToStrLst(content[1:])
    else:
        for c in content[1:-1]:
            if (c == "."):
                #print("strToFltLst")
                return strToFltLst(content[1:])
            elif (c == ","):
                #print("strToIntLst")
                return strToIntLst(content[1:])

def saveList(liste, path):
    with open(path, 'w') as file:
        try:
            file.write(str(liste))
        except:
            print("Failed saving the file. Exiting now...")
"""

"""
print("\nThe List: \n")
testList = loadList(filepath + "intList.txt")
print(str(testList))
print("\nis of type " + str(type(testList[0])))

print("\nThe List: \n")
testList = loadList(filepath + "floatList.txt")
print(str(testList))
print("\nis of type " + str(type(testList[0])))

print("\nThe List: \n")
testList = loadList(filepath + "boolList.txt")
print(str(testList))
print("\nis of type " + str(type(testList[0])))

print("\nThe List: \n")
testList = loadList(filepath + "stringList.txt")
print(str(testList))
print("\nis of type " + str(type(testList[0])))

print("\nThe List: \n")
testList = loadList(filepath + "noneList.txt")
print(str(testList))
print("\nis of type " + str(type(testList[0])))
"""
