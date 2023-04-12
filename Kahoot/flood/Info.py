from scripts.sprint import sprint
from scripts.colors import ran,y,r,g,c
from subprocess import call
import time
import os
from os import system
time.sleep(2)


print("\n" * 128)
print(f"""{r}
LOGO""")
print(" ")
print(" ")
sprint(f"{r}!!!WARNING!!!")
print(f"{r}CPScript {y}is not responsible for the {r}user's actions{y}, and {r}they agree to this by typing {c}'yes' {y}below")
print(f"{y}If this 'Flood' program doesn't work, please tell me via making an issue in the github repo.")
print(" ")
print("Start???")
print("yes | no")
choice = input("").lower()

if choice == "yes":
    print("\nStarting...")
    time.sleep(1)
    print(f"{r}Flooder is being updated...          " * 188)
    time.sleep(5)
    print(" ")
    print(" ")
    print("Restarting...")
    time.sleep(2)
    call(["python", "main.py"])
    
    
if choice == "no":
    print("\nLoading...")
    time.sleep(1)
    print("\n" * 64)
    call(["python", "main.py"])
