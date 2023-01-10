import os
import platform
import sys
from scripts.banner import banner2,banner,clear
from scripts.sprint import sprint
from scripts.colors import ran,y,r,g,c
import time
print("\n" * 128)
print("                                                         ▄▄ ▄████▄▐▄▄▄▌           ")
print("            ▄▀▄     ▄▀▄                                 ▐  ████▀███▄█▄▌           ")
print("           ▄█░░▀▀▀▀▀░░█▄                              ▐ ▌  █▀▌  ▐▀▌▀█▀            ")
print("       ▄▄  █░░░░░░░░░░░█  ▄▄        //+++\\            ▀   ▌ ▌  ▐ ▌               ")
print("      █▄▄█ █░░▀░░┬░░▀░░█ █▄▄█      // |||  \\              █ █  ▐▌█               ")
print("██╗░░██╗██╗████████╗████████╗██╗░░░██╗|||████████╗░█████╗░░█████╗░██╗░░░░░░██████╗")
print("██║░██╔╝██║╚══██╔══╝╚══██╔══╝╚██╗░██╔╝|||╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░██╔════╝")
print("█████═╝░██║░░░██║░░░░░░██║░░░░╚████╔╝░|||░░░██║░░░██║░░██║██║░░██║██║░░░░░╚█████╗░")
print("██╔═██╗░██║░░░██║░░░░░░██║░░░░░╚██╔╝░░|||░░░██║░░░██║░░██║██║░░██║██║░░░░░░╚═══██╗")
print("██║░╚██╗██║░░░██║░░░░░░██║░░░░░░██║░░░|||░░░██║░░░╚█████╔╝╚█████╔╝███████╗██████╔╝")
print("╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░░░░╚═╝░░░|||░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝╚═════╝░")
print("                       \\             |||             //                          ")
print("                        \\            |||            //                           ")
print("                         \\           |||           //                            ")
print("                          \\          |||          //                             ")
print("                     /===================================\                        ")
print("                   //                -Fun-                \\                      ")
print("                  ||                -Hacks-                ||                     ")
print("                  ||                 -For-                 ||                     ")
print("                  ||                 -The-                 ||                     ")
print("                  ||                -Whole-                ||                     ")
print("                  ||                -Family-               ||                     ")
print("                   \\                                     //                      ")
print("                     \===================================/                        ")
print(" ")
print(" ")
print("Please type ? or !")
print(" ")
print("[?]How to use")
print("or")
print("[!]Start Hack")
choice = input("")

if choice == "!":
    print("Starting...")
    time.sleep(1)
    print("\n" * 64) ## imo this makes more sense
    from subprocess import call
    call(["python", "kahoot.py"])

if choice == "?":
    print("Loading...")
    time.sleep(1)
    from subprocess import call
    call(["python", "HTU.py"])

time.sleep(10)
print("For more hacks go to↓↓↓")
print("https://mem.rip/kahoot/")
print(" ")
print(" ")
print("Software Made by CPScript")
print(" ")
print("   ▄▀ ▄▀   ")
print("    ▀  ▀   ")
print("  █▀▀▀▀▀█▄ ")
print("  █░░░░░█ █")
print("  ▀▄▄▄▄▄▀▀ ")
print(">CPScript<")
