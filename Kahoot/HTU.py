import os
import platform
import sys
from scripts.sprint import sprint
from scripts.colors import ran,y,r,g,c
print("\n" * 32)
print("────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
print("─██████──██████─██████████████─██████──────────██████────██████████████────██████──██████─██████████████─██████████████─")
print("─██░░██──██░░██─██░░░░░░░░░░██─██░░██──────────██░░██────██░░░░░░░░░░██────██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─")
print("─██░░██──██░░██─██░░██████░░██─██░░██──────────██░░██────██████████░░██────██░░██──██░░██─██░░██████████─██░░██████████─")
print("─██░░██──██░░██─██░░██──██░░██─██░░██──────────██░░██────────────██░░██────██░░██──██░░██─██░░██─────────██░░██─────────")
print("─██░░██████░░██─██░░██──██░░██─██░░██──██████──██░░██────██████████░░██────██░░██──██░░██─██░░██████████─██░░██████████─")
print("─██░░░░░░░░░░██─██░░██──██░░██─██░░██──██░░██──██░░██────██░░░░░░░░░░██────██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─")
print("─██░░██████░░██─██░░██──██░░██─██░░██──██░░██──██░░██────██░░██████████────██░░██──██░░██─██████████░░██─██░░██████████─")
print("─██░░██──██░░██─██░░██──██░░██─██░░██████░░██████░░██────██░░██────────────██░░██──██░░██─────────██░░██─██░░██─────────")
print("─██░░██──██░░██─██░░██████░░██─██░░░░░░░░░░░░░░░░░░██────██░░██████████────██░░██████░░██─██████████░░██─██░░██████████─")
print("─██░░██──██░░██─██░░░░░░░░░░██─██░░██████░░██████░░██────██░░░░░░░░░░██────██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─")
print("─██████──██████─██████████████─██████──██████──██████────██████████████────██████████████─██████████████─██████████████─")
print("────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
print(" ")
print(" ")
print("Its acctualy VERY simple...")
print("Please READ")
print(" ")
print(" ")
sprint(f"{y} When it asks you for the {r} 'Quiz ID' {y} !!!DO NOT TYPE THE 6 to 8 digit code!!! ")
sprint(f"{y} In the Search bar where it tells you the Website address it should have a 5 letter/number line of code... ")
sprint(f"{y} IT LOOKS LIKE THIS--> {r} quizId=285524a1-dd39-416a-b92e-2ccdf6d1b9d4 ")
sprint(f"{y} If you can see it on your teachers screen than type it, IF NOT than this wont work for you :(")
print(" ")
sprint(f"{r} PS! if the quiz was assigned to you instead of hosted, it should be there so it should work :) ")
print(" ")
print(" ")
sprint(f"{y} When loading bar is done it will start the Software.")


import sys
def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "#"*x, "."*(size-x), j, count), 
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)
    
import time    
for i in progressbar(range(500), "Loading: ", 35):
    time.sleep(0.1)
print("\n" * 64)
from subprocess import call
call(["python", "Kahoot/kahoot.py"])
