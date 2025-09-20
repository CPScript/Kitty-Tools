#!/usr/bin/env python3
import os
import time
import sys
import platform
import json
import re
import threading
import random
import ssl
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, parse_qs
from http.client import InvalidURL

# Dependency management with graceful fallbacks
DEPENDENCIES = {
    "colorama": {"package": "colorama", "components": ["Fore", "Style"]},
    "pystyle": {"package": "pystyle", "components": ["Write", "System", "Colors", "Colorate", "Anime"]}
}

def check_and_install_dependencies():
    missing_deps = []
    
    for dep_name, dep_info in DEPENDENCIES.items():
        try:
            module = __import__(dep_info["package"])
            for component in dep_info["components"]:
                if not hasattr(module, component):
                    raise ImportError(f"Component {component} not found in {dep_name}")
        except (ImportError, ModuleNotFoundError):
            missing_deps.append(dep_info["package"])
    
    if missing_deps:
        print(f"Installing missing dependencies: {', '.join(missing_deps)}")
        for dep in missing_deps:
            install_status = os.system(f"pip install {dep}")
            if install_status != 0:
                print(f"Warning: Failed to install {dep}. Some features may not work correctly.")

check_and_install_dependencies()

from colorama import Fore, Style
from pystyle import Write, System, Colors, Colorate, Anime

class ColorScheme:
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    GREEN = Fore.GREEN
    BLUE = Fore.BLUE
    ORANGE = Fore.RED + Fore.YELLOW
    MAGENTA = Fore.MAGENTA
    LIGHTBLUE = Fore.LIGHTBLUE_EX
    CYAN = Fore.CYAN
    GRAY = Fore.LIGHTBLACK_EX + Fore.WHITE
    RESET = Fore.RESET
    PINK = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
    DARK_GREEN = Fore.GREEN + Style.BRIGHT
    PRETTY = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
    
    @classmethod
    def random(cls):
        colors = [cls.RED, cls.YELLOW, cls.GREEN, cls.BLUE, cls.CYAN, 
                 cls.MAGENTA, cls.LIGHTBLUE]
        return random.choice(colors)

class PlatformManager:    
    @staticmethod
    def detect_platform():
        system = platform.system().lower()
        
        if system == 'windows':
            return "windows"
        elif system == 'linux':
            # Check if running in Termux on Android
            if os.path.exists("/data/data/com.termux"):
                return "android"
            return "linux"
        elif system == 'darwin':
            return "macos"
        else:
            return "unknown"
    
    @staticmethod
    def clear_screen():
        system = PlatformManager.detect_platform()
        
        try:
            if system == "windows":
                os.system('cls')
            elif system in ["linux", "macos"]:
                os.system('clear')
            elif system == "android":
                os.system('clear')
                print("Notice: Running on Android. For optimal performance, consider using Kitty-Tools LITE.")
            else:
                print("\033[H\033[J", end="")
                print(f"Notice: Unsupported platform '{system}'. Some features may not work as expected.")
                print("For more info: https://github.com/CPScript/Kitty-Tools/extra.md")
        except Exception as e:
            # Last resort fallback
            print("\n" * 100)
            print(f"Screen clearing failed: {e}")

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

