#!/usr/bin/env python3
import os
import sys
import time
import platform
import subprocess
from pathlib import Path
from datetime import datetime

# Terminal Control Constants
class TermCtrl:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Foreground Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright Foreground Colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background Colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Clear Screen
    CLEAR = "\033[2J\033[H"
    
    # Cursor Movement
    @staticmethod
    def pos(x, y):
        return f"\033[{y};{x}H"

class SystemManager:
    @staticmethod
    def detect_platform():
        system = platform.system().lower()
        
        if system == 'windows':
            return "windows"
        elif system == 'linux':
            if os.path.exists("/data/data/com.termux"):
                return "android"
            return "linux"
        elif system == 'darwin':
            return "macos"
        else:
            return "unknown"
    
    @staticmethod
    def clear_screen():
        system = SystemManager.detect_platform()
        
        try:
            if system == "windows":
                os.system('cls')
            elif system in ["linux", "macos", "android"]:
                os.system('clear')
            else:
                print("\033[2J\033[H", end="")
        except Exception:
            print("\n" * 100)
            
    @staticmethod
    def detect_terminal_size():
        try:
            columns, lines = os.get_terminal_size()
            return columns, lines
        except:
            return 80, 24
    
    @staticmethod
    def is_dependency_installed(command):
        try:
            devnull = open(os.devnull, 'w')
            subprocess.check_call([command, "--version"], stdout=devnull, stderr=devnull)
            return True
        except:
            return False

class DependencyChecker:
    """Check and install Python dependencies"""
    
    @staticmethod
    def check_python_version():
        """Check if Python version is compatible"""
        if sys.version_info < (3, 6):
            print(f"{TermCtrl.BRIGHT_RED}Error: Python 3.6 or higher is required.{TermCtrl.RESET}")
            print(f"Current version: {sys.version}")
            return False
        return True
    
    @staticmethod
    def install_missing_packages():
        """Install missing Python packages"""
        packages_to_check = ['colorama', 'pystyle']
        missing_packages = []
        
        for package in packages_to_check:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"{TermCtrl.BRIGHT_YELLOW}Installing missing packages: {', '.join(missing_packages)}{TermCtrl.RESET}")
            for package in missing_packages:
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                    print(f"{TermCtrl.BRIGHT_GREEN}Successfully installed {package}{TermCtrl.RESET}")
                except subprocess.CalledProcessError:
                    print(f"{TermCtrl.BRIGHT_RED}Failed to install {package}{TermCtrl.RESET}")
        
        return True

class MenuManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.src_dir = os.path.join(self.base_dir, "src")
        self.gui_dir = os.path.join(self.base_dir, "src", "client")
        self.kitty_dir = os.path.join(self.base_dir, "Kitty")
        
        # Check if src directory exists
        self.is_src_available = os.path.isdir(self.src_dir)
        
        # Initialize terminal state
        self.term_width, self.term_height = SystemManager.detect_terminal_size()
        
        # Menu state
        self.exit_requested = False
        self.current_selection = 0
        self.menu_items = [
            {"id": "howto", "label": "How to Use", "description": "Interactive guide on using Kitty Tools            "},
            {"id": "info", "label": "Information", "description": "Credits, license, and additional information      "},
            {"id": "flood", "label": "Kahoot Flooder", "description": "Advanced Kahoot game flooding utility             "},
            {"id": "answers", "label": "Answer Hack", "description": "Obtain answers for Kahoot quizzes                 "},
            {"id": "graphical", "label": "GUI", "description": "A graphical user interface for ease of use        "},
            {"id": "exit", "label": "Exit", "description": "Exit the application                              "}
        ]
    
    def render_header(self):
        version_number = "v36.2 Enhanced"        
        print(f" {TermCtrl.BRIGHT_YELLOW}┌{'─' * (self.term_width - 4)}┐{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_YELLOW}│{TermCtrl.RESET} {TermCtrl.BOLD}{TermCtrl.BRIGHT_WHITE}KITTY TOOLS{TermCtrl.RESET} {TermCtrl.DIM}by CPScript{TermCtrl.RESET}{' ' * (self.term_width - 28)}{TermCtrl.DIM}{TermCtrl.RESET}{TermCtrl.BRIGHT_YELLOW}│{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_YELLOW}│{TermCtrl.RESET} {TermCtrl.DIM}{version_number}{TermCtrl.RESET}{' ' * (self.term_width - 17 - len(version_number))}{TermCtrl.BRIGHT_YELLOW}            │{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_YELLOW}└{'─' * (self.term_width - 4)}┘{TermCtrl.RESET}")
        print()
    
    def render_menu(self):
        print(f" {TermCtrl.BRIGHT_CYAN}╭{'─' * (self.term_width - 4)}╮{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET} {TermCtrl.BOLD}Main Menu{TermCtrl.RESET}{' ' * (self.term_width - 14)}{TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_CYAN}├{'─' * (self.term_width - 4)}┤{TermCtrl.RESET}")
        
        for idx, item in enumerate(self.menu_items):
            if idx == self.current_selection:
                selector = f"{TermCtrl.BRIGHT_GREEN}▶{TermCtrl.RESET}"
                label = f"{TermCtrl.BRIGHT_WHITE}{TermCtrl.BOLD}{item['label']}{TermCtrl.RESET}"
                desc = f"{TermCtrl.BRIGHT_WHITE}{item['description']}{TermCtrl.RESET}"
            else:
                selector = " "
                label = f"{TermCtrl.WHITE}{item['label']}{TermCtrl.RESET}"
                desc = f"{TermCtrl.DIM}{item['description']}{TermCtrl.RESET}"
            
            id_text = f"{idx + 1}. "
            spacing = " " * (20 - len(item['label']))
            print(f" {TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET} {selector} {id_text}{label}{spacing}{desc}{' ' * (self.term_width - 50 - len(item['description']))}{TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET}")
        
        print(f" {TermCtrl.BRIGHT_CYAN}╰{'─' * (self.term_width - 4)}╯{TermCtrl.RESET}")
        print()
        print(f" {TermCtrl.DIM}Use number keys to navigate, Enter to select{TermCtrl.RESET}")
    
    def render_status(self, message=None):
        platform_info = SystemManager.detect_platform()
        platform_label = f"{platform_info.capitalize()} platform detected"
        
        if message:
            status_text = message
        else:
            status_text = "Ready"
        
        print()
        print(f" {TermCtrl.BRIGHT_BLACK}Status: {TermCtrl.RESET}{status_text}")
        print(f" {TermCtrl.BRIGHT_BLACK}System: {TermCtrl.RESET}{platform_label}")
        
        # Check if enhanced version is available
        if self.is_src_available:
            print(f" {TermCtrl.BRIGHT_BLACK}Mode:   {TermCtrl.RESET}{TermCtrl.BRIGHT_GREEN}Enhanced Version Available{TermCtrl.RESET}")
        else:
            print(f" {TermCtrl.BRIGHT_BLACK}Mode:   {TermCtrl.RESET}{TermCtrl.YELLOW}Standard Version{TermCtrl.RESET}")

    def get_user_selection(self):
        try:
            choice = input("\n Make a selection (1-6): ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.menu_items):
                return int(choice) - 1
            return self.current_selection
        except KeyboardInterrupt:
            return len(self.menu_items) - 1  # Select exit option
        except:
            return self.current_selection
    
    def check_dependencies_for_action(self, action_id):
        """Check if dependencies are available for the selected action"""
        if action_id in ["flood", "answers", "graphical"]:
            # Check Python dependencies
            try:
                import colorama
                import pystyle
            except ImportError:
                print(f"{TermCtrl.BRIGHT_YELLOW}Installing required Python packages...{TermCtrl.RESET}")
                DependencyChecker.install_missing_packages()
            
            # For flooder, check Node.js
            if action_id == "flood":
                node_available = SystemManager.is_dependency_installed("node")
                npm_available = SystemManager.is_dependency_installed("npm")
                
                if not node_available or not npm_available:
                    print(f"{TermCtrl.BRIGHT_RED}Node.js is required for the Kahoot Flooder.{TermCtrl.RESET}")
                    print("The setup script will guide you through installation.")
                    time.sleep(2)
        
        return True
    
    def execute_selected_action(self, selection):
        action_id = self.menu_items[selection]["id"]
        
        # Check dependencies before executing
        if not self.check_dependencies_for_action(action_id):
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to the main menu...{TermCtrl.RESET}")
            return
        
        # Prepare to execute selected action
        print(f"\n {TermCtrl.BRIGHT_BLUE}Launching {self.menu_items[selection]['label']}...{TermCtrl.RESET}")
        time.sleep(1)
        SystemManager.clear_screen()
        
        try:
            if action_id == "howto":
                self.execute_howto()
            elif action_id == "info":
                self.execute_info()
            elif action_id == "flood":
                self.execute_flood()
            elif action_id == "answers":
                self.execute_answers()
            elif action_id == "graphical":
                self.execute_graphical()
            elif action_id == "exit":
                self.exit_requested = True
                print(f"{TermCtrl.BRIGHT_GREEN}Thank you for using KITTY TOOLS{TermCtrl.RESET}")
                return
                
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to the main menu...{TermCtrl.RESET}")
            
        except KeyboardInterrupt:
            print(f"\n{TermCtrl.BRIGHT_YELLOW}Operation cancelled by user{TermCtrl.RESET}")
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to the main menu...{TermCtrl.RESET}")
        except Exception as e:
            print(f"\n{TermCtrl.BRIGHT_RED}Error executing {action_id}: {str(e)}{TermCtrl.RESET}")
            print(f"{TermCtrl.DIM}If this error persists, please report it on GitHub{TermCtrl.RESET}")
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to the main menu...{TermCtrl.RESET}")
    
    def execute_howto(self):
        print(f"{TermCtrl.BOLD}{TermCtrl.BRIGHT_CYAN}How to Use KITTY TOOLS{TermCtrl.RESET}\n")
        
        if self.is_src_available:
            # Enhanced version
            print(f"{TermCtrl.BRIGHT_WHITE}KITTY TOOLS is a suite of utilities for Kahoot:{TermCtrl.RESET}\n")
            print(f"{TermCtrl.BRIGHT_CYAN}1. Information{TermCtrl.RESET}")
            print(f"   View credits, license information, and contributors to the project.")
            print(f"{TermCtrl.BRIGHT_CYAN}2. Kahoot Flooder{TermCtrl.RESET}")
            print(f"   Create multiple automated players in Kahoot games with customizable settings.")
            print(f"   You can control the bots collectively or let them act autonomously.")
            print(f"   Note: Requires Node.js installation")
            print(f"{TermCtrl.BRIGHT_CYAN}3. Answer Hack{TermCtrl.RESET}")
            print(f"   Retrieve answers for a Kahoot quiz by providing the Quiz ID.")
            print(f"   Export answers to a file for future reference.")
            print(f"{TermCtrl.BRIGHT_CYAN}4. GUI{TermCtrl.RESET}")
            print(f"   Use the graphical user interface for easier interaction.")
            print(f"   Requires PyQt5 installation.\n")
            print(f"{TermCtrl.BRIGHT_YELLOW}Note: All features require an active internet connection.{TermCtrl.RESET}")
            print(f"{TermCtrl.BRIGHT_YELLOW}Troubleshooting: If you encounter SSL errors, the tools will attempt to fix them automatically.{TermCtrl.RESET}")
        else:
            # Standard version
            try:
                subprocess.run([sys.executable, os.path.join(self.kitty_dir, "htu.py")])
            except Exception as e:
                print(f"Error running how-to guide: {e}")
                print("Please check the Kitty directory for the htu.py file")
    
    def execute_info(self):
        if self.is_src_available:
            # Enhanced version
            print(f"{TermCtrl.BOLD}{TermCtrl.BRIGHT_CYAN}KITTY TOOLS Information{TermCtrl.RESET}\n")
            print(f"{TermCtrl.BRIGHT_WHITE}KITTY TOOLS v36.2 Enhanced{TermCtrl.RESET}")
            print(f"Developed by: {TermCtrl.BRIGHT_YELLOW}CPScript{TermCtrl.RESET}\n")
            
            print(f"{TermCtrl.UNDERLINE}Contributors:{TermCtrl.RESET}")
            print(f"- {TermCtrl.BRIGHT_RED}@Ccode-lang{TermCtrl.RESET} for helping out!")
            print(f"- {TermCtrl.BRIGHT_RED}@xTobyPlayZ{TermCtrl.RESET} for Flooder!")
            print(f"- {TermCtrl.BRIGHT_RED}@cheepling{TermCtrl.RESET} for finding bugs!")
            print(f"- {TermCtrl.BRIGHT_RED}@Zacky2613{TermCtrl.RESET} for helping and fixing issues!")
            print(f"- {TermCtrl.BRIGHT_RED}@KiraKenjiro{TermCtrl.RESET} for reviewing and making changes! {TermCtrl.BRIGHT_RED}<3{TermCtrl.RESET}\n")
            
            print(f"{TermCtrl.UNDERLINE}License:{TermCtrl.RESET}")
            print(f"This software is provided for educational purposes only.")
            print(f"Use at your own risk. The authors are not responsible for any misuse.")
            print(f"Please read the complete license in the repository for more details.\n")
            
            print(f"{TermCtrl.UNDERLINE}Recent Fixes:{TermCtrl.RESET}")
            print(f"- Fixed SSL certificate issues on macOS")
            print(f"- Fixed HTTP 403 Forbidden errors with better headers")
            print(f"- Fixed Node.js module loading issues")
            print(f"- Added automatic dependency installation")
            print(f"- Improved error handling and user feedback\n")
            
            print(f"{TermCtrl.BRIGHT_GREEN}Thank you for using KITTY TOOLS!{TermCtrl.RESET}")
        else:
            # Standard version
            try:
                subprocess.run([sys.executable, os.path.join(self.kitty_dir, "Info", "main.py")])
            except Exception as e:
                print(f"Error running info module: {e}")
                print("Please check the Kitty/Info directory")
    
    def execute_flood(self):
        if self.is_src_available:
            # Enhanced version
            try:
                subprocess.run([sys.executable, os.path.join(self.src_dir, "main.py")])
            except Exception as e:
                print(f"Error running enhanced flooder: {e}")
                print("Falling back to standard version...")
                try:
                    subprocess.run([sys.executable, os.path.join(self.kitty_dir, "Flood", "main.py")])
                except Exception as e2:
                    print(f"Error running standard flooder: {e2}")
        else:
            # Standard version
            try:
                subprocess.run([sys.executable, os.path.join(self.kitty_dir, "Flood", "main.py")])
            except Exception as e:
                print(f"Error running flooder: {e}")
                print("Please check the Kitty/Flood directory")
    
    def execute_answers(self):
        if self.is_src_available:
            # Enhanced version
            try:
                subprocess.run([sys.executable, os.path.join(self.src_dir, "client.py")])
            except Exception as e:
                print(f"Error running enhanced client: {e}")
                print("Falling back to standard version...")
                try:
                    subprocess.run([sys.executable, os.path.join(self.kitty_dir, "client.py")])
                except Exception as e2:
                    print(f"Error running standard client: {e2}")
        else:
            # Standard version
            try:
                subprocess.run([sys.executable, os.path.join(self.kitty_dir, "client.py")])
            except Exception as e:
                print(f"Error running client: {e}")
                print("Please check the Kitty directory")
            
    def execute_graphical(self):
        if self.is_src_available:
            # Enhanced version - try GUI first, fallback to client
            try:
                # Check if PyQt5 is available
                import PyQt5
                subprocess.run([sys.executable, os.path.join(self.gui_dir, "main.py")])
            except ImportError:
                print(f"{TermCtrl.BRIGHT_YELLOW}PyQt5 not found. Installing...{TermCtrl.RESET}")
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyQt5'])
                    print(f"{TermCtrl.BRIGHT_GREEN}PyQt5 installed successfully. Starting GUI...{TermCtrl.RESET}")
                    subprocess.run([sys.executable, os.path.join(self.gui_dir, "main.py")])
                except subprocess.CalledProcessError:
                    print(f"{TermCtrl.BRIGHT_RED}Failed to install PyQt5. Using console client instead.{TermCtrl.RESET}")
                    subprocess.run([sys.executable, os.path.join(self.src_dir, "client.py")])
            except Exception as e:
                print(f"Error running GUI: {e}")
                print("Falling back to console client...")
                subprocess.run([sys.executable, os.path.join(self.src_dir, "client.py")])
        else:
            # Standard version - just run the client
            try:
                subprocess.run([sys.executable, os.path.join(self.kitty_dir, "client.py")])
            except Exception as e:
                print(f"Error running client: {e}")
    
    def run(self):
        while not self.exit_requested:
            SystemManager.clear_screen()
            self.term_width, self.term_height = SystemManager.detect_terminal_size()
            
            self.render_header()
            self.render_menu()
            self.render_status()
            
            selection = self.get_user_selection()
            if 0 <= selection < len(self.menu_items):
                self.current_selection = selection
                self.execute_selected_action(selection)

def check_system_requirements():
    """Check system requirements and dependencies"""
    print(f"{TermCtrl.BRIGHT_CYAN}Checking system requirements...{TermCtrl.RESET}")
    
    # Check Python version
    if not DependencyChecker.check_python_version():
        sys.exit(1)
    
    # Install missing Python packages
    DependencyChecker.install_missing_packages()
    
    print(f"{TermCtrl.BRIGHT_GREEN}System requirements check completed.{TermCtrl.RESET}")
    time.sleep(1)

def main():
    try:
        # Check system requirements first
        check_system_requirements()
        
        # Ensure necessary directories exist
        menu_manager = MenuManager()
        menu_manager.run()
        
    except KeyboardInterrupt:
        SystemManager.clear_screen()
        print(f"{TermCtrl.BRIGHT_GREEN}Thank you for using KITTY TOOLS{TermCtrl.RESET}")
    except Exception as e:
        print(f"{TermCtrl.BRIGHT_RED}A critical error occurred: {str(e)}{TermCtrl.RESET}")
        print(f"{TermCtrl.BRIGHT_YELLOW}Please report this issue on GitHub: https://github.com/CPScript/Kitty-Tools/issues{TermCtrl.RESET}")

if __name__ == "__main__":
    main()
