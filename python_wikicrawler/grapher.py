import networkx as nx
import matplotlib.pyplot as plt
import re
import txtedit as tx


class graphManip:
    def __init__(self, rootLink, colored, maxNodes=500, maxRecursionDepht=10):
        self.maxNodes = maxNodes
        self.tooManyNodes = False
        self.maxRecursionDepht = maxRecursionDepht
        self.G = nx.Graph()
        self.graphDic = {}
        self.colored = colored

        self.rootLink = rootLink
        self.texter = tx.textManip()
        self.root = self.texter.extractSitename(self.rootLink)

    # Ablaufroutine 1. graphDic intialisieren, 2. wiki crawlen, 3. Graphen bauen
    def doGraphWork(self):
        self.graphDic = {}
        self.graphDic[self.root] = []
        self.crawlWiki(self.graphDic)
        self.buildGraph()

    # builds the graph
    def buildGraph(self):
        print("Building the graph...")
        for element in self.graphDic.keys():
            self.G.add_node(element)
            for value in self.graphDic.get(element):
                self.G.add_edge(element, value)

    def drawGraph(self):
        print("Drawing the graph...")

        # positions for all nodes
        pos = nx.spring_layout(self.G)

        for element in self.graphDic.keys():
            if element == self.root:
                nx.draw_networkx_nodes(
                    self.G,
                    pos,
                    nodelist=[self.root],
                    node_size=20,
                    alpha=0.9,
                    node_color="g",
                )
            else:
                # schaue nach ob im Titel der substring vorkommt, wenn ja färbe den node ein
                if self.colored:
                    if self.colored in element:
                        # print(f"Matched element on given pattern = {element}")
                        nx.draw_networkx_nodes(
                            self.G,
                            pos,
                            node_size=3 + len(self.graphDic.get(element)) / 5,
                            alpha=0.9,
                            nodelist=[element],
                            node_color="r",
                        )
                    else:
                        nx.draw_networkx_nodes(
                            self.G,
                            pos,
                            node_size=3 + len(self.graphDic.get(element)) / 5,
                            alpha=0.9,
                            nodelist=[element],
                        )
                else:
                    nx.draw_networkx_nodes(
                        self.G,
                        pos,
                        node_size=3 + len(self.graphDic.get(element)) / 5,
                        alpha=0.9,
                        nodelist=[element],
                    )

        nx.draw_networkx_labels(self.G, pos, font_size=1)
        nx.draw_networkx_edges(self.G, pos, alpha=0.1, arrows=True)

    # crawlet solange alle Seiten per Breitensuche (sozusagen), bis self.maxNodes oder self.maxRecursionDepth erreicht ist
    def crawlWiki(self, dic):
        print("Crawling the Wiki...")
        # linkMemory merkt sich alle hinzugefügten Knoten (keine Doppelten)
        # und fügt sie dem dictionary als neuen Eintrag hinzu
        linkMemory = []

        # elementMemory merkt sich alle bereits gecrawlten Seiten
        elementMemory = []
        recurStep = 0
        recurIntervals = [0]

        while len(dic) < self.maxNodes:
            # neue Einträge für frisch gefundene (Links) Nodes anlegen
            if len(linkMemory) > 0:
                linkMemory = list(dict.fromkeys(linkMemory))
                for link in linkMemory:
                    dic[link] = []

                # Schrittgröße merken um festzustellen auf welcher Tiefe wir im Baum sind ()
                if len(recurIntervals) > recurStep + 1:
                    recurIntervals[recurStep + 1] += len(linkMemory)
                else:
                    recurIntervals.append(0)
                    recurIntervals[recurStep + 1] += len(linkMemory)

            # Check ob max. Node oder max. Depth erreicht wurde
            if len(dic) >= self.maxNodes:
                print("\nMaximum of nodes reached.\n")
                break
            elif recurStep > self.maxRecursionDepht:
                print("\nMaximum of Recursion Depth reached\n")
                break

            try:
                if len(elementMemory) > recurIntervals[recurStep]:
                    recurStep += 1
            except Exception:
                # ist nur ein workaround, brauch kein handling
                pass

            # setze zurück um neue Seite crawlen zu können
            linkMemory = []

            # iteriere fortlaufend über dic.keys()
            for element in dic.keys():
                # check ob Seite schon besucht
                if element in elementMemory:
                    continue
                # falls nicht, crawle diese Seite (Element) und starte dann die schleife neu
                # um das dictionary zu aktualisieren
                else:
                    print(f"     Crawling {element}")
                    # füge dem Gedächtnis hinzu
                    elementMemory.append(element)

                    # Liste aller Verlinkungen auf unserer Seite
                    linksLst = self.texter.getLinksFromTitle(element)

                    # für jeden gefundenen Link
                    for link in linksLst:
                        # haben wir ihn schonmal irgendwo gefunden oder gecrawlt?
                        if link in dic.keys():
                            # ja -> dann füge ihn zur Liste unserer Seite hinzu
                            dic[element].append(link)
                        else:
                            # removes duplicates
                            linkMemory = list(dict.fromkeys(linkMemory))

                            # nein -> check ob dich Maximum erreicht hat?
                            if len(dic) + len(linkMemory) >= self.maxNodes:
                                break
                            else:
                                # wenn nicht, zur Liste der Schlüssel und zu unserer Seite
                                # hinzufügen
                                linkMemory.append(link)
                                dic[element].append(link)
                    break

    def saveGraphAsSvg(self, path):
        print(f"Saving graph as svg image at {path}...")
        plt.savefig(fname=(path), format="svg")

    def saveGraphAsTxt(self, path):
        print(f"Saving graph as txt file at {path}...")
        txt = open(path, "w+", encoding="utf-8")
        txt.write(str(self.graphDic))

    # region graph analyzation

    # gibt die Graphdichte zurück
    def computeDensity(self):
        maximumEdges = (len(self.G) - 1) * len(self.G)
        return self.G.number_of_edges() / maximumEdges

    # gibt incoming and outgoing nodes
    def getNeighours(self, node):
        neighbours = self.getIncomingNodes(node)
        neighbours += self.graphDic.get(node)

        neighbours = list(dict.fromkeys(neighbours))
        return neighbours

    # Eingangsgrad
    def getEinGrad(self, node):
        return len(self.getIncomingNodes(node))

    def getIncomingNodes(self, node):
        incoming = []

        for element in self.graphDic.keys():
            if node in self.graphDic.get(element):
                incoming.append(element)

        incoming = list(dict.fromkeys(incoming))
        return incoming

    # Ausgangsgrad
    def getAusGrad(self, node):
        return len(self.getOutgoingNodes(node))

    def getOutgoingNodes(self, node):
        return self.graphDic.get(node)

    # endregion
