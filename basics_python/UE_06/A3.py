class neueListe(list):
    def __init__(self):
        super().__init__()

    def __add__(self, element):
        self.append(element)

    def range(self):
        return abs(self.index(min(self)) - self.index(max(self)))


testList = neueListe()

print(testList)

testList + 65

print(f"testList + 65 {testList}")

testList + 100
testList + 50
testList + 60
testList + 3000

# TypeError: '<' not supported between instances of 'str' and 'int'
# hatte noch viel zu tun, deswegen hab' ich es mal nur für Zahlen gemacht, kann das aber gerne noch nachreichen nächste Woche
# testList + "Peter"

print(f"testList + 100 + 50 + 60 + 3000 {testList}")

print(f"Abstand von der 50 zur 3000 sind: {testList.range()}")
