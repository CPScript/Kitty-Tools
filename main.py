from scripts.sprint import sprint
from scripts.colors import ran, y, r, g, c
from subprocess import call
import time
import os
from os import system
# os.system('git clone https://github.com/CPScript/Kitty-Tools')

print("\n" * 128)
print(f"{g}                                                         {y}▄▄ ▄████▄▐▄▄▄▌           ")
print(f"            {y}▄▀▄     ▄▀▄                                 {y}▐  ████▀███▄█▄▌           ")
print(f"           {y}▄█░░▀▀▀▀▀░░█▄                              {y}▐ ▌  █▀▌  ▐▀▌▀█▀            ")
print(f"       {y}▄▄  █░░░░░░░░░░░█  ▄▄        {g}//+++\\             {y}▀   ▌ ▌  ▐ ▌            ")
print(f"      {y}█▄▄█ █░░▀░░┬░░▀░░█ █▄▄█     {g}//  ||| \\                {y}█ █  ▐▌█         {g}")
print("██╗░░██╗██╗████████╗████████╗██╗░░░██╗|||████████╗░█████╗░░█████╗░██╗░░░░░░██████╗")
print("██║░██╔╝██║╚══██╔══╝╚══██╔══╝╚██╗░██╔╝|||╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░██╔════╝")
print("█████═╝░██║░░░██║░░░░░░██║░░░░╚████╔╝░|||░░░██║░░░██║░░██║██║░░██║██║░░░░░╚█████╗░")
print("██╔═██╗░██║░░░██║░░░░░░██║░░░░░╚██╔╝░░|||░░░██║░░░██║░░██║██║░░██║██║░░░░░░╚═══██╗")
print("██║░╚██╗██║░░░██║░░░░░░██║░░░░░░██║░░░|||░░░██║░░░╚█████╔╝╚█████╔╝███████╗██████╔╝")
print("╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░░░░╚═╝░░░|||░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝╚═════╝░")
print("Kahoot Terminal tool   \\             |||             //                          ")
print("                        -------------------------------                           ")
print(f"{y}|======= {r}News{y} =======| ")
print(f"|{r}HEY YOU! Can you help me??? I need people to maintain and update this script. if you would like to help than make an issue on the repo!{y}")
print(f"{y}|=========================| ")
print(" ")
sprint(f"{y}[!]Please type 1, 2, 3, or {r}4{y}")
print(" ")
print("[1] How to use")
print("||| \\--------/")
print(" ")
print("[2] Information")
print("||| \\---------/")
print(" ")
print("[3] Flooder (Getting Updated!)")
print("||| \\-----/")
print(" ")
print(f"{y}[{r}4{y}] {r}Start Hack")
print(f"{c}||| {y}\\--------/")
choice = input("")


if choice == "1":
    print(" ")
    print("Loading...")
    time.sleep(1)
    call(["python", "Kahoot/HTU.py"])

if choice == "2":
    print(" ")
    print("Loading...")
    time.sleep(1)
    call(["python", "Kahoot/Info.py"])

if choice == "3":
    print(" ")
    print("Loading...")
    time.sleep(1)
    call(["python", "Kahoot/flood/Info.py"])

if choice == "4":
    print(" ")
    print("Starting...")
    time.sleep(1)
    print("\n" * 64)  # imma this makes more sense
    call(["python", "Kahoot/kahoot.py"])

time.sleep(25)
print(" ")
print(" ")
print("Program Made by CPScript")
print(" ")
print("   ▄▀ ▄▀   ")
print("    ▀  ▀   ")
print("  █▀▀▀▀▀█▄ ")
print("  █░░░░░█ █")
print("  ▀▄▄▄▄▄▀▀ ")
