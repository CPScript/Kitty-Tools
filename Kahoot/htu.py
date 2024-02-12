import os
import platform
import sys
from scripts.sprint import sprint
from scripts.colors import ran,y,r,g,c
print("\n" * 32)
print("""
$$\   $$\                                 $$\                                                   
$$ |  $$ |                                $$ |                                                  
$$ |  $$ | $$$$$$\  $$\  $$\  $$\       $$$$$$\    $$$$$$\        $$\   $$\  $$$$$$$\  $$$$$$\  
$$$$$$$$ |$$  __$$\ $$ | $$ | $$ |      \_$$  _|  $$  __$$\       $$ |  $$ |$$  _____|$$  __$$\ 
$$  __$$ |$$ /  $$ |$$ | $$ | $$ |        $$ |    $$ /  $$ |      $$ |  $$ |\$$$$$$\  $$$$$$$$ |
$$ |  $$ |$$ |  $$ |$$ | $$ | $$ |        $$ |$$\ $$ |  $$ |      $$ |  $$ | \____$$\ $$   ____|
$$ |  $$ |\$$$$$$  |\$$$$$\$$$$  |        \$$$$  |\$$$$$$  |      \$$$$$$  |$$$$$$$  |\$$$$$$$\ 
\__|  \__| \______/  \_____\____/          \____/  \______/        \______/ \_______/  \_______|
================================================================================================
Selection '1' : You are looking at it!
Selection '2' : This opens a catigory with more information such as; Contributers, the repo's licence, and more!
Selection '3' : This runs a script that will flood the game lobbie with bots, its currently not working and I havn't fixed it yet~
Selection '4' : This runs a script that gives you the answers to a kahoot game. 
""")
sprint(f"{r} PS! if the quiz was assigned to you instead of hosted, it should be there so it should work :) ")

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
