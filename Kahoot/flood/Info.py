import os
import platform
import sys
from scripts.sprint import sprint
from scripts.colors import ran,y,r,g,c
import time
time.sleep(2)





print("\n" * 128)
sprint(f"{r}!!!WARNING!!!")
print(" ")
print(" ")
sprint(f"{r}CPScript {y}is not {r}responsible {y}for the {r}user's actions{y}, and {r}they agree to this{r} {y}by {r}typing yes {y}bellow")
sprint(f"{y}If this code is ran in a sandbox, it wont work correctly, and might not work at all...")
sprint(f"Please use the newest verison of PYTHON")
print(" ")
print("CASE SENSITIVE")
print("Start?")
print("yes | no")
choice = input("")

if choice == "yes":
    print(" ")
    print("Starting...")
    time.sleep(1)
    print("\n" * 64)
    from subprocess import call
    call(["python", "Kahoot/flood/main.py"])
    
    print("Thank you for using Kahoot Flooder!")
    time.sleep(5)
    call(["python", "main.py"])
    
if choice == "no":
    print(" ")
    print("Loading...")
    time.sleep(1)
    print("\n" * 64)
    from subprocess import call
    call(["python", "main.py"])
