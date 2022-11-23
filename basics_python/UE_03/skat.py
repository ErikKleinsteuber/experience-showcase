import itertools
import random

# farben = ["Kreuz","Pik","Herz","Karo"]                     #mit Strings
farben = ["\u2663", "\u2660", "\u2665", "\u2666"]  # in schoen
werte = ["Ass", "König", "Dame", "Bube", "10", "9", "8", "7"]
# werte = ["\u+1F0A1",]


kartenGenerator = (
    farbe + " " + wert for farbe, wert in itertools.product(farben, werte)
)  # (= g)

"""
ein generator Objekt eignet sich nicht zum Mischen von Karten, da es nicht für Zugriffe
beliebigen Indexes, sondern für chronologischen Zugriff und damit Speicherplatz-optimierung
konstruiert wurde. arrays sind im Punkto Zugriff bspw. variabler, deswegen kopieren wir
die Objekte unseres generators gleich mal rueber nach cards
"""
kartenListe = []
counter = 0
print("\nKarten aus unserem Generator: \n")
for n in kartenGenerator:
    if counter == len(werte):
        print("")
        counter = 0
    kartenListe.append(n)
    print(n, end=" ; ")
    counter += 1

counter = 0
print("\n")


print("Karten aus unserer Liste: \n")
for n in kartenListe:
    if counter == len(werte):
        print("")
        counter = 0
    print(n, end=" ; ")
    counter += 1


# returnes mixed cardStack, mixes n times, default n = 12
def mischeKarten(kartenStapel, n=12):
    for x in range(n):
        a = random.randrange(len(kartenStapel))
        b = a
        while a == b:
            b = random.randrange(len(kartenStapel))

        # print(str(a) + " " + str(b))   #Debug
        c = kartenStapel[a]
        kartenStapel[a] = kartenStapel[b]
        kartenStapel[b] = c
    return kartenStapel


kartenListe = mischeKarten(kartenListe)
print()
print("\nGemischte Karten aus unserer Liste: ")
for n in kartenListe:
    if counter == len(werte):
        print("")
        counter = 0
    print(n, end=" ; ")
    counter += 1
