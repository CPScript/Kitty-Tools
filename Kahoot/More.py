import os
import platform
import sys
from scripts.sprint import sprint
from scripts.colors import ran,y,r,g,c
import time
sprint(f"{y}Nothing is here...")
time.sleep(2)
sprint(f"{r}NOTHING AT ALL...{c}")
time.sleep(5)

from subprocess import call
call(["python", "main.py"])
