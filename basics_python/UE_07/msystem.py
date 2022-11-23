class ManagementSystem:
    def __init__(self, konten, veranstaltungen, veranstaltungstypen):

        # lade schon vorhandene Liste an Konten
        __konten = konten

        # lade schon vorhandene Liste an Veranstaltungen
        __veranstaltungen = veranstaltungen

        # lade schon vorhandene Liste an Veranstlatungstypen
        __veranstaltungstypen = veranstaltungstypen

    # erstelle Konto und speichere es in die Liste vorhandener Konten
    def kontoerstellen(self):
        pass

    # lösche Konto aus der Liste
    def kontolöschen(self):
        pass

    # zeige alle momentan vorhandenen Konten (also lade...)
    def konten_auflisten(self):
        pass


class Historie:
    def __init__(self, accounttyp, aktionen):

        # speichert ob es sich um einen Nutzer, Veranstalter oder admin handelt) -> dementsprechend anderes verhalten
        __accounttyp = accounttyp

        # dic o.Ä. zum abspeichern der Aktionen
        __aktionen = aktionen

    # pushe eine Aktion in -> aktionen (write only, stack)
    def addAktion(self):
        pass


class Konto:
    def __init__(self, accounttyp, name, passwort):

        # jedes Konto erstellt genau eine Historie
        __history = Historie(accounttyp, {})

        # jedes Konto hat einen Namen und passwort -> kommuniziert mit dem Managementsystem, wird hier eigentlich nicht geladen,
        # .. aber ich habe es der Übersicht halber mal mit hingeschrieben
        __name = name
        __passwort = passwort

    # lade Nutzerdaten und checke ob richtig -> falls ja loginsession auf
    def login(self):
        pass

    # loginsession zu
    def logout(self):
        pass

    def changeName(self):
        pass

    def changePW(self):
        pass

    # lädt die historie aus dem attribut aus konto
    def getHistorie(self):
        pass


class Benutzerkonto(Konto):
    def __init__(self, alter, geschlecht, mail, zahlungsinfo):
        super().__init__("Benutzer")
        __alter = alter
        __geschlecht = geschlecht
        __mail = mail
        __zahlungsinfo = zahlungsinfo

    # suche in einer Liste von Veranstaltungen im Managementsystem
    def sucheVeranstaltung(self):
        pass

    def kaufeTicket(self):
        pass


class Veranstalterkonto(Konto):
    def __init__(self, firma, mail, kontaktinfo):
        super().__init__("Veranstalter")
        __firma = firma
        __mail = mail
        __kontaktinfo = kontaktinfo

    # füge eine Veranstaltung in die Liste im Managementsystem hinzu
    def addEvent(self):
        pass

    # ändere spezifische Infos der eigenst erstellten Veranstaltung
    def changeEvent(self):
        pass

    # lade Infos aus einem spezifischen Veranstaltungsobjekt
    def getEventInfo(self):
        pass


class Admin(Konto):
    def __init__(self, name):
        super().__init__("Admin")
        __name = name

    # sperre Account (lässt sich am besten über einen Mechanismus direkt im Managementsystem realisieren)
    def sperreACC(self):
        pass

    def entsperreACC(self):
        pass

    # setze passwort zurück (über E-mail kommunikation und spezielle methode im Managementsystem -> diese speichert dann neue Daten ab)
    def resetPW(self):
        pass

    # füge Ort- /Veranstaltung- /Veranstaltungstyp hinzu
    def addOrt(self):
        pass

    def addEventType(self):
        pass

    def addEvent(self):
        pass


# diese Klassen haben keine eigenen Objekte, da sie nur zur Datenkapselung und Ordnung da sind (sie speichern Infos geordnet und wiederverwendbar ab)
class Ort:
    def __init__(self, adresse, fläche, veranstaltungen):
        __adresse = adresse
        __fläche = fläche
        __veranstaltungen = veranstaltungen


class Veranstaltung:
    def __init__(self, ort, datum, typ, veranstalter):
        __ort = ort
        __datum = datum
        __typ = typ

        # um später dafür zu sorgen dass nur der veranstalter auch die veranstaltung ändern kann
        __veranstalter = veranstalter
