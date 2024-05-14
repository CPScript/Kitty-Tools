# This version is purly just a one file script with no extra fetures, the simpleist it can be!

import json
import urllib.request
import os
from os import system
import platform

print(f"'{system}'") # OS Alert

print("""
 - Kitty-Tools LITE v1.10 - 
======= For Termux =========

  Please enter your quiz ID
   /
>.<
----------------------------
""")
api = 'https://play.kahoot.it/rest/kahoots/'
usrinput = input(f" Enter ID >> ")
link = api + usrinput
finished = False

answers = {}
images = {}
questions = {}

try:
    with urllib.request.urlopen(link) as url:
        print("")
        data = json.load(url)
        quizlength = len(data['questions'])

        def is_a_question(dat):
            try:
                eval(dat)
                return True
            except KeyError:
                return False

        question = 0
        for x in range(quizlength):
            if is_a_question("data['questions'][question]['choices']"):
                try:
                    if data['questions'][question]['type'] == "quiz":
                        if data['questions'][question]['choices'][0]['correct']:
                            answers[f"Question {question + 1}"] = 'Red'
                        elif data['questions'][question]['choices'][1]['correct']:
                            answers[f"Question {question + 1}"] = 'Blue'
                        elif data['questions'][question]['choices'][2]['correct']:
                            answers[f"Question {question + 1}"] = 'Yellow'
                        elif data['questions'][question]['choices'][3]['correct']:
                            answers[f"Question {question + 1}"] = 'Green'
                    elif data['questions'][question]['type'] == "jumble":
                        length = len(data['questions'][question]['choices'])
                        for y in range(length):
                            if answers.get(f"Question {question + 1}") is None:
                                answers[f"Question {question + 1}"] = ""
                            answers[f"Question {question + 1}"] += str(data['questions'][question]['choices'][y]['answer']).upper()

                    elif data['questions'][question]['type'] == "survey":
                        answers[f"Question {question + 1}"] = "Could not find any answers"

                    elif data['questions'][question]['type'] == "content":
                        answers[f"Question {question + 1}"] = "Could not find any answers"

                    elif data['questions'][question]['type'] == "multiple_select_quiz":
                        multiselect = []
                        for z in range(len(data['questions'][question]['choices'])):
                            if data['questions'][question]['choices'][0]['correct']:
                                multiselect.append("Blue")

                            if data['questions'][question]['choices'][1]['correct']:
                                multiselect.append("Red")

                            if data['questions'][question]['choices'][2]['correct']:
                                multiselect.append("Yellow")

                            if data['questions'][question]['choices'][3]['correct']:
                                multiselect.append("Green")

                        answers[f"Question {question + 1}"] = list(dict.fromkeys(multiselect))
                    else:
                        answers[f"Question {question + 1}"] = 'Could not find any answers'

                    questions[f"Question {question + 1}"] = data["questions"][question]["question"]

                    if is_a_question('data["questions"][question]["image"]'):
                        images[f"Question {question + 1}"] = data["questions"][question]["image"]
                    else:
                        images[f"Question {question + 1}"] = None

                    question += 1
                    if question + 1 == quizlength:
                        finished = True
                except Exception as err:
                    print(err)
            else:
                answers[f"Question {question + 1}"] = 'Could not find any answers'
                images[f"Question {question + 1}"] = 'Could not find any images'
                questions[f"Question {question + 1}"] = 'Could not find the question'

                question += 1

except Exception as err:
    os.system('clear')
    print("Womp Womp! ")
    print("There was an error!  Mabey you typed the 'Quiz ID' incorrectly!\n")
    print(err)


def print_answers():
    for key, value in answers.items():
        if type(value) == list:
            print(key, ':', f"{', '.join(value)}\n")
        else:
            print(key, ':', f"{value}\n")


print_answers()

if finished:
    # try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(dir_path, "quizzes", f"{usrinput}.json")

    if not os.path.exists(os.path.join(dir_path, "quizzes")):
        os.mkdir(os.path.join(dir_path, "quizzes"), 0o666)

    if not os.path.exists(data_path):
        with open(data_path, "x") as f:
            startconfig = {"answers": {}, "questions": {}, "images": {}}
            json.dump(startconfig, f, indent=4)

    with open(data_path, "r") as f:
        config = json.load(f)

    for i, v in answers.items():
        if "Woops! Could not find any answers" in v:
            config["answers"][i] = None
        else:
            config["answers"][i] = v

    for i, v in questions.items():
        if "Woops! Could not find the question" in v:
            config["questions"][i] = None
        else:
            config["questions"][i] = str(v).replace("T or F: ", '').replace("</b>", '').replace("<b>T or  F: ", '').replace('<b>', '')

    for i, v in images.items():
        if "Woops! Could not find any images" in v:
            config["images"][i] = None
        else:
            config["images"][i] = v

    with open(data_path, "w+") as f:
        json.dump(config, f, indent=4)

    # except Exception as err:
    #     print(f"{err}\n")

input("Enter to exit...")
