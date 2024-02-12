import os
import platform
import sys
from scripts.sprint import sprint
from scripts.colors import ran, y, r, g, c
import time
from subprocess import call


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
    print(
        f"For more info go to https://github.com/CPScript/Kitty-Tools/more/moreinfo.md"
    )


clear()

print("[Extra-InfoChart v2.7")
print("[====================")
print("[1] GO BACK          ")
print("[2] More info        ")
print("[3] Contributors     ")
print("[4] Legal (COC & TOS)")
print("[====================")
choice = input("[U] >> ")

if choice == "1":
  print(" ")
  print("Loading...")
  time.sleep(1)
  print("\n" * 64)
  call(["python", "main.py"])

if choice == "2":
  print(" ")
  print("Loading...")
  time.sleep(1)
  print("\n" * 64)
  call(["python", "Kitty/Info/extra.py"])

if choice == "3":
  print(" ")
  print("Loading...")
  time.sleep(1)
  print("\n" * 64)
  call(["python", "Kitty/Info/contributors.py"])

if choice == "4":
  print(" ")
  print("Loading...")
  time.sleep(1)
  print("\n" * 64)
  call(["python", "Kitty/Info/legal.py"])
