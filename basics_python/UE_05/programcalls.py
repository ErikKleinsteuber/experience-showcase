import os
import shutil
import sys
import time

directoryName = "newDir"
programName = "programcalls.py"
secondSafetyNumber = 5
safetyNumber = 0

# check if there is a system argument
# make sure to not set any when running the first time
# makes sure which copy is called atm
if len(sys.argv) == 2:
    safetyNumber = int(sys.argv[1]) - 1
    # print(f"safetyNumber = {safetyNumber}")
    secondSafetyNumber = safetyNumber + 1
elif len(sys.argv) == 3:
    safetyNumber = int(sys.argv[1])
    secondSafetyNumber = safetyNumber
else:
    safetyNumber = 5


print(f"Safetynumber = {safetyNumber}")
print(f"SecondSafetyNumber = {secondSafetyNumber}")

if safetyNumber > 0:
    if safetyNumber != secondSafetyNumber:
        os.chdir(f"./{directoryName}")
        print(f"Changing directory to: {os.getcwd()}")

    if os.path.exists(f"{os.getcwd()}/{directoryName}"):
        print("Verzeichnis schon vorhanden. Ignoriere und mache weiter.")
    else:
        os.mkdir(f"./{directoryName}")

    print(f"Making file at {os.getcwd()}\\{directoryName}\\{programName}")
    shutil.copy(
        f"{os.getcwd()}\\{programName}",
        f"{os.getcwd()}\\{directoryName}\\{programName}",
    )

    os.system(f"python {os.getcwd()}\\{directoryName}\\{programName} {safetyNumber}")
else:
    # wait 15 seconds and terminate
    time.sleep(15)


if safetyNumber > 0:
    print(f"Program with safetynumber: {safetyNumber} starts deleting now!")
    os.chdir("./")
    print(f"Changing directory to: {os.getcwd()}")
    os.remove(f"./{directoryName}/{programName}")
    os.rmdir(f"./{directoryName}")
