import re

file_object = open(
    "C:/My_stuff/Studium/[PYTHON]Skriptsprachen/UE_04/GeschichteMathe.html",
    "r",
    encoding="utf-8",
)
# file_object  = open("C:/My_stuff/Studium/[PYTHON]Skriptsprachen/UE_04/Frauenininfo.html", "r", encoding = 'utf-8')

innerText = False
inBrckt = False
plainText = ""
words = {}
wordCounter = 0
sentenceCounter = 0
yearCounter = 0

# iterating over our loaded html page
for line in file_object:
    # splits the whole page sensitive to the html bracketing
    # authours note: (something like <a <...> > would probably kill the algorithm)
    for part in re.split("(<[^>]*>)", line):

        # checks if we are leaving a plain-Text area of the html file
        # if so -> innerText = False
        if re.match("</p>", part):
            innerText = False

        if innerText == True:

            try:
                # check if we are in a html bracket while innerText == True
                # if so -> inBrckt = True
                if part[0] == "<" and part[1] != "p":
                    inBrckt = True
            except Exception:
                pass  # Das Bööööööööse, aber den Fehler brauch man nicht abfangen

            # if we are not in a html Bracket, then we actually read plain Text from the page
            # so let's do some working in here
            if not inBrckt:
                # splits to every word in our part and iterates over them
                for word in part.split(" "):

                    # counts sentences (naively)
                    if "." in word:
                        sentenceCounter += 1

                    # counts dates (naively)
                    if re.match(r"\d\d\d\d", word):
                        yearCounter += 1

                    # here we remove all non alpha characters from the string and build a new
                    # only alpha character-String from it, which we save to our dic
                    wordAltered = "".join(re.findall("[a-zA-Z]+", word))

                    # save to dic
                    if wordAltered.isalpha() and wordAltered != "":
                        # save
                        if part not in words.keys():
                            words[wordAltered] = 1
                            wordCounter += 1
                        # or count up if already saved earlier
                        else:
                            words[wordAltered] += 1

            # just a helper boolean, could have been also a single if-statement, but i thought
            # that would have become to messy
            inBrckt = False

        # checks if we enter a plain-Text area of the html file
        # if so -> innerText = True
        if re.match("<p>", part):
            innerText = True

# dic for our most frequently used Nouns/Substantives
mstFrqSubs = {}

# helper string for checking if the word we are looking at
# is more frequently used than the "smalles" one in mstFrqSubs
smallest = ""

# iterate over our counted words
for word in words.keys():

    # check if begins with upperCase (naively for == noun)
    if str(word[0]).isupper():

        # just save the first 10
        if len(mstFrqSubs) < 10:
            mstFrqSubs[word] = words[word]
        # after saving the first 10
        else:
            # get the lessest counter one in mstFrqSubs
            for lessMstFrqWord in mstFrqSubs:
                if smallest == "":
                    smallest = lessMstFrqWord
                elif mstFrqSubs[smallest] > mstFrqSubs[lessMstFrqWord]:
                    smallest = lessMstFrqWord

            # if the word we are looking at, is counter more often than the
            # smallest in mstFrqSubs -> replace it
            if words[word] > mstFrqSubs[smallest]:
                del mstFrqSubs[smallest]
                mstFrqSubs[word] = words[word]
                smallest = ""

print(f"We have counted {wordCounter} words (with repitition).")
print(f"We have {len(words)} entries in our dictionary (without repitition).")
print(f"We have {sentenceCounter} sentences on our page.")
print(f"Therefore we have an average sentence length of {wordCounter/sentenceCounter}")
print(f"Our page is {(len(words)/wordCounter)*100}% versatile")
print(f"There are {yearCounter} dates mentioned in the text (with repition).")
print()
print(
    f"The following dictionary shows the most frequently used nouns:\n\n {mstFrqSubs}\n"
)


"""
TODO: Fragen stellen. 
    Frage 1: Warum ist (x) ein anderer regex als x
    Frage 2: Warum matched re.match(r'\d\d\d\d', word) die Zahl 40000 oder 1950ern oder oder oder...
        es gehen auch überlappende matches, und er gibt 40000 zurück weil \d\d\d\d darin eindeutig vorhanden ist
    Frage(n) 3:

    [^]
    (\.|\S)*
    #warum zur hoelle funktioniert nichts davon -_______________________________-....?
    #htmlCode = re.compile('<((\.)*|(\S)*|( )*)>')
    #htmlText = re.compile('<p>((\S)|(.))*</p>')
    #pattern = re.compile('<+([^>p])*>?|<?([^>p])*>')
    #htmlText = re.compile('<p>(.|(\S)|(\s))*(</p>)?')

"""
