import random


def verstecken(s, n):
    ucLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = s.upper()

    print("Uppercase:")
    print(s + "\n")

    newString = ""

    for x in range(len(s)):

        adding = ""
        for y in range(n):
            adding += ucLetters[random.randint(0, 25)]

        # print("adding = " + adding)
        # print("x = " + str(x))
        # print(s[:x].lstrip() + s[x] + adding + s[x+1:].rstrip())

        newString += s[x] + adding

    print(newString)


verstecken("Hi my name is BMO.", 3)
