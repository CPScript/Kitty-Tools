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
    def diagnose_npm_issues():
        """Diagnose and fix common npm issues"""
        ColorOutput.info("Diagnosing npm configuration...")
        
        # Check npm configuration
        try:
            config_result = subprocess.run(
                ["npm", "config", "list"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if config_result.returncode != 0:
                ColorOutput.error("npm configuration is corrupted")
                return False
            
            # Check registry
            registry_result = subprocess.run(
                ["npm", "config", "get", "registry"],
                capture_output=True,
                text=True,
                check=False
            )
            
            registry = registry_result.stdout.strip()
            ColorOutput.info(f"Current npm registry: {registry}")
            
            # Fix registry if needed
            if "registry.npmjs.org" not in registry:
                ColorOutput.warning("Fixing npm registry...")
                subprocess.run(
                    ["npm", "config", "set", "registry", "https://registry.npmjs.org/"],
                    check=False
                )
            
            # Test connectivity to npm registry
            try:
                import urllib.request
                with urllib.request.urlopen("https://registry.npmjs.org/", timeout=10) as response:
                    if response.status == 200:
                        ColorOutput.success("npm registry is accessible")
                    else:
                        ColorOutput.error(f"npm registry returned status: {response.status}")
                        return False
            except Exception as e:
                ColorOutput.error(f"Cannot reach npm registry: {e}")
                ColorOutput.warning("You may be behind a firewall or have network issues")
                return False
            
            return True
            
        except Exception as e:
            ColorOutput.error(f"npm diagnosis failed: {e}")
            return False
    
    @staticmethod
    def fix_npm_permissions():
        """Fix npm permissions issues"""
        platform_name = PlatformManager.detect_platform()
        
        if platform_name in ["linux", "macos"]:
            ColorOutput.info("Checking npm permissions...")
            
            try:
                # Get npm prefix
                prefix_result = subprocess.run(
                    ["npm", "config", "get", "prefix"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                npm_prefix = prefix_result.stdout.strip()
                ColorOutput.info(f"npm prefix: {npm_prefix}")
                
                # Check if we need to fix global permissions
                if "/usr/local" in npm_prefix or "/usr" in npm_prefix:
                    ColorOutput.warning("npm is using system directories")
                    ColorOutput.info("Setting up user-local npm directory...")
                    
                    # Set up local npm directory
                    home_dir = os.path.expanduser("~")
                    npm_dir = os.path.join(home_dir, ".npm-global")
                    
                    if not os.path.exists(npm_dir):
                        os.makedirs(npm_dir)
                    
                    # Configure npm to use local directory
                    subprocess.run(
                        ["npm", "config", "set", "prefix", npm_dir],
                        check=False
                    )
                    
                    ColorOutput.success("Configured npm to use local directory")
                    
                    # Add to PATH suggestion
                    ColorOutput.info(f"Add this to your shell profile (~/.bashrc or ~/.zshrc):")
                    ColorOutput.info(f"export PATH={npm_dir}/bin:$PATH")
                
                return True
                
            except Exception as e:
                ColorOutput.warning(f"Could not fix npm permissions: {e}")
                return False
        
        return True
    
    @staticmethod
    def create_npmrc(script_dir):
        """Create .npmrc file with safe configurations"""
        npmrc_path = os.path.join(script_dir, ".npmrc")
        
        npmrc_content = """registry=https://registry.npmjs.org/
fund=false
audit=false
save-exact=true
engine-strict=false
"""
        
        try:
            with open(npmrc_path, 'w') as f:
                f.write(npmrc_content)
            ColorOutput.success("Created .npmrc configuration file")
            return True
        except Exception as e:
            ColorOutput.warning(f"Could not create .npmrc: {e}")
            return False
    
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
                "install-deps": "npm install",
                "clean": "rm -rf node_modules package-lock.json"
            },
            "keywords": ["kahoot", "flooder", "educational", "testing"],
            "author": "CPScript",
            "license": "MIT",
            "dependencies": {
                "readline-sync": "^1.4.10",
                "kahoot.js-updated": "3.1.2",
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
        
        # Clean install to fix corrupted packages
        ColorOutput.info("Cleaning previous installations...")
        node_modules_path = os.path.join(script_dir, 'node_modules')
        package_lock_path = os.path.join(script_dir, 'package-lock.json')
        
        # Remove node_modules and package-lock.json if they exist
        try:
            if os.path.exists(node_modules_path):
                import shutil
                shutil.rmtree(node_modules_path)
                ColorOutput.success("Removed old node_modules directory")
            
            if os.path.exists(package_lock_path):
                os.remove(package_lock_path)
                ColorOutput.success("Removed old package-lock.json")
        except Exception as e:
            ColorOutput.warning(f"Could not clean old files: {e}")
        
        try:
            # Clear npm cache
            ColorOutput.info("Clearing npm cache...")
            subprocess.run(
                ["npm", "cache", "clean", "--force"],
                cwd=script_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False
            )
            
            # Try installing from package.json first
            ColorOutput.info("Installing packages from package.json...")
            result = subprocess.run(
                ["npm", "install", "--no-fund", "--no-audit", "--force"],
                cwd=script_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            ColorOutput.success("Successfully installed all Node.js packages")
            return True
            
        except subprocess.CalledProcessError as e:
            ColorOutput.warning("Package installation from package.json failed, trying alternative approach...")
            
            # Try installing packages individually with specific versions
            packages_with_versions = [
                "readline-sync@1.4.10",
                "kahoot.js-updated@3.1.2", 
                "an-array-of-english-words@2.0.0",
                "request@2.88.2",
                "random-name@0.1.2",
                "console-title@1.1.0",
                "beepbeep@1.3.0"
            ]
            
            success_count = 0
            for package in packages_with_versions:
                try:
                    ColorOutput.info(f"Installing {package}...")
                    subprocess.run(
                        ["npm", "install", package, "--no-fund", "--no-audit", "--force"],
                        cwd=script_dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True
                    )
                    ColorOutput.success(f"Installed {package}")
                    success_count += 1
                except subprocess.CalledProcessError as pkg_error:
                    ColorOutput.error(f"Failed to install {package}")
                    
                    # Special handling for kahoot.js-updated
                    if "kahoot.js-updated" in package:
                        ColorOutput.info("Trying alternative Kahoot package...")
                        try:
                            subprocess.run(
                                ["npm", "install", "kahoot.js@3.0.4", "--no-fund", "--no-audit", "--force"],
                                cwd=script_dir,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True
                            )
                            ColorOutput.success("Installed alternative kahoot.js package")
                            success_count += 1
                        except subprocess.CalledProcessError:
                            ColorOutput.error("Failed to install alternative Kahoot package")
            
            if success_count >= 6:  # Allow one failure
                ColorOutput.success("Most packages installed successfully")
                return True
            else:
                ColorOutput.error("Too many packages failed to install")
                return False
        
        except Exception as e:
            ColorOutput.error(f"Unexpected error during package installation: {e}")
            return False
    
    @staticmethod
    def verify_installation(script_dir):
        """Verify that all required modules can be loaded"""
        ColorOutput.info("Verifying Node.js module installation...")
        
        test_script = '''
const modules = [
    'readline-sync',
    'an-array-of-english-words',
    'request',
    'random-name',
    'console-title',
    'beepbeep'
];

// Special handling for Kahoot module with fallback
const kahootModules = ['kahoot.js-updated', 'kahoot.js'];

let success = 0;
let failed = 0;

// Test regular modules
for (const moduleName of modules) {
    try {
        require(moduleName);
        console.log(`SUCCESS: ${moduleName}`);
        success++;
    } catch (error) {
        console.log(`FAILED: ${moduleName} - ${error.message}`);
        failed++;
    }
}

// Test Kahoot module with fallback
let kahootSuccess = false;
for (const kahootModule of kahootModules) {
    try {
        require(kahootModule);
        console.log(`SUCCESS: ${kahootModule}`);
        kahootSuccess = true;
        success++;
        break;
    } catch (error) {
        console.log(`FAILED: ${kahootModule} - ${error.message}`);
    }
}

if (!kahootSuccess) {
    console.log('FAILED: No working Kahoot module found');
    failed++;
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
            if not self.setup.run_setup():
                return False
        
        # Check if flood.js exists
        if not os.path.exists(self.flood_js_path):
            ColorOutput.error(f"Flood script not found at: {self.flood_js_path}")
            return False
        
        # Check if node_modules directory exists
        node_modules_path = os.path.join(self.script_dir, "node_modules")
        if not os.path.exists(node_modules_path):
            ColorOutput.warning("Node modules not found. Installing dependencies...")
            if not NodeJSManager.install_node_packages(self.script_dir):
                ColorOutput.error("Failed to install dependencies.")
                self.offer_minimal_mode()
                return False
        
        # Quick verification of key modules
        try:
            test_result = subprocess.run(
                ["node", "-e", "require('readline-sync'); console.log('OK');"],
                cwd=self.script_dir,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if test_result.returncode != 0:
                ColorOutput.warning("Dependencies verification failed. Reinstalling...")
                if not NodeJSManager.install_node_packages(self.script_dir):
                    ColorOutput.error("Failed to install dependencies.")
                    self.offer_minimal_mode()
                    return False
            
        except Exception:
            ColorOutput.warning("Could not verify dependencies. Reinstalling...")
            if not NodeJSManager.install_node_packages(self.script_dir):
                ColorOutput.error("Failed to install dependencies.")
                self.offer_minimal_mode()
                return False
        
        return True
    
    def offer_minimal_mode(self):
        """Offer minimal mode when full installation fails"""
        ColorOutput.warning("Full installation failed, but we can try minimal mode.")
        print()
        print("Minimal mode includes:")
        print("- Basic flooding functionality")
        print("- Fewer dependencies required")
        print("- Limited features (no fancy names, simple UI)")
        print()
        
        choice = input("Try minimal mode? (y/n): ").lower().strip()
        if choice == 'y':
            self.create_minimal_flooder()
    
    def create_minimal_flooder(self):
        """Create minimal flooder script"""
        ColorOutput.info("Creating minimal flooder...")
        
        minimal_script_path = os.path.join(self.script_dir, "minimal_flood.js")
        
        # The minimal flood script content
        minimal_script = '''// Minimal Kahoot Flooder - Fallback Version
console.log("Starting Minimal Kahoot Flooder...");

let readline = null;
let Kahoot = null;

try {
    readline = require('readline-sync');
    console.log("✓ readline-sync loaded");
} catch (error) {
    console.error("✗ readline-sync not available");
    console.log("Please install: npm install readline-sync@1.4.10");
    process.exit(1);
}

const kahootModules = ['kahoot.js', 'kahoot.js-updated'];
for (const moduleName of kahootModules) {
    try {
        Kahoot = require(moduleName);
        console.log(`✓ ${moduleName} loaded`);
        break;
    } catch (error) {
        console.log(`✗ ${moduleName} not available`);
    }
}

if (!Kahoot) {
    console.error("No Kahoot module found!");
    console.log("Please install: npm install kahoot.js@3.0.4");
    process.exit(1);
}

function getRandomName() {
    const names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Echo'];
    return names[Math.floor(Math.random() * names.length)] + Math.floor(Math.random() * 1000);
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

console.clear();
console.log("====================================");
console.log("Kitty Tools - Minimal Kahoot Flooder");
console.log("====================================");

const pin = readline.question('Enter game PIN: ');
const bots = parseInt(readline.question('Enter number of bots (1-20): ')) || 10;

console.log(`\\nStarting ${bots} bots for game ${pin}...`);

let connected = 0;
let failed = 0;

function createBot(id) {
    const name = getRandomName();
    const client = new Kahoot();
    
    client.join(pin, name).then(() => {
        connected++;
        console.log(`[${id}] ${name} connected (${connected}/${bots})`);
    }).catch(err => {
        failed++;
        console.log(`[${id}] ${name} failed: ${err.description || err.message}`);
    });
    
    client.on("QuestionReady", question => {
        setTimeout(() => {
            try {
                client.answer(getRandomInt(0, 3));
            } catch (error) {
                // Ignore answer errors
            }
        }, getRandomInt(1000, 3000));
    });
    
    client.on("Disconnect", reason => {
        console.log(`[${id}] ${name} disconnected: ${reason}`);
    });
}

for (let i = 0; i < bots; i++) {
    setTimeout(() => createBot(i), i * 500);
}

process.on('SIGINT', () => {
    console.log('\\nStopped by user');
    process.exit(0);
});

console.log("\\nPress Ctrl+C to stop");
'''
        
        try:
            with open(minimal_script_path, 'w') as f:
                f.write(minimal_script)
            
            ColorOutput.success("Created minimal flooder script")
            
            # Try to install minimal dependencies
            ColorOutput.info("Installing minimal dependencies...")
            minimal_packages = ["readline-sync@1.4.10", "kahoot.js@3.0.4"]
            
            for package in minimal_packages:
                try:
                    subprocess.run(
                        ["npm", "install", package, "--force"],
                        cwd=self.script_dir,
                        check=True,
                        capture_output=True
                    )
                    ColorOutput.success(f"Installed {package}")
                except subprocess.CalledProcessError:
                    ColorOutput.warning(f"Failed to install {package}")
            
            # Try to run minimal flooder
            try:
                ColorOutput.info("Starting minimal flooder...")
                subprocess.run(["node", minimal_script_path], cwd=self.script_dir)
            except Exception as e:
                ColorOutput.error(f"Failed to run minimal flooder: {e}")
                
        except Exception as e:
            ColorOutput.error(f"Failed to create minimal flooder: {e}")
    
    def run(self):
        PlatformManager.clear_screen()
        
        ColorOutput.info("Kitty-Tools Kahoot Flooder - Enhanced Version")
        print("=" * 50)
        ColorOutput.warning("DISCLAIMER: This tool is for educational purposes only.")
        ColorOutput.warning("Using this tool may violate Kahoot's terms of service.")
        ColorOutput.warning("The authors are not responsible for any misuse of this tool.")
        print("=" * 50)
        
        print("\nStart flooder?")
        print("yes | no | diagnose")
        choice = input(">> ").lower()
        
        if choice == "diagnose":
            self.run_diagnostics()
            input("\nPress Enter to continue...")
            return self.run()
        
        elif choice == "yes":
            time.sleep(1)
            PlatformManager.clear_screen()
            
            # Verify Node.js is ready
            ColorOutput.info("Verifying Node.js installation and dependencies...")
            if not self.verify_nodejs_ready():
                ColorOutput.error("Node.js setup failed. Cannot run flooder.")
                print("\nTroubleshooting options:")
                print("1. Run this script again and choose 'diagnose'")
                print("2. Try the manual setup instructions below")
                print("3. Use the standard version instead (Kitty/Flood/)")
                print()
                self.show_manual_setup_instructions()
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
    
    def run_diagnostics(self):
        """Run comprehensive diagnostics"""
        ColorOutput.info("Running Node.js and npm diagnostics...")
        print("=" * 50)
        
        # Check Node.js
        node_installed, node_version = NodeJSManager.check_node_installed()
        if node_installed:
            ColorOutput.success(f"Node.js: {node_version}")
        else:
            ColorOutput.error("Node.js: Not found")
        
        # Check npm
        npm_installed, npm_version = NodeJSManager.check_npm_installed()
        if npm_installed:
            ColorOutput.success(f"npm: {npm_version}")
        else:
            ColorOutput.error("npm: Not found")
        
        if not node_installed or not npm_installed:
            return
        
        # Check npm configuration
        try:
            registry_result = subprocess.run(
                ["npm", "config", "get", "registry"],
                capture_output=True,
                text=True,
                check=False
            )
            registry = registry_result.stdout.strip()
            ColorOutput.info(f"npm registry: {registry}")
            
            # Test registry connectivity
            import urllib.request
            try:
                with urllib.request.urlopen("https://registry.npmjs.org/", timeout=10) as response:
                    if response.status == 200:
                        ColorOutput.success("npm registry: Accessible")
                    else:
                        ColorOutput.error(f"npm registry: HTTP {response.status}")
            except Exception as e:
                ColorOutput.error(f"npm registry: Not accessible ({e})")
            
            # Check npm permissions
            try:
                test_result = subprocess.run(
                    ["npm", "list", "-g", "--depth=0"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if test_result.returncode == 0:
                    ColorOutput.success("npm permissions: OK")
                else:
                    ColorOutput.warning("npm permissions: May have issues")
            except Exception:
                ColorOutput.warning("npm permissions: Could not test")
                
        except Exception as e:
            ColorOutput.error(f"Diagnostic error: {e}")
    
    def show_manual_setup_instructions(self):
        """Show manual setup instructions when automatic setup fails"""
        print("MANUAL SETUP INSTRUCTIONS:")
        print("=" * 30)
        print()
        print("If automatic setup fails, try these manual steps:")
        print()
        print("1. Open a terminal in the 'src' directory")
        print("2. Run these commands one by one:")
        print()
        print("   rm -rf node_modules package-lock.json")
        print("   npm cache clean --force")
        print("   npm config set registry https://registry.npmjs.org/")
        print("   npm install readline-sync@1.4.10")
        print("   npm install kahoot.js@3.0.4")
        print()
        print("3. If you're behind a corporate firewall:")
        print("   npm config set strict-ssl false")
        print("   npm config set registry http://registry.npmjs.org/")
        print()
        print("4. If you have permission issues (Linux/Mac):")
        print("   mkdir ~/.npm-global")
        print("   npm config set prefix '~/.npm-global'")
        print("   export PATH=~/.npm-global/bin:$PATH")
        print()
        print("5. Test the installation:")
        print("   node -e \"require('readline-sync'); require('kahoot.js'); console.log('OK');\"")
        print()
        
        platform_name = PlatformManager.detect_platform()
        if platform_name == "windows":
            print("Windows-specific tips:")
            print("- Run Command Prompt as Administrator")
            print("- Use PowerShell instead of Command Prompt")
            print("- Try: npm install --global windows-build-tools")
        elif platform_name in ["linux", "macos"]:
            print("Unix-specific tips:")
            print("- Use 'sudo' only if absolutely necessary")
            print("- Consider using Node Version Manager (nvm)")
            print("- Check if you need build tools: sudo apt install build-essential (Ubuntu)")

    
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
