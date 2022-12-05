import time
import pyfiglet
from termcolor import colored

ascii_banner = pyfiglet.figlet_format("Kahoot Flooder")
print(ascii_banner)

import sys
def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "/"*x, "|"*(size-x), j, count), 
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)
for i in progressbar(range(100), "Loading: ", 40):
    time.sleep(0.1) # any code you need
for i in progressbar(range(500), "Downloading Packets: ", 20):
    time.sleep(0.1) # any code you need
for i in progressbar(range(50), "Uploading Java: ", 40):
    time.sleep(0.1) # any code you need
for i in progressbar(range(10), "Finishing up: ", 40):
    time.sleep(0.1) # any code you need
print("Done!")

from subprocess import call
call(["node", "flooder.js"])
time.sleep(0.1)
