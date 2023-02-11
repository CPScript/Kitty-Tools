# not made by CPScript
# Kahoot Flooder by xTobyPlayZ
# Edited by Zacky2613

from scripts.colors import ran,y,r,g,c
from scripts.sprint import sprint
from platform import platform
from subprocess import call
from time import sleep
from os import system
import platform
import requests
import socket    
import time
import sys
import re
import os

user_os = platform().split("-")[0]  
# Example Windows return: "Windows-10-10.0.00000-ABC"
# the .split() will return this: ['Windows', '10', '10.0.00000', 'ABC']
# We then get the first item which in this case is "Windows".
# P.S: I used a linux vm and the code works perfectly fine and returns "Linux" 

if user_os.lower() == "windows":
    delet = 'cls'
    dr = '\\'
else:
    delet = 'clear'
    dr = '/'
    
os.system('pip install selenium')
os.system(delet)


print("""                                                                           
                                                                           
                     .;c'                                                  
                   'l0Kc                                                   
                .:xXMWd.                            ..',;::;;,,'....       
              .l0WMMMX:                          'cx0XNWWWWMWWNX0kxol,     
             ;0WMMMMMO.                       .cONMMMMMMMMMN0dc,...        
            ;KMMMMMMMx.                    .;xXWMMMMMMMMWXd,.              
           .xWMMMMMMWo                   .cONMMMMMMMMMWKo.                 
           '0MMMMMMMNc                 .l0WMMMMMMMMMW0c.                   
           :XMMMMMMMX:              .;oKWMMMMMMMMMNO:.                     
           cNMMMMMMMX;            'dXWMMMMMMMMMMNk;.                       
           cNMMMMMMMK;          ,dXMMMMMMMMMMMNx,                          
           lNMMMMMMMK,        ,xXMMMMMMMMMMMXd,                            
           lWMMMMMMMK,      ,xNMMMMMMMMMMMXd'                              
           lWMMMMMMMK,    ,xNMMMMMMMMMMMXd'                                
           lWMMMMMMMK;  ,xXMMMMMMMMMMWXd'                                  
           lNMMMMMMMXc,xXMMMMMMMMMMWOo;                                    
           cNMMMMMMMWXXMMMMMMMMMMMMWX0Od,                                  
           cNMMMMMMMMMMMMMMMMMMMMMMMMMMMNx'                                
           cNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMK:                               
           cNMMMMMMMMMMMMMMMN00XWMMMMMMMMMMXl.                             
           cNMMMMMMMMMMMMNOl'. 'xNMMMMMMMMMMNo.                            
           cNMMMMMMMMWXOo,.     .dWMMMMMMMMMMNo.                           
           cNMMMMMMMWx'          .kWMMMMMMMMMMNl                           
           cNMMMMMMMX:            '0MMMMMMMMMMMX:                          
           :NMMMMMMMX:             :XMMMMMMMMMMM0,                         
           :NMMMMMMMX:              oXNMMMMMMMMMWk.                        
           :XMMMMMMMX;              .:kWMMMMMMMMMNo.                       
           :XMMMMMMMX;                ,KMMMMMMMMMMXc                       
           :XMMMMMMMX;                 cNMMMMMMMMMMK;                      
           :XMMMMMMMK,                 .dWMMMMMMMMMW0;                     
           :XMMMMMMXc                   .kWMMMMMMMMMMXo.           .,'     
           cNMMMMNk,                     'OWMMMMMMMMMMWKx:,....':looc'     
          'OWMWXx;                        'kWMMMMMMMMMMMMMWXKKK0xc.        
         .kWXkc.                           .lKWMMMMMMMMMMMWNOo;.           
        ;k0o'                                .cxKNWMWWNKOo:'               
       .;;.                                     .';:;,'.                   
 """)


# Initial imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from time import sleep
from names import FIRST, LAST
from random import choice
from sys import platform

# Declaring the path and user agent along with a tab counter
PATH = ""
if platform == "linux":
    PATH = "chromedriver/chromedriverlinux"
elif platform == "darwin":
    PATH = "chromedriver/chromedrivermac"
elif platform == "win32":
    PATH = "chromedriver/chromedriverwindows.exe"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/" \
             "537.36 (KHTML, like Gecko) Chrome/" \
             "87.0.4280.88 Safari/537.36"
tab_number = 0

print("Welcome to Kahoot Flooder")

# Getting the required user input
pin_input = int(input("Game Pin: "))
print("1) Custom names")
print("2) Random names")

name_choice = ""
bot_name_input = ""
random_names = False
while name_choice == "":
    name_choice = input("Choose an option: ")
    if name_choice == str(1):
        bot_name_input = input("Bot Name: ")
    elif name_choice == str(2):
        print("Using random names...")
        random_names = True
    else:
        print("That is not an option!")
        name_choice = ""

bot_amount_input = int(input("Bot Amount: "))

print(f"Sending {bot_amount_input} bots...")

# Declaring the options
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f"user-agent={USER_AGENT}")
options.add_argument("--window-size=1920,1080")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=PATH, options=options)


# Main loop that runs the amount of times the user specifies
def create_bot(tab, pin, bot_name):
    """
    Create a bot.

    Uses the pin and name to create as many bots as the user wants.

    :param tab: Keeps track of which tab the browser is on.
    :param pin: The pin for the Kahoot.
    :param bot_name: The name for each bot to be created.
    :return: None
    """
    if tab != 0:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[tab])

    # Navigating to Kahoot! (headless), then joining the game using
    # the provided pin and name the amount of times specified
    driver.get("https://kahoot.it")

    # Sending the bots
    pin_entry = driver.find_element_by_id("game-input")
    pin_entry.send_keys(pin)
    pin_entry.send_keys(Keys.RETURN)
    try:
        WebDriverWait(driver, 1).until(
            ec.presence_of_element_located(
                (By.ID, "nickname")))
        bot_name_entry = driver.find_element_by_id("nickname")
        bot_name_entry.send_keys(bot_name + str(i + 1))
        bot_name_entry.send_keys(Keys.RETURN)
    except TimeoutException:
        print("Pausing...")
        sleep(6)
        print("Continuing...")
    driver.delete_all_cookies()


for i in range(bot_amount_input):
    if random_names:
        bot_name_input = choice(FIRST) + choice(LAST)
    create_bot(tab_number, pin_input, bot_name_input)
    tab_number += 1


print("Bots have been delivered")

time.sleep(4)
os.system(delet)

print("Thank you for using Kahoot Flooder!")
time.sleep(5)
call(["python", "main.py"])
