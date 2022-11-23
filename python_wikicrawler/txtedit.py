import re
import requests

wikiUrlStrt = "https://de.wikipedia.org/wiki"


class textManip:
    # takes a link(url) and returns the title of the article
    def extractSitename(self, link):
        helper = ""
        for c in link:
            if c == "/":
                helper = ""
            else:
                helper += c

        return helper

    # crops and filters the text to a list
    def getCroppedText(self, bareContent):
        # region Crop Text
        splitText = []
        inText = False
        piece = ""

        for c in bareContent:
            piece += c
            if bool(re.search("<p>", piece[-3:])):
                inText = True
                piece = ""

            if bool(re.search("</p>", piece[-4:])) and inText == True:
                inText = False
                piece = piece[:-4]
                splitText.append(piece)
                piece = ""
        # endregion

        return splitText

    # list to String
    def backToString(self, text):
        # region backToString
        bareText = ""
        for word in text:
            bareText += word
            bareText += "\n"
        # endregion

        return bareText

    def extractLinks(self, bareText):
        helperList = []
        inLink = False
        inMarkedWord = False
        extracted = False
        piece = ""

        # region filter marked Words
        for c in bareText:
            piece += c

            if inMarkedWord is True:

                if c == "<":
                    inMarkedWord = False
                    extracted = False
                    continue
            elif inLink is True:
                if c == ">":
                    inLink = False
                    inMarkedWord = True
                    piece = ""
                if c == '"' and extracted is False:
                    helperList.append(piece[1:-1])
                    piece = ""

                    extracted = True
            elif bool(re.search('<a href="/wiki', piece[-14:])):
                inLink = True
                piece = ""
        # endregion

        return helperList

    def getContent(self, link):
        content = requests.get(link)
        return content.text

    def getUrlFromTitle(self, title):
        return wikiUrlStrt + "/" + title

    def getLinksFromTitle(self, title):
        return self.extractLinks(
            self.backToString(
                self.getCroppedText(self.getContent(self.getUrlFromTitle(title)))
            )
        )
