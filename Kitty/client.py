import os
import time
from os import system
import platform

print("Attempting to check if imports are installed; colorama, pystyle.")
time.sleep(1)

def clear():
    system = platform.system().lower()

    if system == 'windows':
        _ = os.system('cls')
    elif system == 'linux' or system == 'darwin':
        _ = os.system('clear')
    elif system == 'android':
        System.Clear()
        print("How are you here, leave!")
        sprint(f"Please use the 'LITE' version so this kahoot client will run smoothly! {r}<3")
        exit()
clear() # Call clear func
try:
    import colorama 
    import pystyle
except ModuleNotFoundError:
    #from scripts.check import try_install | Idk how to fix the error for line 16, its 2am so idc
    print("Result: You dont have a certan import(s) installed, installing them now")
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

api = "https://play.kahoot.it/rest/kahoots/"
class Kahoot:
    def __init__(self, uuid):
        self.uuid = uuid
        try:
            if not re.fullmatch(r"^[A-Za-z0-9-]*$", uuid):
                self.data = False
            else:
                self.data = load(urlopen(f"https://play.kahoot.it/rest/kahoots/{uuid}"))
        except HTTPError or InvalidURL:
            self.data = False

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
        print("There was an error!  Mabey you typed the 'Quiz ID' incorrectly!\n")
        print(err)
    Write.Print(f"""
||=========================================================
||Thanks for using Kitty-Tools <3
||Please *STAR* this repo and follow the creator on github!
||=========================================================\n
""", Colors.red_to_purple, interval=0.000)

start_kahoot()


input("Press any key to exit...")
