from scripts.sprint import sprint
from scripts.colors import ran,y,r,g,c
from subprocess import call
import time
time.sleep(2)


print("\n" * 128)
print(f"""{y}
""")
sprint(f"{r}!!!WARNING!!!")
print(f"{r}CPScript {y}is not responsible for the {r}user's actions{y}, and {r}they agree to this by typing {c}'yes' {y}below")
print(f"{y}If this code is ran in a sandbox, it wont work correctly, and might not work at all...")

print("Start? (TYPE FULL WORD)")
print("yes | no")
choice = input("").lower()

if choice == "yes":
    print("\nStarting...")
    time.sleep(1)
    print("\n" * 64)
    execfile('index.js')
    
if choice == "no":
    print("\nLoading...")
    time.sleep(1)
    print("\n" * 64)
    call(["python", "main.py"])
