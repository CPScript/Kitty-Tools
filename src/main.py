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
            return result.returncode == 0, result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return False, None
    
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
            return result.returncode == 0, result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return False, None
    
    @staticmethod
    def install_nodejs_guide():
        """Show Node.js installation guide"""
        platform_name = PlatformManager.detect_platform()
        
        ColorOutput.error("Node.js is required but not found on your system.")
        ColorOutput.info("Please install Node.js using the following instructions:")
        print()
        
        if platform_name == "windows":
            ColorOutput.info("Windows Installation:")
            print("1. Download the installer from https://nodejs.org/")
            print("2. Run the installer and follow the installation wizard")
            print("3. Make sure to check 'Add to PATH' during installation")
            print("4. Restart your computer after installation")
            print()
            ColorOutput.info("Alternative - Using Chocolatey:")
            print("choco install nodejs")
            
        elif platform_name == "macos":
            ColorOutput.info("macOS Installation:")
            print("Option 1 - Using Homebrew (recommended):")
            print("  brew install node")
            print()
            print("Option 2 - Official installer:")
            print("  1. Download from https://nodejs.org/")
            print("  2. Run the .pkg installer")
            print()
            print("Option 3 - Using MacPorts:")
            print("  sudo port install nodejs18")
            
        elif platform_name == "linux":
            ColorOutput.info("Linux Installation:")
            print("Ubuntu/Debian:")
            print("  sudo apt update && sudo apt install nodejs npm")
            print()
            print("Fedora:")
            print("  sudo dnf install nodejs npm")
            print()
            print("Arch Linux:")
            print("  sudo pacman -S nodejs npm")
            print()
            print("CentOS/RHEL:")
            print("  sudo yum install nodejs npm")
            print()
            print("Using Node Version Manager (recommended):")
            print("  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash")
            print("  nvm install node")
            
        elif platform_name == "android":
            ColorOutput.info("Android (Termux) Installation:")
            print("pkg install nodejs")
            
        else:
            ColorOutput.info("For other platforms, please visit: https://nodejs.org/")
        
        print()
        ColorOutput.warning("After installation, restart your terminal and run this script again.")
    
    @staticmethod
    def create_package_json(script_dir):
        """Create package.json file"""
        package_json_path = os.path.join(script_dir, 'package.json')
        
        package_data = {
            "name": "kitty-tools-kahoot-flooder",
            "version": "2.0.0",
            "description": "Enhanced Kahoot game flooding utility",
            "main": "flood.js",
            "scripts": {
                "start": "node flood.js",
                "install-deps": "npm install"
            },
            "keywords": ["kahoot", "flooder", "educational", "testing"],
            "author": "CPScript",
            "license": "MIT",
            "dependencies": {
                "readline-sync": "^1.4.10",
                "kahoot.js-updated": "^3.1.3",
                "an-array-of-english-words": "^2.0.0", 
                "request": "^2.88.2",
                "random-name": "^0.1.2",
                "console-title": "^1.1.0",
                "beepbeep": "^1.3.0"
            },
            "engines": {
                "node": ">=12.0.0",
                "npm": ">=6.0.0"
            }
        }
        
        try:
            with open(package_json_path, 'w', encoding='utf-8') as f:
                json.dump(package_data, f, indent=2, ensure_ascii=False)
            ColorOutput.success(f"Created package.json")
            return True
        except Exception as e:
            ColorOutput.error(f"Failed to create package.json: {e}")
            return False
    
    @staticmethod
    def install_node_packages(script_dir):
        """Install required Node.js packages"""
        ColorOutput.info("Installing required Node.js packages...")
        
        # Create package.json first
        if not NodeJSManager.create_package_json(script_dir):
            return False
        
        try:
            # Try installing from package.json first
            result = subprocess.run(
                ["npm", "install", "--no-fund", "--no-audit"],
                cwd=script_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            ColorOutput.success("Successfully installed all Node.js packages")
            return True
            
        except subprocess.CalledProcessError as e:
            ColorOutput.warning("Package installation from package.json failed, trying individual installation...")
            
            # Try installing packages individually
            success_count = 0
            for package in NodeJSManager.REQUIRED_PACKAGES:
                try:
                    ColorOutput.info(f"Installing {package}...")
                    subprocess.run(
                        ["npm", "install", package, "--no-fund", "--no-audit"],
                        cwd=script_dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True
                    )
                    ColorOutput.success(f"Installed {package}")
                    success_count += 1
                except subprocess.CalledProcessError:
                    ColorOutput.error(f"Failed to install {package}")
            
            if success_count == len(NodeJSManager.REQUIRED_PACKAGES):
                ColorOutput.success("All packages installed successfully")
                return True
            elif success_count > 0:
                ColorOutput.warning(f"{success_count}/{len(NodeJSManager.REQUIRED_PACKAGES)} packages installed")
                return True
            else:
                ColorOutput.error("No packages were installed successfully")
                return False
        
        except Exception as e:
            ColorOutput.error(f"Unexpected error during package installation: {e}")
            return False
    
    @staticmethod
    def verify_installation(script_dir):
        """Verify that all required modules can be loaded"""
        ColorOutput.info("Verifying Node.js module installation...")
        
        test_script = '''
const requiredModules = [
    'readline-sync',
    'kahoot.js-updated', 
    'an-array-of-english-words',
    'request',
    'random-name',
    'console-title',
    'beepbeep'
];

let success = 0;
let failed = 0;

for (const moduleName of requiredModules) {
    try {
        require(moduleName);
        console.log(`SUCCESS: ${moduleName}`);
        success++;
    } catch (error) {
        console.log(`FAILED: ${moduleName} - ${error.message}`);
        failed++;
    }
}

console.log(`SUMMARY: ${success} success, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
'''
        
        test_file = os.path.join(script_dir, 'test_modules.js')
        
        try:
            with open(test_file, 'w') as f:
                f.write(test_script)
            
            result = subprocess.run(
                ['node', test_file],
                cwd=script_dir,
                capture_output=True,
                text=True
            )
            
            # Parse output
            for line in result.stdout.split('\n'):
                if line.startswith('SUCCESS:'):
                    ColorOutput.success(f"Module verified: {line.split(': ')[1]}")
                elif line.startswith('FAILED:'):
                    ColorOutput.error(f"Module failed: {line.split(': ')[1]}")
                elif line.startswith('SUMMARY:'):
                    print(line)
            
            # Clean up test file
            os.remove(test_file)
            
            return result.returncode == 0
            
        except Exception as e:
            ColorOutput.error(f"Verification failed: {e}")
            return False
    
    @staticmethod
    def run_flood_script(script_path):
        if not os.path.exists(script_path):
            ColorOutput.error(f"Flood script not found at: {script_path}")
            return False
        
        try:
            ColorOutput.info("Starting Kahoot flooder...")
            
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

class NodeJSSetup:
    """Node.js setup and verification system"""
    
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
    def run_setup(self):
        """Run complete Node.js setup"""
        ColorOutput.info("Kitty-Tools Node.js Setup")
        print("=" * 50)
        
        # Check Node.js installation
        node_installed, node_version = NodeJSManager.check_node_installed()
        npm_installed, npm_version = NodeJSManager.check_npm_installed()
        
        if not node_installed:
            ColorOutput.error("Node.js not found")
            NodeJSManager.install_nodejs_guide()
            return False
        else:
            ColorOutput.success(f"Node.js found: {node_version}")
        
        if not npm_installed:
            ColorOutput.error("NPM not found")
            ColorOutput.info("NPM is usually installed with Node.js. Please reinstall Node.js.")
            return False
        else:
            ColorOutput.success(f"NPM found: {npm_version}")
        
        # Install packages
        if not NodeJSManager.install_node_packages(self.script_dir):
            ColorOutput.error("Failed to install required packages")
            return False
        
        # Verify installation
        if not NodeJSManager.verify_installation(self.script_dir):
            ColorOutput.warning("Some modules failed verification, but the flooder might still work")
        else:
            ColorOutput.success("All modules verified successfully")
        
        return True

class FloodManager:    
    def __init__(self):
        """Initialize the flood manager."""
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.flood_js_path = os.path.join(self.script_dir, "flood.js")
        self.setup = NodeJSSetup()
        
    def verify_nodejs_ready(self):
        """Verify Node.js and dependencies are ready"""
        # Check if Node.js is installed
        node_installed, _ = NodeJSManager.check_node_installed()
        npm_installed, _ = NodeJSManager.check_npm_installed()
        
        if not node_installed or not npm_installed:
            ColorOutput.warning("Node.js or NPM not found. Running setup...")
            return self.setup.run_setup()
        
        # Check if flood.js exists
        if not os.path.exists(self.flood_js_path):
            ColorOutput.error(f"Flood script not found at: {self.flood_js_path}")
            return False
        
        # Check if node_modules directory exists
        node_modules_path = os.path.join(self.script_dir, "node_modules")
        if not os.path.exists(node_modules_path):
            ColorOutput.warning("Node modules not found. Installing dependencies...")
            return NodeJSManager.install_node_packages(self.script_dir)
        
        # Quick verification of key modules
        try:
            test_result = subprocess.run(
                ["node", "-e", "require('kahoot.js-updated'); console.log('OK');"],
                cwd=self.script_dir,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if test_result.returncode != 0:
                ColorOutput.warning("Dependencies verification failed. Reinstalling...")
                return NodeJSManager.install_node_packages(self.script_dir)
            
        except Exception:
            ColorOutput.warning("Could not verify dependencies. Reinstalling...")
            return NodeJSManager.install_node_packages(self.script_dir)
        
        return True
    
    def run(self):
        PlatformManager.clear_screen()
        
        ColorOutput.info("Kitty-Tools Kahoot Flooder - Enhanced Version")
        print("=" * 50)
        ColorOutput.warning("DISCLAIMER: This tool is for educational purposes only.")
        ColorOutput.warning("Using this tool may violate Kahoot's terms of service.")
        ColorOutput.warning("The authors are not responsible for any misuse of this tool.")
        print("=" * 50)
        
        print("\nStart flooder?")
        print("yes | no")
        choice = input(">> ").lower()
        
        if choice == "yes":
            time.sleep(1)
            PlatformManager.clear_screen()
            
            # Verify Node.js is ready
            ColorOutput.info("Verifying Node.js installation and dependencies...")
            if not self.verify_nodejs_ready():
                ColorOutput.error("Node.js setup failed. Cannot run flooder.")
                input("\nPress Enter to return to the main menu...")
                return self.return_to_main_menu()
            
            # Execute the flood script
            ColorOutput.success("Node.js setup verified. Starting flooder...")
            time.sleep(2)
            PlatformManager.clear_screen()
            
            NodeJSManager.run_flood_script(self.flood_js_path)
            
            input("\nPress Enter to return to the main menu...")
            return self.return_to_main_menu()
        
        elif choice == "no":
            print("\nReturning to main menu...")
            time.sleep(2)
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
