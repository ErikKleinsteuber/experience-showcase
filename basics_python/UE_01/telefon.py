numberBook = {}

for x in range(3):

    name = input("Name: ")
    number = input("Telefonnummer: ")
    print(name)
    print(number)
    numberBook[str(number)] = name

print(numberBook)
