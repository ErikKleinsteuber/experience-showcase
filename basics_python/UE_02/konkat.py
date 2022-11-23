def konkat(*string):
    sumOfStrings = ""
    for x in string:
        try:
            sumOfStrings += x
        except Exception:
            print("error: unable to convert to String")
    print(sumOfStrings)


konkat("hi", "hihi", " <- dreimalhi", " und ", "drei mal ha: ", " ha ha ha ")
