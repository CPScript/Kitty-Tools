import os
import platform
import sys
from scripts.sprint import sprint
from scripts.colors import ran,y,r,g,c
import time
from subprocess import call
# NEED TO MAKE LOOP... ill do this later
print("\n" * 99)
print("{INFO}")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print("    ▄▄ ▄███████████████████████████████████████████▄▐▄▄▄▌           ")
print("   ▐  ████▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀███▄█▄▌           ")
print(" ▐ ▌  █▀▌                                         ▐▀▌▀█▀            ")
print("  ▀   ▌ ▌                                         ▐ ▌               ")
print("      █ █                                         ▐▌█               ")
print("""KITTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTY-TOOLS!    """)
sprint(f"{y}Version: 2.3.9")
print("===========================")
print("Please type 1, 2, 3, or 4")
print(" ")
print("[1] GO BACK")
print("[2] More info")
print("[3] Contributors")
print("[4] Start hack")
print("||| \-----------/")
choice = input("")

if choice == "1":
    print(" ")
    print("Loading...")
    time.sleep(1)
    print("\n" * 64) 
    from subprocess import call
    call(["python", "main.py"])
    
if choice == "2":
    print(" ")
    print("Loading...")
    time.sleep(1)
    print("\n" * 64) 
    from subprocess import call
    call(["python", "Kahoot/More.py"])
    
if choice == "3":
    print(" ")
    print("Loading...")
    time.sleep(1)
    print("\n" * 64) 
    from subprocess import call
    call(["python", "Kahoot/c.py"])
    
if choice == "4":
    print(" ")
    print("Loading...")
    time.sleep(1)
    print("\n" * 64) 
    from subprocess import call
    call(["python", "Kahoot/kahoot.py"])
