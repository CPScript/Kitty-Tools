import time
time.sleep(2)





print("\n" * 128)
sprint(f"{r}!!!WARNING!!!")
sprint(f"{y}If this code is ran in a sandbox, it wont work correctly... and might not work at all...")
sprint(f"Please use the newest verison of PYTHON")
print(" ")
print("CASE SENSITIVE ANSWERS")
print("Start???")
print("yes | no")
choice = input("")

if choice == "yes":
    print(" ")
    print("Starting...")
    time.sleep(1)
    print("\n" * 64)
    from subprocess import call
    call(["python", "Kahoot/flood/main.py"])
    
if choice == "no":
    print(" ")
    print("Loading...")
    time.sleep(1)
    print("\n" * 64)
    from subprocess import call
    call(["python", "main.py"])
