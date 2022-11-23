import re

# DATUM
datumgueltig = re.compile(
    "(([0-2]?[0-9])|3[0-1])\\.(([0-1][0-2])|[0-9])\\.([0-9][0-9])?[0-9][0-9]"
)

for find in re.finditer(
    datumgueltig,
    "qwlkdjqwlkfj 22.22.22 ölkqkwjf 01.02.00 oiwuqroi 1.2.33 qwlkdjqwlkfj 22.22.22 ölkqkwjf 01.02.0044 oiwuqroi 1.2.33, 30.19.9999, 30.12.0000, 31.12.1999, 32.10.0000",
):
    print(find)

# UHRZEIT
uhrzeit = re.compile("(([0-1][0-9])|(2[0-3]))\\:[0-5][0-9]\\:[0-5][0-9]")

for find in re.finditer(
    uhrzeit,
    "oqiwur23:44:55lköqwjrölkjqwr25:44:55.......23:59:59......00:00:00....00:00:60.......24:00:00",
):
    print(find)
