import os
import platform
import sys
from scripts.sprint import sprint
from scripts.colors import ran,y,r,g,c
import time
print("Cool contributers")
sprint(f"""{y}Thank you
{r}@Ccode-lang {y}for helping out!
{r}@xTobyPlayZ {y}for Flooder!
{r}@cheepling {y}for finding bugs!
{r}@Zacky2613 {y}for helping and fixing issus!
{r}@KiraKenjiro {y}for reviewing and making changes! {r}<3 {y}
""")
time.sleep(5)

from subprocess import call
call(["python", "main.py"])
