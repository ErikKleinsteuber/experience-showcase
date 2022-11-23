adenin = "A"
cytosin = "C"
guanin = "G"
thymin = "T"

paarungen = [adenin + thymin, thymin + adenin, cytosin + guanin, guanin + cytosin]

print(str(paarungen))

counter = 0

for a in paarungen:
    for b in paarungen:
        for c in paarungen:
            for d in paarungen:
                for e in paarungen:
                    counter += 1
                    print(
                        "Basenpaar = ["
                        + str(a)
                        + str(b)
                        + str(c)
                        + str(d)
                        + str(e)
                        + "] counter = "
                        + str(counter)
                    )

print(
    "Es existieren "
    + str(len(paarungen))
    + "^5 = "
    + str(counter)
    + " mögliche verschiedene Baasenpaare"
)
