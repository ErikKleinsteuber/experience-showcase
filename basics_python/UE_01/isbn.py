x = input("Please input 9 digit number: ")

counter = 0
s = 0.0

for y in x:
    # print(x[counter])
    counter += 1
    # print(counter)
    s += counter * int(x[counter - 1])

print("s = ", s)

print("z10 = ", int(s) % 11)
