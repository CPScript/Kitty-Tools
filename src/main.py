#!/usr/bin/env python3
import os
import sys
import time
import json
import platform
import subprocess
import shutil
from pathlib import Path

class ColorOutput:
    # ANSI color codes
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    @staticmethod
    def print_colored(text, color):
        print(f"{color}{text}{ColorOutput.RESET}")
    
    @staticmethod
    def success(text):
        ColorOutput.print_colored(text, ColorOutput.GREEN)
    
    @staticmethod
    def error(text):
        ColorOutput.print_colored(text, ColorOutput.RED)
    
    @staticmethod
    def info(text):
        ColorOutput.print_colored(text, ColorOutput.CYAN)
    
    @staticmethod
    def warning(text):
        ColorOutput.print_colored(text, ColorOutput.YELLOW)

class PlatformManager:    
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
        system = PlatformManager.detect_platform()
        
        try:
            if system == "windows":
                os.system('cls')
            elif system in ["linux", "macos", "android"]:
                os.system('clear')
            else:
                print("\033[H\033[J", end="")
        except Exception:
            print("\n" * 100)

class NodeJSManager:
    REQUIRED_PACKAGES = [
        "readline-sync",
        "kahoot.js-updated",
        "an-array-of-english-words",
        "request",
        "random-name",
        "console-title",
        "beepbeep"
    ]
    
    @staticmethod
    def check_node_installed():
        try:
            result = subprocess.run(
                ["node", "--version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            return result.returncode == 0
        except Exception:
            return False
    
    @staticmethod
    def check_npm_installed():
        try:
            result = subprocess.run(
                ["npm", "--version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            return result.returncode == 0
        except Exception:
            return False
    
    @staticmethod
    def install_node_packages():
        ColorOutput.info("Installing required Node.js packages...")
        
        for package in NodeJSManager.REQUIRED_PACKAGES:
            ColorOutput.info(f"Installing {package}...")
            try:
                subprocess.run(
                    ["npm", "install", package, "--no-fund", "--no-audit"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )
                ColorOutput.success(f"Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                ColorOutput.error(f"Failed to install {package}: {e}")
                return False
            except Exception as e:
                ColorOutput.error(f"Unexpected error installing {package}: {e}")
                return False
        
        return True
    
    @staticmethod
    def suggest_node_installation():
        platform_name = PlatformManager.detect_platform()
        
        ColorOutput.error("Node.js is required but not found on your system.")
        ColorOutput.info("Please install Node.js using the following instructions:")
        
        if platform_name == "windows":
            ColorOutput.info("1. Download the installer from https://nodejs.org/")
            ColorOutput.info("2. Run the installer and follow the installation wizard")
            ColorOutput.info("3. Restart your computer after installation")
        elif platform_name == "linux":
            ColorOutput.info("Install Node.js using your package manager:")
            ColorOutput.info("  Ubuntu/Debian: sudo apt update && sudo apt install nodejs npm")
            ColorOutput.info("  Fedora: sudo dnf install nodejs npm")
            ColorOutput.info("  Arch: sudo pacman -S nodejs npm")
        elif platform_name == "macos":
            ColorOutput.info("1. Install Homebrew if not already installed:")
            ColorOutput.info("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            ColorOutput.info("2. Install Node.js: brew install node")
        elif platform_name == "android":
            ColorOutput.info("In Termux, run: pkg install nodejs")
        else:
            ColorOutput.info("Please visit https://nodejs.org/ for installation instructions for your platform")
    
    @staticmethod
    def run_flood_script(script_path):
        if not os.path.exists(script_path):
            ColorOutput.error(f"Flood script not found at: {script_path}")
            return False
        
        try:
            # Run the process and forward output to console
            process = subprocess.Popen(
                ["node", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            for line in iter(process.stdout.readline, ''):
                print(line, end='')
            
            process.stdout.close()
            return_code = process.wait()
            
            if return_code != 0:
                ColorOutput.error(f"Flood script exited with error code: {return_code}")
                return False
            
            return True
            
        except KeyboardInterrupt:
            ColorOutput.warning("Flood operation cancelled by user")
            return False
        except Exception as e:
            ColorOutput.error(f"Error running flood script: {e}")
            return False

class FloodManager:    
    def __init__(self):
        """Initialize the flood manager."""
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.flood_js_path = os.path.join(self.script_dir, "flood.js")
        
        # Create package.json if it doesn't exist to help with npm installs
        self.ensure_package_json()
    
    def ensure_package_json(self):
        package_json_path = os.path.join(self.script_dir, "package.json")
        
        if not os.path.exists(package_json_path):
            package_data = {
                "name": "kitty-tools-kahoot-flooder",
                "version": "1.0.0",
                "description": "Kahoot game flooding utility",
                "main": "flood.js",
                "author": "CPScript",
                "license": "MIT",
                "dependencies": {
                    "readline-sync": "^1.4.10",
                    "kahoot.js-updated": "^3.0.0",
                    "an-array-of-english-words": "^2.0.0",
                    "request": "^2.88.2",
                    "random-name": "^0.1.2",
                    "console-title": "^1.1.0",
                    "beepbeep": "^1.3.0"
                }
            }
            
            try:
                with open(package_json_path, 'w') as f:
                    json.dump(package_data, f, indent=2)
            except Exception as e:
                ColorOutput.warning(f"Failed to create package.json: {e}")
    
    def check_prerequisites(self):
        if not NodeJSManager.check_node_installed():
            NodeJSManager.suggest_node_installation()
            return False
        
        if not NodeJSManager.check_npm_installed():
            ColorOutput.error("npm is required but not found on your system.")
            return False
        
        if not os.path.exists(self.flood_js_path):
            ColorOutput.error(f"Flood script not found at: {self.flood_js_path}")
            return False
        
        return True
    
    def install_dependencies(self):
        # Try using package.json first (preferred method)
        try:
            ColorOutput.info("Installing dependencies from package.json...")
            result = subprocess.run(
                ["npm", "install", "--no-fund", "--no-audit"],
                cwd=self.script_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            if result.returncode == 0:
                ColorOutput.success("Successfully installed dependencies")
                return True
        except Exception as e:
            ColorOutput.warning(f"Failed to install from package.json: {e}")
        
        # Fallback to installing packages individually
        return NodeJSManager.install_node_packages()
    
    def run(self):
        PlatformManager.clear_screen()
        
        ColorOutput.info("Welcome to Kitty-Tools Kahoot Flooder - Enhanced Version")
        ColorOutput.info("===============================================")
        ColorOutput.warning("DISCLAIMER: This tool is for educational purposes only.")
        ColorOutput.warning("Using this tool may violate Kahoot's terms of service.")
        ColorOutput.warning("The authors are not responsible for any misuse of this tool.")
        ColorOutput.info("===============================================")
        
        print("\nStart?")
        print("yes | no")
        choice = input("").lower()
        
        if choice == "yes":
            time.sleep(1)
            PlatformManager.clear_screen()
            
            # Check prerequisites
            ColorOutput.info("Checking if required dependencies exist...")
            if not self.check_prerequisites():
                ColorOutput.error("Prerequisites check failed")
                input("\nPress Enter to return to the main menu...")
                return self.return_to_main_menu()
            
            # Install dependencies
            ColorOutput.info("Installing required dependencies...")
            if not self.install_dependencies():
                ColorOutput.error("Failed to install required dependencies")
                input("\nPress Enter to return to the main menu...")
                return self.return_to_main_menu()
            
            # Execute the flood script
            ColorOutput.success("All dependencies installed successfully")
            ColorOutput.info("Executing flooder...")
            time.sleep(2)
            PlatformManager.clear_screen()
            
            NodeJSManager.run_flood_script(self.flood_js_path)
            
            input("\nPress Enter to return to the main menu...")
            return self.return_to_main_menu()
        
        elif choice == "no":
            print("\nReturning to main menu...")
            time.sleep(3)
            PlatformManager.clear_screen()
            return self.return_to_main_menu()
        
        else:
            ColorOutput.error("Invalid choice")
            time.sleep(2)
            return self.run()
    
    def return_to_main_menu(self):
        try:
            main_py_path = os.path.abspath(os.path.join(self.script_dir, "..", "..", "main.py"))
            if os.path.exists(main_py_path):
                subprocess.run([sys.executable, main_py_path], check=False)
            else:
                ColorOutput.error(f"Main menu script not found at: {main_py_path}")
        except Exception as e:
            ColorOutput.error(f"Failed to return to main menu: {e}")

if __name__ == "__main__":
    try:
        manager = FloodManager()
        manager.run()
    except KeyboardInterrupt:
        ColorOutput.warning("\nOperation cancelled by user")
    except Exception as e:
        ColorOutput.error(f"Unexpected error: {e}")
