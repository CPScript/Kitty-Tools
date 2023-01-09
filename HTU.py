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
print("When it asks you for the 'Quiz ID' !!!DO NOT TYPE THE 6 to 8 digit code!!!")
print("In the Search bar where it tells you the Website address it should have a 5 letter/number line of code...")
print("IT LOOKS LIKE THIS--> quizId=285524a1-dd39-416a-b92e-2ccdf6d1b9d4")
print("If you can see it on your teachers screen than type it, IF NOT than this wont work for you :(")
print(" ")
print("PS! if the quiz was assigned to you instead of hosted, it should be there so it should work :) ")
print(" ")
print(" ")
print("When loading bar is done it will start the Software.")


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
call(["python", "kahoot.py"])
