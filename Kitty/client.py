import os
import time
from os import system
import platform
import json
import re
import ssl
import random
import threading
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, parse_qs
from http.client import InvalidURL

print("Attempting to check if imports are installed; colorama, pystyle.")
time.sleep(1)

def clear():
    system = platform.system().lower()

    if system == 'windows':
        _ = os.system('cls')
    elif system == 'linux' or system == 'darwin':
        _ = os.system('clear')
    elif system == 'android':
        _ = os.system('clear')
        print("How are you here, leave!")
        print("Please use the 'LITE' version so this kahoot client will run smoothly!")
        exit()
clear() # Call clear func

try:
    import colorama 
    import pystyle
except ModuleNotFoundError:
    print("Result: You dont have a certain import(s) installed, installing them now")
    time.sleep(1)
    os.system("pip install colorama")
    os.system("pip install pystyle")
    clear()

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse, parse_qs
from json import load
from http.client import InvalidURL
import json, random, string, re, ctypes, threading
from colorama import Fore, Style
from pystyle import Write, System, Colors, Colorate, Anime
from datetime import datetime

# Colors :D
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

output_lock = threading.Lock()
colorama.init()

class SSLContextManager:
    """Handle SSL certificate issues across platforms"""
    
    @staticmethod
    def create_ssl_context():
        """Create SSL context with fallback for certificate issues"""
        try:
            # Try to create default context first
            context = ssl.create_default_context()
            
            # For macOS, try to use certifi if available
            if platform.system() == 'Darwin':
                try:
                    import certifi
                    context = ssl.create_default_context(cafile=certifi.where())
                except ImportError:
                    # certifi not available, use default
                    pass
            
            return context
        except Exception:
            # If all else fails, create unverified context
            print("Warning: Using unverified SSL context due to certificate issues")
            return ssl._create_unverified_context()

