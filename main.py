print("""
||| Error message : If you dont see any errors, please ignore this message! |||
|
|
| If you see this message and there is an error below this message please re run the 'main.py' file!
| If re-running said file doesn't fix the software please contact me via making an issue on the github repo
| https://github.com/CPScript/Kitty-Tools
===========================================================================================================
""")
import time
time.sleep(0.001)

from scripts.sprint import sprint
from scripts.colors import ran, y, r, g, c
from subprocess import call
import os
from os import system
import platform 

def clear():
    system = platform.system().lower()

    if system == 'windows':
        _ = os.system('cls')
    elif system == 'linux' or system == 'darwin':
        _ = os.system('clear')
    elif system == 'android':
        _ = subprocess.run(['termux-exec', 'sh', '-c', 'clear'], check=False)
        print("Please use the 'LITE' version so kitty tools will run smoothly <3")
        exit()
    else:
        print(f"Unsupported platform, please use Kitty-Tools LITE '{system}'")
        print(f"For more info go to https://github.com/CPScript/Kitty-Tools/extra.md")

# Call the clear function
print("Checking if Your Platform is Supported!") # Warning
time.sleep(0.5)
print(f"You are using '{system}'") # OS Alert
time.sleep(1)
print("Running test!") # testing if previouse script works
print("1")
clear()

print("done")
clear()


# tui
print(f"||================== Notice ====================|| ")
print(f"|| *STAR* this repo so I can get more support <3|| ")
print(f"||==============================================|| ")
time.sleep(4) 
clear()

print(f"""
 ZZz   |\      _,,,---,,_
    zz /,`.-'`'    -.  ;-;;,_
      |,4-  ) )-,_. ,\ (  `'-'
     '---''(_/--'  `-'\_)""")
print(f"{y}>| {r}Kahoot Client {y}| {r}Made by - CPScript{y} |<")
print(" ")
print(f"{y}-----Version-36.2-----")
print(f"{y}/1/ {g}How to use {y}| {r}Shows you how to use the tool{y}")
print(f"{y}/2/ {g}Information {y}| {r}Credits, licence, and more{y}")
print(f"{y}/3/ {g}Flooder {y}| {r}Flood a Kahoot game (Not working){y}")
print(f"{y}/4/ {g}Answer Hack {y}| {r}Start the answer client{y}")
print(f"{y}----------------------")
choice = input("Make Number Selection :")


if choice == "1":
    print(" ")
    print("Loading...")
    time.sleep(1)
    call(["python", "Kitty/htu.py"])

if choice == "2":
    print(" ")
    print("Loading...")
    time.sleep(1)
    call(["python", "Kitty/Info/main.py"])

if choice == "3":
    print(" ")
    print("Loading...")
    time.sleep(1)
    call(["python", "Kitty/flood/Info.py"])

if choice == "4":
    print(" ")
    print("Starting...")
    time.sleep(1)
    print("\n" * 64)  # imma this makes more sense
    call(["python", "Kitty/client.py"])
