import re

# finds a match
for hit in re.finditer("<+([^>p])*>", "Weltkriegs</a>"):
    print(hit)

# returns false...
if bool(re.findall("<+([^>p])*>", "Weltkriegs</a>")):
    print("qwliufzhqlwfku")

if bool(re.findall("LIÖUÖAIWUDÖLI", "Weltkriegs</a>")):
    print("qwliufzhqlwfku")