class RateLimiter:
    """Rate limiter to avoid getting blocked"""
    
    def __init__(self, min_delay=1.0, max_delay=3.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request = None
    
    def wait(self):
        """Wait appropriate time between requests"""
        if self.last_request:
            elapsed = time.time() - self.last_request
            delay = random.uniform(self.min_delay, self.max_delay)
            
            if elapsed < delay:
                sleep_time = delay - elapsed
                time.sleep(sleep_time)
        
        self.last_request = time.time()

# Enhanced Kahoot API
api = "https://play.kahoot.it/rest/kahoots/"

class Kahoot:
    def __init__(self, uuid):
        self.uuid = uuid
        self.rate_limiter = RateLimiter()
        self.ssl_context = SSLContextManager.create_ssl_context()
        
        try:
            if not re.fullmatch(r"^[A-Za-z0-9-]*$", uuid):
                self.data = False
            else:
                self.data = self._fetch_quiz_data(uuid)
        except HTTPError or InvalidURL:
            self.data = False

    def _get_headers(self):
        """Generate realistic browser headers"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }

    def _fetch_quiz_data(self, uuid):
        """Fetch quiz data with enhanced error handling"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Apply rate limiting
                self.rate_limiter.wait()
                
                url = f"https://play.kahoot.it/rest/kahoots/{uuid}"
                headers = self._get_headers()
                request = Request(url, headers=headers)
                
                with urlopen(request, timeout=15, context=self.ssl_context) as response:
                    return load(response)
                    
            except HTTPError as e:
                if e.code == 403:
                    print(f"Attempt {attempt + 1}: Access forbidden (403)")
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5
                        print(f"Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print("Error: Access forbidden. This could be due to rate limiting or geographic restrictions.")
                        return False
                
                elif e.code == 404:
                    print("Error: Quiz not found. Please verify the Quiz ID is correct.")
                    return False
                
                elif e.code == 429:  # Too Many Requests
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 10
                        print(f"Rate limited. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print("Error: Rate limited by server. Please wait a few minutes and try again.")
                        return False
                
                else:
                    print(f"HTTP Error {e.code}: {e.reason}")
                    return False
                    
            except URLError as e:
                print(f"Connection error: {e.reason}")
                return False
                
            except ssl.SSLError as e:
                print(f"SSL Error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    # Try with unverified context on next attempt
                    self.ssl_context = ssl._create_unverified_context()
                    print("Retrying with unverified SSL context...")
                    continue
                else:
                    print(f"SSL connection failed: {e}")
                    return False
                    
            except json.JSONDecodeError:
                print("Error: Failed to parse the response from Kahoot servers.")
                return False
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(2)
                    continue
                else:
                    print(f"Unexpected error: {str(e)}")
                    return False
        
        return False

    def get_quiz_details(self):
        return {
            "uuid": self.data["uuid"],
            "creator_username": self.data["creator_username"],
            "title": self.data["title"],
            "description": self.data["description"],
            "cover": self.data["cover"]}

    def get_questions(self):
        return self.data["questions"]

    def get_question_names(self):
        questions = []
        for i in range(self.get_quiz_length()):
            if self.get_question_details(i)["type"] == "content":
                questions.append(self.get_question_details(i)["title"])
            else:
                questions.append(self.get_question_details(i)["question"])
        return questions

    def get_quiz_length(self):
        return len(self.data["questions"])

    def get_question_details(self, question):
        if self.data["questions"][question]["type"] == "content":
            data = {
                "type": "content",
                "title": self.data["questions"][question]["title"],
                "description": self.data["questions"][question]["description"]
            }
        else:
            data = {
                "type": self.data["questions"][question]["type"],
                "question": str(self.data["questions"][question]["question"]).replace('"', '\\"').replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>", "").replace("<br/>", "\n").replace("</span>", "").replace("</mo>", "").replace("</mrow>", "").replace("<mn>", "").replace("</mn>", "").replace("</annotation>", "").replace("</semantics>", "").replace("</math>", "").replace("<span>", "").replace("<math>", "").replace("<semantics>", "").replace("<mrow>", "").replace("<mo>", "").replace("<msup>", "").replace("<mi>", "").replace("</mi>", "").replace("</msup>", "").replace("<b>", "").replace("</b>", ""),
                "choices": self.data["questions"][question]["choices"],
                "amount_of_answers": len(self.data["questions"][question]["choices"]),
                "amount_of_correct_answers": 0}

            for i in range(len(self.data["questions"][question]["choices"])):
                self.data["questions"][question]["choices"][i]["answer"] = self.data["questions"][question]["choices"][i]["answer"].replace('"', '\\"').replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>", "").replace("<br/>", "\n").replace("</span>", "").replace("</mo>", "").replace("</mrow>", "").replace("<mn>", "").replace("</mn>", "").replace("</annotation>", "").replace("</semantics>", "").replace("</math>", "").replace("<span>", "").replace("<math>", "").replace("<semantics>", "").replace("<mrow>", "").replace("<mo>", "").replace("<msup>", "").replace("<mi>", "").replace("</mi>", "").replace("</msup>", "").replace("<b>", "").replace("</b>", "")

            for i in range(len(self.data["questions"][question]["choices"])):
                if self.data["questions"][question]["choices"][i]["correct"]:
                    data["amount_of_correct_answers"] += 1

        if "layout" in self.data["questions"][question]:
            data["layout"] = self.data["questions"][question]["layout"]
        else:
            data["layout"] = None

        if "image" in self.data["questions"][question]:
            data["image"] = self.data["questions"][question]["image"]
        else:
            data["image"] = None

        if "pointsMultiplier" in self.data["questions"][question]:
            data["pointsMultiplier"] = self.data["questions"][question]["pointsMultiplier"]
        else:
            data["pointsMultiplier"] = None

        if "time" in self.data["questions"][question]:
            data["time"] = self.data["questions"][question]["time"]
        else:
            data["time"] = None

        return data

    def get_answer(self, question):
        answers = []
        if self.get_question_details(question)["type"] == "content":
            answers = None

        elif self.get_question_details(question)["type"] == "jumble":
            for i in self.get_question_details(question)["choices"]:
                answers.append(str(i["answer"]).replace('"', '\\"').replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>", "").replace("<br/>", "\n").replace("</span>", "").replace("</mo>", "").replace("</mrow>", "").replace("<mn>", "").replace("</mn>", "").replace("</annotation>", "").replace("</semantics>", "").replace("</math>", "").replace("<span>", "").replace("<math>", "").replace("<semantics>", "").replace("<mrow>", "").replace("<mo>", "").replace("<msup>", "").replace("<mi>", "").replace("</mi>", "").replace("</msup>", "").replace("<b>", "").replace("</b>", ""))

        else:
            for i in self.get_question_details(question)["choices"]:
                if i["correct"]:
                    answers.append(str(i["answer"]).replace('"', '\\"').replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>", "").replace("<br/>", "\n").replace("</span>", "").replace("</mo>", "").replace("</mrow>", "").replace("<mn>", "").replace("</mn>", "").replace("</annotation>", "").replace("</semantics>", "").replace("</math>", "").replace("<span>", "").replace("<math>", "").replace("<semantics>", "").replace("<mrow>", "").replace("<mo>", "").replace("<msup>", "").replace("<mi>", "").replace("</mi>", "").replace("</msup>", "").replace("<b>", "").replace("</b>", ""))
            if len(answers) == 0:
                answers = None
        return answers

def start_kahoot():
    print("NOTICE: This version is under development and sometimes it might bug, please create an issue at 'https://github.com/CPScript/Kitty-tools/issues' and we will try to fix it <3")
    Write.Print(f"""
       _______________________
      || Enter your quiz ID  ||
      || below! <3           ||
      |//
(>﹏<)
--------------------------------------
---- Kitty-Tools | By <> CPScript ----
--------------------------------------
    \n""", Colors.orange, interval=0.000)
    Write.Print(f"┌─[Enter Kahoot-ID] <> [User-Input]\n", Colors.white, interval=0.000)
    Write.Print(f"└─────► ", Colors.white, interval=0.000); quiz_id = input(pretty)
    try:
        kahoot = Kahoot(quiz_id)
        
        if not kahoot.data:
            print(f"{red}Error: Failed to fetch quiz data. Please check the Quiz ID and try again.{reset}")
            input("Press any key to exit...")
            return
            
        print(f"{pretty}{orange}({green}!{orange}) Fetching Answers From: {orange}[{reset}Quiz-ID: {quiz_id}{orange}]\n")
        time.sleep(1)
        for i in range(kahoot.get_quiz_length()):
            if kahoot.get_answer(i) is not None:
                if kahoot.get_question_details(i)['type'] == 'open_ended':
                    with output_lock:
                        print(f"{pretty}{orange}[{reset}Question{orange}]{green}--{orange}[{reset}{kahoot.get_question_names()[i]}{orange}]{reset}\n{pretty}{orange}[{reset}Answer{orange}]{green}--{orange}[{reset}{', '.join(kahoot.get_answer(i))}{orange}]{reset}\n")
                else:
                    with output_lock:
                        print(f"{pretty}{orange}[{reset}Question{orange}]{green}--{orange}[{reset}{kahoot.get_question_names()[i]}{orange}]{reset}\n{pretty}{orange}[{reset}Answer{orange}]{green}--{orange}[{reset}{', '.join(kahoot.get_answer(i))}{orange}]{reset}\n")
            time.sleep(0.010)
    except Exception as err:
        os.system('clear')
        print("Womp Womp! ")
        print("There was an error!  Maybe you typed the 'Quiz ID' incorrectly!\n")
        print(f"Error details: {err}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify the Quiz ID is correct")
        print("3. The quiz might be private or restricted")
        print("4. Try again in a few minutes")
    Write.Print(f"""
||=========================================================
||Thanks for using Kitty-Tools <3
||Please *STAR* this repo and follow the creator on github!
||=========================================================\n
""", Colors.red_to_purple, interval=0.000)

start_kahoot()

input("Press any key to exit...")
