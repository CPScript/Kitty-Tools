# THE CONTENT IN THIS FILE AND ITS SIMPLICITY IS UGLY AND MAKES MY MIND HURT

import time
import os
import platform 
import subprocess
import json
from os import system
from subprocess import call

def clear():
    system = platform.system().lower()

    if system == 'windows':
        _ = os.system('cls')
    elif system == 'linux' or system == 'darwin':
        _ = os.system('clear')
    elif system == 'android':
        _ = subprocess.run(['termux-exec', 'sh', '-c', 'clear'], check=False)
        print("Please use LITE!")
        exit()
    else:
        print(f"Unsupported platform, please use Kitty-Tools LITE '{system}'")
        print(f"For more info go to https://github.com/CPScript/Kitty-Tools/extra.md")

def check_node_installed():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, None

def check_npm_installed():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, None

def install_nodejs_guide():
    """Show Node.js installation guide"""
    system_name = platform.system().lower()
    
    print("\nNode.js is required but not found on your system.")
    print("Please install Node.js using the following instructions:")
    print()
    
    if system_name == "windows":
        print("Windows Installation:")
        print("1. Go to https://nodejs.org/")
        print("2. Download the Windows Installer (.msi)")
        print("3. Run the installer and follow the installation wizard")
        print("4. Make sure to check 'Add to PATH' during installation")
        print("5. Restart your computer after installation")
        print()
        print("Alternative - Using Chocolatey:")
        print("choco install nodejs")
        
    elif system_name == "darwin":  # macOS
        print("macOS Installation:")
        print("Option 1 - Using Homebrew (recommended):")
        print("  brew install node")
        print()
        print("Option 2 - Official installer:")
        print("  1. Go to https://nodejs.org/")
        print("  2. Download the macOS Installer (.pkg)")
        print("  3. Run the installer")
        
    elif system_name == "linux":
        print("Linux Installation:")
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
        
    else:
        print("For other platforms, please visit: https://nodejs.org/")
    
    print()
    print("After installation, restart your terminal and run this script again.")

def create_package_json():
    """Create package.json file for dependencies"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    package_json_path = os.path.join(script_dir, 'package.json')
    
    package_data = {
        "name": "kitty-tools-kahoot-flooder",
        "version": "1.4.0",
        "description": "Kahoot game flooding utility",
        "main": "flood.js",
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
            "node": ">=12.0.0"
        }
    }
    
    try:
        with open(package_json_path, 'w') as f:
            json.dump(package_data, f, indent=2)
        print("Created package.json file")
        return True
    except Exception as e:
        print(f"Failed to create package.json: {e}")
        return False

def install_node_packages():
    """Install required Node.js packages"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Installing Node.js dependencies...")
    
    # Create package.json first
    if not create_package_json():
        return False
    
    try:
        # Try installing from package.json
        result = subprocess.run(
            ['npm', 'install', '--no-fund', '--no-audit'],
            cwd=script_dir,
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.returncode == 0:
            print("Successfully installed all Node.js packages")
            return True
        else:
            print(f"npm install failed: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Package installation failed: {e}")
        print("Error output:", e.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error during package installation: {e}")
        return False

def verify_installation():
    """Verify that Node.js modules are installed correctly"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    test_script = '''
try {
    require('readline-sync');
    require('kahoot.js-updated');
    require('an-array-of-english-words');
    require('request');
    require('random-name');
    require('console-title');
    require('beepbeep');
    console.log('VERIFICATION_SUCCESS');
} catch (error) {
    console.log('VERIFICATION_FAILED:', error.message);
    process.exit(1);
}
'''
    
    test_file = os.path.join(script_dir, 'test_modules.js')
    
    try:
        with open(test_file, 'w') as f:
            f.write(test_script)
        
        result = subprocess.run(['node', test_file], capture_output=True, text=True, cwd=script_dir)
        
        if 'VERIFICATION_SUCCESS' in result.stdout:
            print("All modules verified successfully")
            os.remove(test_file)
            return True
        else:
            print(f"Module verification failed: {result.stdout}")
            os.remove(test_file)
            return False
            
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

def run_flood_script():
    """Run the flood.js script"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    flood_js_path = os.path.join(script_dir, 'flood.js')
    
    if not os.path.exists(flood_js_path):
        print(f"Error: flood.js not found at {flood_js_path}")
        return False
    
    try:
        print("Starting Kahoot flooder...")
        subprocess.run(['node', flood_js_path], cwd=script_dir, check=False)
        return True
    except KeyboardInterrupt:
        print("\nFlooder stopped by user")
        return True
    except Exception as e:
        print(f"Error running flooder: {e}")
        return False

clear() # call check

print("Start???")
print("yes | no")
choice = input("").lower()

if choice == "yes":
    time.sleep(1)
    clear()
    
    # Check if Node.js is installed
    node_installed, node_version = check_node_installed()
    npm_installed, npm_version = check_npm_installed()
    
    if not node_installed:
        print("Node.js is not installed!")
        install_nodejs_guide()
        input("\nPress Enter to return to main menu...")
        clear()
        call(["python", "../../main.py"])
        exit()
    
    if not npm_installed:
        print("npm is not installed!")
        print("npm is usually installed with Node.js. Please reinstall Node.js.")
        input("\nPress Enter to return to main menu...")
        clear()
        call(["python", "../../main.py"])
        exit()
    
    print(f"Node.js found: {node_version}")
    print(f"npm found: {npm_version}")
    
    # Check if node exists
    print("Checking if Node.js is accessible...")
    try:
        import node # does node exist
    except ModuleNotFoundError:
        print("Attempting to install node Python package...")
        time.sleep(2)
        os.system("pip install node") # installation
        clear()
    
    # Install Node.js packages
    if not install_node_packages():
        print("Failed to install required Node.js packages!")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Try running as administrator/sudo")
        print("3. Clear npm cache: npm cache clean --force")
        input("\nPress Enter to return to main menu...")
        clear()
        call(["python", "../../main.py"])
        exit()
    
    # Verify installation
    if not verify_installation():
        print("Warning: Some modules failed verification")
        print("The flooder might still work, but some features may be limited")
        
        proceed = input("Continue anyway? (y/n): ").lower()
        if proceed != 'y':
            clear()
            call(["python", "../../main.py"])
            exit()
    
    clear()   
    print("Executing!")
    time.sleep(2)
    clear()
    
    # Run the flooder
    if not run_flood_script():
        print("Flooder execution failed!")
        input("\nPress Enter to return to main menu...")
    
    clear()
    call(["python", "../../main.py"])
    
if choice == "no":
    print("\nRe-Running main menu file!")
    time.sleep(3)
    clear()
    call(["python", "../../main.py"])
