class Metall:
    dichte = {"Fe": ("Eisen", 7.87), "Au": ("Gold", 19.32), "Ag": ("Silber", 10.5)}

    def __init__(self, volumen, symbol):

        self.__volumen = volumen
        self.__symbol = symbol

    def get_Masse(self):
        return self.dichte.get(self.__symbol)[1] * self.get_Volumen()

    # wofür ist denn das get_Volumen wenn ich sowieso auf das Objektattribut von überall zugreifen kann?
    # im allgemeinen Fall um eventuell ein read-only objekt zu erzeugen?
    def get_Volumen(self):
        return self.__volumen

    # hoffe mal -> überschreiben <- ist richtig so?
    def __str__(self):
        print(
            f"{self.dichte.get(self.__symbol)[0]} with volume {self.get_Volumen()} has a mass of {self.get_Masse()}."
        )


# Soll ich Symbol und Volumen jetzt setzen oder wie is das gemeint <_<?
# Entweder Masse oder Volumen muss ich ja setzen, also setze ich jetzt mal Volumen
mObjekt = Metall(2, "Fe")

mObjekt.__str__()

# mObjekt.__volumen = 5
# mObjekt.__symbol = "Au"
# print(mObjekt.get_Volumen())
# print(mObjekt.__dict__)

# diese hübschen Attributsnamen werden zwar im dict gelistet, mir aber nicht von der
# code completion vorgeschlagen ._. -> wofür setter methoden?
mObjekt._Metall__symbol = "Au"
mObjekt._Metall__volumen = 5

mObjekt.__str__()

print()


class Quader(Metall):

    # wo soll ich denn das element/symbol abspeichern aus dem der Quader besteht?
    def __init__(self, symbol, laenge, breite, hoehe):
        super().__init__(laenge * breite * hoehe, symbol)
        self.__laenge = laenge
        self.__breite = breite
        self.__hoehe = hoehe

    def __str__(self):
        print(
            f"Der Quader aus {self.dichte.get(self._Metall__symbol)[0]} mit der Laenge {self.__laenge}, Breite {self.__breite} und Hoehe {self.__hoehe} hat ein Volumen von {self.get_Volumen()} und eine Masse von {self.get_Masse()}."
        )

    # ==
    def __eq__(self, quader):
        if self.get_Masse() == quader.get_Masse():
            return True
        else:
            return False

    # <
    def __lt__(self, quader):
        if self.get_Masse() < quader.get_Masse():
            return True
        else:
            return False

    # <=
    def __le__(self, quader):
        if self.get_Masse() <= quader.get_Masse():
            return True
        else:
            return False

    # >
    def __gt__(self, quader):
        if self.get_Masse() > quader.get_Masse():
            return True
        else:
            return False

    # >=
    def __ge__(self, quader):
        if self.get_Masse() >= quader.get_Masse():
            return True
        else:
            return False


goldwuerfel = Quader("Fe", 1, 2, 3)

print(f"goldwuerfel == goldwuerfel = {goldwuerfel == goldwuerfel}")
print(f"goldwuerfel < goldwuerfel = {goldwuerfel < goldwuerfel}")
print(f"goldwuerfel <= goldwuerfel = {goldwuerfel <= goldwuerfel}")
print(f"goldwuerfel > goldwuerfel = {goldwuerfel > goldwuerfel}")
print(f"goldwuerfel >= goldwuerfel = {goldwuerfel >= goldwuerfel}")
silberwuerfel = Quader("Ag", 1, 2, 3)
eisenwuerfel = Quader("Fe", 1, 2, 3)
print(f"silberwuerfel > eisenwuerfel = { silberwuerfel > eisenwuerfel}")
