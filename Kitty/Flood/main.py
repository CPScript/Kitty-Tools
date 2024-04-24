# THE CONTENT IN THIS FILE AND ITS SIMPLICITY IS UGLY AND MAKES MY MIND HURT

import time
import os
import platform 
import subprocess
from os import system
from subprocess import call

def clear():
    system = platform.system().lower()

    if system == 'windows':
        _ = os.system('cls')
    elif system == 'linux' or system == 'darwin':
        _ = os.system('clear')
    elif system == 'android':
        _ = subprocess.run(['termux-exec', 'sh', '-c', 'clear'], check=False)
        print("Please use LITE!")
        exit()
    else:
        print(f"Unsupported platform, please use Kitty-Tools LITE '{system}'")
        print(f"For more info go to https://github.com/CPScript/Kitty-Tools/extra.md")
clear() # call check

print("Start???")
print("yes | no")
choice = input("").lower()

if choice == "yes":
    time.sleep(1)
    clear()
    print("Checking if requirment exists: node")
    try:
        import node # does node exist
    except ModuleNotFoundError:
        print("Atempting to install node...")
        time.sleep(2)
        os.system("pip install node") # installation
        clear()
    clear()   
    print("Exicuting!")
    time.sleep(2)
    clear()
    subprocess.run(["node", "Kitty/Flood/flood.js"])
    
    
if choice == "no":
    print("\nRe-Running main menu file!")
    time.sleep(3)
    clear()
    call(["python", "main.py"])
