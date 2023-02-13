from scripts.sprint import sprint
from scripts.colors import ran,y,r,g,c
from subprocess import call
import time
time.sleep(2)


print("\n" * 128)
sprint(f"{r}!!!REQUIRMENTS!!!")
sprint(f"{r}MUST Have {y} Chrome Drivers installed, They can be found in the {r}Kahoot/flood/chromedriver' {y}Directory/file\n")
sprint(f"{r}!!!WARNING!!!")
sprint(f"{r}CPScript {y}is not responsible for the {r}user's actions{y}, and {r}they agree to this by typing {c}'yes' {y}below")
sprint(f"{y}If this code is ran in a sandbox, it wont work correctly, and might not work at all...")

sprint(f"Please use the newest verison of PYTHON\n")
print("Start? (TYPE FULL WORD)")
print("yes | no")
choice = input("").lower()

if choice == "yes":
    print("\nStarting...")
    time.sleep(1)
    print("\n" * 64)
    call(["python", "Kahoot/flood/main.py"])
    
    print("Thank you for using Kahoot Flooder!")
    time.sleep(5)
    call(["python", "main.py"])
    
if choice == "no":
    print("\nLoading...")
    time.sleep(1)
    print("\n" * 64)
    call(["python", "main.py"])