# Kahoot API interaction
class KahootAPI:    
    BASE_API_URL = "https://play.kahoot.it/rest/kahoots/"
    CHALLENGE_API_URL = "https://kahoot.it/rest/challenges/pin/"
    REQUEST_TIMEOUT = 15  # seconds
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.ssl_context = SSLContextManager.create_ssl_context()
    
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
    
    def _make_request(self, url, max_retries=3):
        """Make request with retry logic and proper error handling"""
        for attempt in range(max_retries):
            try:
                # Apply rate limiting
                self.rate_limiter.wait()
                
                # Create request with headers
                headers = self._get_headers()
                request = Request(url, headers=headers)
                
                # Make the request with SSL context
                with urlopen(request, timeout=self.REQUEST_TIMEOUT, context=self.ssl_context) as response:
                    return json.loads(response.read().decode('utf-8'))
                    
            except HTTPError as e:
                if e.code == 403:
                    print(f"Attempt {attempt + 1}: Access forbidden (403)")
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5
                        print(f"Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        return {'error': 'Access forbidden. This could be due to rate limiting, geographic restrictions, or the quiz being private.'}
                
                elif e.code == 404:
                    return {'error': 'Quiz not found. The ID may be incorrect.'}
                
                elif e.code == 429:  # Too Many Requests
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 10
                        print(f"Rate limited. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        return {'error': 'Rate limited by server. Please wait a few minutes and try again.'}
                
                else:
                    return {'error': f'HTTP Error: {e.code} - {e.reason}'}
                    
            except URLError as e:
                return {'error': f'Connection error: {e.reason}. Check your internet connection.'}
                
            except ssl.SSLError as e:
                print(f"SSL Error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    # Try with unverified context on next attempt
                    self.ssl_context = ssl._create_unverified_context()
                    print("Retrying with unverified SSL context...")
                    continue
                else:
                    return {'error': f'SSL connection failed: {e}'}
                    
            except json.JSONDecodeError:
                return {'error': 'Failed to parse the response from Kahoot servers.'}
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(2)
                    continue
                else:
                    return {'error': f'Unexpected error: {str(e)}'}
        
        return {'error': 'All retry attempts failed'}
    
    @staticmethod
    def get_quiz_by_id(quiz_id):
        if not re.fullmatch(r"^[A-Za-z0-9-]*$", quiz_id):
            return {'error': 'Invalid quiz ID format'}
        
        api = KahootAPI()
        url = f"{api.BASE_API_URL}{quiz_id}"
        return api._make_request(url)
    
    @staticmethod
    def get_quiz_id_from_pin(pin):
        if not pin.isdigit():
            return {'error': 'PIN must contain only digits'}
            
        api = KahootAPI()
        url = f"{api.CHALLENGE_API_URL}{pin}"
        result = api._make_request(url)
        
        if 'error' not in result and 'id' in result:
            return {'quiz_id': result['id']}
        elif 'error' not in result:
            return {'error': 'No quiz ID found in response'}
        
        return result

class KahootQuiz:    
    def __init__(self, quiz_data):
        self.data = quiz_data
        self.valid = 'error' not in quiz_data and 'uuid' in quiz_data
    
    def get_quiz_details(self):
        if not self.valid:
            return None
            
        return {
            "uuid": self.data["uuid"],
            "creator_username": self.data.get("creator_username", "Unknown"),
            "title": self.data.get("title", "Untitled Quiz"),
            "description": self.data.get("description", ""),
            "cover": self.data.get("cover", ""),
            "question_count": len(self.data.get("questions", [])),
            "visibility": self.data.get("visibility", "Unknown"),
            "created": self.data.get("created", "Unknown date")
        }
    
    def get_questions(self):
        if not self.valid:
            return []
        return self.data.get("questions", [])
    
    def get_quiz_length(self):
        if not self.valid:
            return 0
        return len(self.data.get("questions", []))
    
    def _clean_text(self, text):
        if not text:
            return ""
            
        text = str(text)
        
        replacements = [
            ("<p>", ""), ("</p>", ""), 
            ("<strong>", ""), ("</strong>", ""),
            ("<b>", ""), ("</b>", ""),
            ("<br/>", "\n"), ("<br>", "\n"),
            ("<span>", ""), ("</span>", ""),
            ("<math>", ""), ("</math>", ""),
            ("<semantics>", ""), ("</semantics>", ""),
            ("<mrow>", ""), ("</mrow>", ""),
            ("<mo>", ""), ("</mo>", ""),
            ("<msup>", ""), ("</msup>", ""),
            ("<mi>", ""), ("</mi>", ""),
            ("<mn>", ""), ("</mn>", ""),
            ("<annotation>", ""), ("</annotation>", "")
        ]
        
        for old, new in replacements:
            text = text.replace(old, new)
        
        text = re.sub(r'<[^>]+>', '', text)
        
        text = text.replace('\\"', '"')
        
        return text.strip()
    
    def get_question_details(self, question_index):
        if not self.valid or question_index >= self.get_quiz_length():
            return None
            
        question = self.data["questions"][question_index]
        question_type = question.get("type", "unknown")
        
        details = {
            "type": question_type,
            "layout": question.get("layout"),
            "image": question.get("image"),
            "pointsMultiplier": question.get("pointsMultiplier", 1),
            "time": question.get("time"),
            "media": question.get("media")
        }
        
        if question_type == "content":
            details.update({
                "title": self._clean_text(question.get("title", "")),
                "description": self._clean_text(question.get("description", ""))
            })
        else:
            # Process question and choices
            details.update({
                "question": self._clean_text(question.get("question", "")),
                "choices": [],
                "amount_of_answers": len(question.get("choices", [])),
                "amount_of_correct_answers": 0
            })
            
            # Process each answer choice
            for choice in question.get("choices", []):
                cleaned_choice = {
                    "answer": self._clean_text(choice.get("answer", "")),
                    "correct": choice.get("correct", False)
                }
                
                details["choices"].append(cleaned_choice)
                if cleaned_choice["correct"]:
                    details["amount_of_correct_answers"] += 1
        
        return details
    
    def get_answer(self, question_index):
        details = self.get_question_details(question_index)
        
        if not details:
            return None
            
        if details["type"] == "content":
            return None  # Content slides don't have answers
            
        answers = []
        
        if details["type"] == "jumble":
            for choice in details["choices"]:
                answers.append(choice["answer"])
        else:
            for choice in details["choices"]:
                if choice["correct"]:
                    answers.append(choice["answer"])
                    
        return answers if answers else None
    
    def export_answers_to_file(self, filename="kahoot_answers.txt"):
        if not self.valid:
            return False
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                quiz_details = self.get_quiz_details()
                f.write(f"KAHOOT QUIZ ANSWERS\n")
                f.write(f"=================\n\n")
                f.write(f"Title: {quiz_details['title']}\n")
                f.write(f"Creator: {quiz_details['creator_username']}\n")
                f.write(f"Quiz ID: {quiz_details['uuid']}\n")
                if quiz_details['description']:
                    f.write(f"Description: {quiz_details['description']}\n")
                f.write(f"Question Count: {quiz_details['question_count']}\n\n")
                f.write(f"QUESTIONS AND ANSWERS\n")
                f.write(f"====================\n\n")
                
                for i in range(self.get_quiz_length()):
                    details = self.get_question_details(i)
                    
                    if details["type"] == "content":
                        f.write(f"SLIDE {i+1}: {details['title']}\n")
                        if details['description']:
                            f.write(f"Description: {details['description']}\n")
                    else:
                        f.write(f"QUESTION {i+1}: {details['question']}\n")
                        f.write(f"Type: {details['type']}\n")
                        
                        answers = self.get_answer(i)
                        if answers:
                            f.write(f"Correct Answer(s): {', '.join(answers)}\n")
                        else:
                            f.write(f"No correct answers found.\n")
                    
                    f.write("\n")
                
            return True
        except Exception as e:
            print(f"Failed to export answers: {str(e)}")
            return False

class KahootClientUI:    
    @staticmethod
    def display_intro():
        PlatformManager.clear_screen()
        
        print("NOTICE: This is an enhanced version of the Kitty-Tools Kahoot client.")
        
        Write.Print(f"""
       _______________________
      || Enter your quiz ID  ||
      || below! <3           ||
      |//
(>﹏<)
--------------------------------------
---- Kitty-Tools | By <> CPScript ----
---- Enhanced Edition v1.0 ----------
--------------------------------------
    \n""", Colors.orange, interval=0.000)
    
    @staticmethod
    def get_quiz_id():
        while True:
            Write.Print(f"┌─[Enter Kahoot-ID] <> [User-Input]\n", Colors.white, interval=0.000)
            Write.Print(f"└─────► ", Colors.white, interval=0.000)
            user_input = input(ColorScheme.PRETTY)
            
            if user_input.isdigit():
                print(f"{ColorScheme.ORANGE}({ColorScheme.GREEN}!{ColorScheme.ORANGE}) Detected a game PIN. Attempting to fetch the quiz ID...")
                result = KahootAPI.get_quiz_id_from_pin(user_input)
                
                if 'error' in result:
                    print(f"{ColorScheme.RED}Error: {result['error']}")
                    retry = input(f"{ColorScheme.YELLOW}Try again? (y/n): {ColorScheme.RESET}").lower()
                    if retry != 'y':
                        return None
                else:
                    quiz_id = result['quiz_id']
                    print(f"{ColorScheme.GREEN}Successfully found quiz ID: {quiz_id}")
                    time.sleep(1)
                    return quiz_id
            else:
                if re.fullmatch(r"^[A-Za-z0-9-]*$", user_input):
                    return user_input
                else:
                    print(f"{ColorScheme.RED}Invalid quiz ID format. It should contain only letters, numbers, and hyphens.")
                    retry = input(f"{ColorScheme.YELLOW}Try again? (y/n): {ColorScheme.RESET}").lower()
                    if retry != 'y':
                        return None
    
    @staticmethod
    def display_answers(kahoot):
        """Display quiz answers with proper formatting and color coding."""
        if not kahoot.valid:
            print(f"{ColorScheme.RED} Failed to retrieve quiz data. Please check the Quiz ID and try again.")
            return
            
        quiz_details = kahoot.get_quiz_details()
        
        print(f"\n{ColorScheme.CYAN}========= QUIZ INFORMATION =========")
        print(f"{ColorScheme.PRETTY}{ColorScheme.ORANGE}[{ColorScheme.RESET}Title{ColorScheme.ORANGE}]{ColorScheme.GREEN}--{ColorScheme.ORANGE}[{ColorScheme.RESET}{quiz_details['title']}{ColorScheme.ORANGE}]{ColorScheme.RESET}")
        print(f"{ColorScheme.PRETTY}{ColorScheme.ORANGE}[{ColorScheme.RESET}Creator{ColorScheme.ORANGE}]{ColorScheme.GREEN}--{ColorScheme.ORANGE}[{ColorScheme.RESET}{quiz_details['creator_username']}{ColorScheme.ORANGE}]{ColorScheme.RESET}")
        print(f"{ColorScheme.PRETTY}{ColorScheme.ORANGE}[{ColorScheme.RESET}Questions{ColorScheme.ORANGE}]{ColorScheme.GREEN}--{ColorScheme.ORANGE}[{ColorScheme.RESET}{quiz_details['question_count']}{ColorScheme.ORANGE}]{ColorScheme.RESET}")
        print(f"{ColorScheme.CYAN}====================================\n")
        
        output_lock = threading.Lock()
        
        for i in range(kahoot.get_quiz_length()):
            question_details = kahoot.get_question_details(i)
            
            with output_lock:
                if question_details["type"] == "content":
                    print(f"{ColorScheme.YELLOW}SLIDE {i+1}: {question_details['title']}")
                    if question_details.get('description'):
                        print(f"{ColorScheme.GRAY}Description: {question_details['description']}{ColorScheme.RESET}\n")
                else:
                    print(f"{ColorScheme.PRETTY}{ColorScheme.ORANGE}[{ColorScheme.RESET}Question {i+1}{ColorScheme.ORANGE}]{ColorScheme.GREEN}--{ColorScheme.ORANGE}[{ColorScheme.RESET}{question_details['question']}{ColorScheme.ORANGE}]{ColorScheme.RESET}")
                    
                    answers = kahoot.get_answer(i)
                    if answers:
                        print(f"{ColorScheme.PRETTY}{ColorScheme.ORANGE}[{ColorScheme.RESET}Answer{ColorScheme.ORANGE}]{ColorScheme.GREEN}--{ColorScheme.ORANGE}[{ColorScheme.RESET}{', '.join(answers)}{ColorScheme.ORANGE}]{ColorScheme.RESET}\n")
                    else:
                        print(f"{ColorScheme.PRETTY}{ColorScheme.ORANGE}[{ColorScheme.RESET}Answer{ColorScheme.ORANGE}]{ColorScheme.GREEN}--{ColorScheme.ORANGE}[{ColorScheme.RESET}No correct answers found{ColorScheme.ORANGE}]{ColorScheme.RESET}\n")
            
            time.sleep(0.010)
    
    @staticmethod
    def display_options(kahoot):
        if not kahoot.valid:
            return
            
        print(f"\n{ColorScheme.CYAN}========= ADDITIONAL OPTIONS =========")
        print(f"{ColorScheme.YELLOW}1. {ColorScheme.RESET}Export answers to a text file")
        print(f"{ColorScheme.YELLOW}2. {ColorScheme.RESET}Return to main menu")
        print(f"{ColorScheme.YELLOW}3. {ColorScheme.RESET}Exit")
        print(f"{ColorScheme.CYAN}======================================\n")
        
        choice = input(f"{ColorScheme.PRETTY}Select an option: {ColorScheme.RESET}")
        
        if choice == "1":
            filename = input(f"{ColorScheme.PRETTY}Enter filename (default: kahoot_answers.txt): {ColorScheme.RESET}") or "kahoot_answers.txt"
            if kahoot.export_answers_to_file(filename):
                print(f"{ColorScheme.GREEN}Answers successfully exported to {filename}")
            else:
                print(f"{ColorScheme.RED}Failed to export answers.")
        elif choice == "2":
            return "menu"
        else:
            return "exit"

def start_kahoot():
    try:
        while True:
            KahootClientUI.display_intro()
            
            quiz_id = KahootClientUI.get_quiz_id()
            if not quiz_id:
                print(f"{ColorScheme.RED}Operation cancelled.")
                break
                
            print(f"{ColorScheme.PRETTY}{ColorScheme.ORANGE}({ColorScheme.GREEN}!{ColorScheme.ORANGE}) Fetching Answers From: {ColorScheme.ORANGE}[{ColorScheme.RESET}Quiz-ID: {quiz_id}{ColorScheme.ORANGE}]\n")
            
            quiz_data = KahootAPI.get_quiz_by_id(quiz_id)
            
            if 'error' in quiz_data:
                print(f"{ColorScheme.RED}Error: {quiz_data['error']}")
                retry = input(f"{ColorScheme.YELLOW}Try again? (y/n): {ColorScheme.RESET}").lower()
                if retry != 'y':
                    break
                continue
                
            kahoot = KahootQuiz(quiz_data)
            
            KahootClientUI.display_answers(kahoot)
            
            result = KahootClientUI.display_options(kahoot)
            
            if result == "exit":
                break
            elif result != "menu":
                input(f"\n{ColorScheme.CYAN}Press any key to exit...{ColorScheme.RESET}")
                break
    
    except KeyboardInterrupt:
        print(f"\n{ColorScheme.YELLOW}Operation cancelled by user.{ColorScheme.RESET}")
    except Exception as e:
        print(f"\n{ColorScheme.RED}An unexpected error occurred: {str(e)}{ColorScheme.RESET}")
    
    print(f"""
{ColorScheme.RED}||=========================================================
||Thanks for using Kitty-Tools <3
||Please *STAR* this repo and follow the creator on github!
||=========================================================\n
{ColorScheme.RESET}""")

if __name__ == "__main__":
    start_kahoot()
