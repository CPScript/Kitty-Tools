from scripts.sprint import sprint
from scripts.colors import ran, y, r, g, c
from subprocess import call
import time
import os
from os import system
import platform

# Old "clear terminal"
# puk = platform()[0], platform()[1],  platform()[2], platform()[3], platform()[4], platform()[5], platform()[6]
# if puk == ('W', 'i', 'n', 'd', 'o', 'w', 's'): 
#    delet = 'cls'
#    dr = '\\' 
#else:
#    delet = 'clear' 
#    dr = '/' 
#os.system(delet) 

def clear():
    system = platform.system().lower()

    if system == 'windows':
        _ = os.system('cls')
    elif system == 'linux' or system == 'darwin':
        _ = os.system('clear')
    elif system == 'android':
        _ = subprocess.run(['termux-exec', 'sh', '-c', 'clear'], check=False)
    else:
        print(f"Unsupported platform, please use Kitty-Tools LITE '{system}'")
        print(f"For more info go to https://github.com/CPScript/Kitty-Tools/more/moreinfo.md")

# Call the clear function
print("Cheaking if Platform Supported!") # Warning
time.sleep(0.5)
print(f"You are using '{system}'") # OS Alert
time.sleep(1)
print("Running test!") # testing if previouse script works
print("1")
clear()

print("done")


# tui
print(f"|======= News =======| ")
print(f" *STAR* this repo so I can get more support :p")
print(f"|====================| ")
time.sleep(4) 

# clear the Termianl
clear()

print(f"""
 ZZz   |\      _,,,---,,_
    zz /,`.-'`'    -.  ;-;;,_
      |,4-  ) )-,_. ,\ (  `'-'
     '---''(_/--'  `-'\_)""")
print(f"{y}>| {r}Kahoot Client {y}| {r}Made by - CPScript{y} |<")
print(" ")
print(f"{y}-----Version-34.8-----")
print(f"{y}/1/ {g}How to use {y}| {r}Shows you how to use the tool{y}")
print(f"{y}/2/ {g}Information {y}| {r}Credits, licence, and more{y}")
print(f"{y}/3/ {g}Flooder {y}| {r}Flood a Kahoot game (Getting Updated!){y}")
print(f"{y}/4/ {g}Answer Hack {y}| {r}Start the answer client{y}")
print(f"{y}----------------------")
choice = input("Make Number Selection :")


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
print("Program Made by CPScript") # You are not allowed claim this software is yours unless it goes through major changes. 
print(" ")
print("""
⠀⠀⠀⠀⠀⢸⣿⣷⣶⣤⣀⣤⣴⣶⣶⣶⣶⣦⣤⣀⣤⣶⣾⣿⡇
⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃
⠀⠀⠠⣤⣀⡀⠹⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⠃⢀⣀⣤⠄
⢀⠤⢤⣤⣬⣙⠳⣿⣿⡿⠀⢀⠀⠈⣿⣿⠁⠀⡀⠈⣿⣿⣿⠞⣋⣥⣤⠤⠤⡀
⠀⢀⡤⠤⢤⣼⣿⣿⣿⣿⡀⠸⠀⣠⣿⣿⣄⠐⠇⢀⣿⣿⣿⣿⣧⡤⠤⢤⡀
⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⠛⠛⠛⠛⠉⠉⠛⠛⠛⠛⣿⣿⣿⣿⣿⣿⣷⡀
===⠛⠿⢿⣿⠟⠛⠁==========⠈⠛⠻⣿⡿⠻⠛======
======| Follow CPScript |========
=================================
""")
