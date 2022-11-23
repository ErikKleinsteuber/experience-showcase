import sys
import grapher
import os

# region DEFAULT-VALUES
wikiUrlStrt = "https://de.wikipedia.org/wiki"
rootLink = "https://de.wikipedia.org/wiki/Wahrer_Wert"
filePath = ""
colored = ""
colorGraph = False
maxNodes = 500
maxRecursionDepth = 10
# endregion

# region SETUP
if len(sys.argv) <= 1:
    print("Du hast kein Systemargument übergeben, deswegen erscheint dieser Hilfstext.")
    print("Bevor du das Programm benutzt kannst du gerne die Readme lesen.")
    print("Starte das Programm mit 'python main.py -test um einen Testlauf zu starten.")
    print(
        "Starte das Programm mit 'python main.py -help um einen genauen Hilfstext angezeigt zu bekommen."
    )
    sys.exit(0)

try:
    for x in range(len(sys.argv[1:])):
        if x == 0:
            if sys.argv[x + 1] == "-help":
                rootLink = "-help"
                break
            elif sys.argv[x + 1] == "-test":
                rootLink = "-test"
                break
        if sys.argv[x + 1] == "-url":
            rootLink = sys.argv[x + 2]
        elif sys.argv[x + 1] == "-colored":
            colored = sys.argv[x + 2]
        elif sys.argv[x + 1] == "-maxK":
            maxNodes = int(sys.argv[x + 2])
        elif sys.argv[x + 1] == "-maxD":
            maxRecursionDepth = int(sys.argv[x + 2])
        elif sys.argv[x + 1] == "-path":
            filePath = sys.argv[x + 2]
except Exception:
    print("System arguments failed.")
    print("Type -help to see more about the format of the system arguments")

if filePath == "":
    filePath = os.path.dirname(os.path.abspath(__file__))

if rootLink == "-help":
    print("Hilfe:\n")
    print("python main.py followed by systemarguments.")
    print("You need to type them in as pairs, but the pairs don't need ordering.")
    print("-url linkToYourArticle [mandatory]")
    print("-path yourFilePath [obligatory] (if none given, the directory you're in)")
    print("-colored substring [obligatory] (colors matched nodes red)")
    print("-maxK maxNodes [obligatory] (maxNodes of the graph, default = 500)")
    print(
        "-maxD maxDepth [obligatory] (maxIterationDepth of the algorithm, default = 10)"
    )
    sys.exit(0)
elif rootLink == "-test":
    filePath = os.path.dirname(os.path.abspath(__file__))
    rootLink = "https://de.wikipedia.org/wiki/Wahrer_Wert"
    colorGraph = False
    maxNodes = 500
    maxRecursionDepth = 10

if colored != "":
    colorGraph = True
    print(f"Coloring nodes who match the patter '{colored}' red.'")

print(
    f"\nInitiating Graph construction with the following parameters: \n     Rootlink = {rootLink} \n     Colored = {colorGraph}"
)
print(
    f"     Maximum of Nodes = {maxNodes} \n     Maximum of Recursion steps = {maxRecursionDepth}\n     FilePath = {filePath}\\"
)
print("Beginning to work...")
# endregion

if colorGraph:
    gr = grapher.graphManip(
        rootLink=rootLink,
        colored=colored,
        maxNodes=maxNodes,
        maxRecursionDepht=maxRecursionDepth,
    )
else:
    gr = grapher.graphManip(
        rootLink=rootLink,
        colored=False,
        maxNodes=maxNodes,
        maxRecursionDepht=maxRecursionDepth,
    )


gr.doGraphWork()
gr.drawGraph()
gr.saveGraphAsSvg(filePath + "\\graphVisualisation.svg")
gr.saveGraphAsTxt(filePath + "\\graphAsTxt.txt")

# diese Beispielprints wurden auf der URL: https://de.wikipedia.org/wiki/Mate-Tee getestet

"""
print(f"\nneighbours of Chile = {gr.getNeighours('Chile')}")
print(f"neighbours of Mate-Strauch = {gr.getNeighours('Mate-Strauch')}")
print(f"Eingangsgrad of Chile = {gr.getEinGrad('Chile')}")
print(f"Eingangsgrad of Mate-Strauch = {gr.getEinGrad('Mate-Strauch')}")
print(f"Ausgangsgrad of Chile = {gr.getAusGrad('Chile')}")
print(f"Ausgangsgrad of Mate-Strauch = {gr.getAusGrad('Mate-Strauch')}")
"""

print(
    f"\nThe graph consists of {len(gr.G)} nodes and {gr.G.number_of_edges()}/{(len(gr.G)-1)*len(gr.G)} possible edges which makes..."
)
print(f"A density of {gr.computeDensity()}")

print("Done.")
