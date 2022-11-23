from tkinter import *
import ast

filepath = "C:/My_stuff/Studium/[PYTHON]Skriptsprachen/UE_03/telephonebook.txt"
book = {}


def loadBook(filepath):
    # lade Inhalt des Buches
    try:
        print("Opening file...")
        bookContent = open(filepath, "r")
    except Exception:
        print("Das File konnte nicht geladen werden. ")

    try:
        print("Parsing Content...")
        book = ast.literal_eval(bookContent.read())
        return book
    except Exception:
        print("Fehler beim Parsen des abgespeicherten Telefonbuchs.")


# window setup
window = Tk()
window.title("telephone book")
window.geometry("470x200")

# textbox for entering search String
search = Entry(window, width=10)
search.grid(column=0, row=0)

# searchLabel displaying the result
searchLabel = Label(window)
searchLabel.grid(column=3, row=0)


# button for searching-EVENT
def searchClicked():
    print("User searched for '" + search.get() + "'")
    if search.get() in book.keys():
        print("found!")
        foundNumbers = ""
        for number, name in book.items():
            if name == search.get():
                foundNumbers += ":" + number + ":"
                searchLabel.configure(text=foundNumbers)
    else:
        print("not found!")
        searchLabel.configure(text="Name not found!")


# button for searching
searchButton = Button(window, text="Search", command=searchClicked)
searchButton.grid(column=1, row=0)

# textbox for making a new Entry specifing number
newEntryNumber = Entry(window, width=10)
newEntryNumber.grid(column=0, row=1)

# textbox for making a new Entry specifing name
newEntryName = Entry(window, width=10)
newEntryName.grid(column=1, row=1)

# newEntryLabel displaying the result of the newEntry
newEntryLabel = Label(window)
newEntryLabel.grid(column=3, row=1)


# button for newEntry-EVENT
def newEntryClicked():
    print(
        "User trys to make the new entry with name = '"
        + newEntryName.get()
        + "' and number = '"
        + newEntryNumber.get()
        + "'"
    )
    if newEntryNumber.get() in book:
        print("That number already exists")
        newEntryLabel.configure(text="That number already exists")
    else:
        book[newEntryNumber.get()] = newEntryName.get()
        newEntryLabel.configure(text="Succesful")
        print(
            "Succesfully made a new Entry for "
            + newEntryName.get()
            + " "
            + newEntryNumber.get()
        )


# button for searching
newEntryButton = Button(window, text="newEntry", command=newEntryClicked)
newEntryButton.grid(column=2, row=1)


# button for display-EVENT
def display():

    zeilen = 0
    spalten = 2
    tabelle = []

    # prints table
    for z in book:

        tabelle.append([])

        for s in range(spalten):

            nameEntry = Entry(window)

            if s == 1:
                nameEntry.insert(0, str(book.get(z)))
            else:
                nameEntry.insert(0, z)

            nameEntry.grid(row=zeilen + 4, column=s)
            tabelle[-1].append(nameEntry)

        zeilen += 1


# button for saveAndClose-EVENT
def saveAndClose():
    on_closing()


# button for displaying the telephone book
displayButton = Button(window, text="display", command=display)
displayButton.grid(column=0, row=2)

# button for displaying the telephone book
saveAndCloseButton = Button(window, text="saveAndClose", command=saveAndClose)
saveAndCloseButton.grid(column=1, row=2)


# save everything before closing the window and quiting program
def on_closing():
    print("Exiting...")
    with open(filepath, "w") as file:
        try:
            file.write(str(book))
        except Exception:
            print("Failed saving the file. Exiting now...")
    window.destroy()


# ENTRY POINT

# lade Telefonbuch
try:
    book = open(filepath)
except Exception:
    print("Das File konnte nicht geladen werden. ")

"""
lade zu Beginn des Programms den Inhalt des abgespeicherten Telefonbuches in eine Variable 
um damit arbeiten zu können
"""
book = loadBook(filepath)
display()

# listener for the WM_DELETE_WINDOW-EVENT
window.protocol("WM_DELETE_WINDOW", on_closing)

# window initial showup
window.mainloop()
