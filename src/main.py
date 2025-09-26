#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import time

class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    
    @staticmethod
    def print(text, color):
        print(f"{color}{text}{Colors.RESET}")

def clear_screen():
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('clear')

def run_command_safe(command, cwd=None, timeout=30):
    is_windows = platform.system().lower() == "windows"
    
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=is_windows,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def install_essential_packages():
    Colors.print("Installing essential packages for flood.js...", Colors.CYAN)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    essential_packages = [
        "readline-sync",
        "request", 
        "random-name",
        "an-array-of-english-words",
        "console-title",
        "beepbeep"
    ]
    
    kahoot_packages = [
        "kahoot.js-latest",
        "kahoot.js-api",
        "node-kahoot"
    ]
    
    installed_count = 0
    
    for package in essential_packages:
        Colors.print(f"Installing {package}...", Colors.YELLOW)
        success, stdout, stderr = run_command_safe(
            ["npm", "install", package, "--no-fund", "--no-audit"],
            cwd=project_root
        )
        
        if success:
            Colors.print(f"Successfully installed {package}", Colors.GREEN)
            installed_count += 1
        else:
            Colors.print(f"Failed to install {package}", Colors.RED)
    
    kahoot_installed = False
    for package in kahoot_packages:
        if kahoot_installed:
            break
            
        Colors.print(f"Trying {package}...", Colors.YELLOW)
        success, stdout, stderr = run_command_safe(
            ["npm", "install", package, "--no-fund", "--no-audit"],
            cwd=project_root
        )
        
        if success:
            Colors.print(f"Successfully installed {package}", Colors.GREEN)
            installed_count += 1
            kahoot_installed = True
        else:
            Colors.print(f"Failed to install {package}", Colors.RED)
    
    return installed_count > 0

def try_run_flood_js():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    flood_js_path = os.path.join(project_root, "Kitty", "Flood", "flood.js")
    
    if not os.path.exists(flood_js_path):
        Colors.print(f"ERROR: flood.js not found at {flood_js_path}", Colors.RED)
        return False
    
    Colors.print(f"Found flood.js at: {flood_js_path}", Colors.GREEN)
    Colors.print("Starting Kahoot Flooder...", Colors.CYAN)
    print("=" * 50)
    
    try:
        is_windows = platform.system().lower() == "windows"
        
        process = subprocess.Popen(
            ["node", flood_js_path],
            cwd=os.path.dirname(flood_js_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            shell=is_windows
        )
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        rc = process.poll()
        return rc == 0
        
    except FileNotFoundError:
        Colors.print("ERROR: Node.js not found!", Colors.RED)
        Colors.print("Please install Node.js from https://nodejs.org/", Colors.YELLOW)
        return False
    except KeyboardInterrupt:
        Colors.print("\\nFlooder stopped by user", Colors.YELLOW)
        return True
    except Exception as e:
        Colors.print(f"ERROR: {e}", Colors.RED)
        return False

def main():
    clear_screen()
    
    Colors.print("Kitty-Tools Flooder Launcher", Colors.CYAN)
    print("=" * 40)
    Colors.print("This script will run the Kahoot flooder from Kitty/Flood/flood.js", Colors.BLUE)
    print("=" * 40)
    
    node_available, _, _ = run_command_safe(["node", "--version"])
    if not node_available:
        Colors.print("ERROR: Node.js is not installed or not in PATH", Colors.RED)
        Colors.print("Please install Node.js from https://nodejs.org/", Colors.YELLOW)
        input("Press Enter to exit...")
        return
    
    npm_available, _, _ = run_command_safe(["npm", "--version"])
    if not npm_available:
        Colors.print("ERROR: npm is not available", Colors.RED)
        input("Press Enter to exit...")
        return
    
    Colors.print("Node.js and npm are available", Colors.GREEN)
    print()
    
    Colors.print("Attempting to run flood.js...", Colors.CYAN)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    test_modules = [
        "readline-sync",
        "kahoot.js-latest",
        "an-array-of-english-words",
        "request",
        "random-name",
        "console-title",
        "beepbeep"
    ]
    
    missing_modules = []
    for module in test_modules:
        test_success, _, _ = run_command_safe(
            ["node", "-e", f"require('{module}'); console.log('{module} OK');"],
            cwd=project_root,
            timeout=5
        )
        if not test_success:
            missing_modules.append(module)
    
    if not missing_modules:
        Colors.print("All required modules are available!", Colors.GREEN)
        print()
        if try_run_flood_js():
            Colors.print("Flooder completed successfully!", Colors.GREEN)
        else:
            Colors.print("Flooder encountered an error", Colors.YELLOW)
    else:
        Colors.print(f"Missing modules: {', '.join(missing_modules)}", Colors.YELLOW)
        Colors.print("Installing required packages...", Colors.CYAN)
        print()
        
        if install_essential_packages():
            Colors.print("Package installation completed!", Colors.GREEN)
            print()
            Colors.print("Trying to run flood.js again...", Colors.CYAN)
            print()
            
            if try_run_flood_js():
                Colors.print("Flooder completed successfully!", Colors.GREEN)
            else:
                Colors.print("Flooder still failed to run", Colors.RED)
                print()
                Colors.print("Manual troubleshooting:", Colors.YELLOW)
                print("1. Try running: npm install kahoot.js-latest")
                print("2. Try running: npm install readline-sync")
                print("3. Try running: node Kitty/Flood/flood.js")
        else:
            Colors.print("Failed to install required packages", Colors.RED)
            Colors.print("Please try manually installing with:", Colors.YELLOW)
            print("  npm install kahoot.js-latest")
            print("  npm install readline-sync")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Colors.print("\\nExiting...", Colors.YELLOW)
    except Exception as e:
        Colors.print(f"Unexpected error: {e}", Colors.RED)
        input("Press Enter to exit...")
