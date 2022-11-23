running = 1
while running == 1:
    print("Enter a year: ")

    try:
        x = int(input())
        if x > 0 and (x % 400 == 0 or (x % 4 == 0 and 100 % x != 0)):
            print("The year " + str(x) + " is a leap year.")
        else:
            print("The year " + str(x) + " is not a leap year.")
    except Exception:
        running = 0
        print("not a valid year.. quitting")
