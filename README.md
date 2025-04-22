# Kitty-Tools - v36.2

<div align="left">

[![Version](https://img.shields.io/badge/Version-36.2-orange.svg)](https://github.com/CPScript/Kitty-Tools)
[![License](https://img.shields.io/badge/License-CC0_1.0-blue.svg)](https://github.com/CPScript/Kitty-Tools/blob/main/LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows_|_Linux_|_Web_|_Android_|_IOS|_Mobile-orange.svg)](https://github.com/CPScript/Kitty-Tools)

</div>

## Overview

Kitty-Tools is a comprehensive suite of utilities designed for enhancing and analyzing Kahoot quiz interactions. The toolkit provides powerful features for educators, students, and quiz enthusiasts, enabling advanced quiz analysis, answer retrieval, and automated participation capabilities.

<div align="center">
 
  ![Header Image](https://github.com/user-attachments/assets/329567e9-2de0-4cf8-92be-86b525365514)
  <img src="https://github.com/user-attachments/assets/74d15637-c774-41d7-9c6d-3e5316e0087d" width="80%" />
  ![image](https://github.com/user-attachments/assets/36fa992b-6c7b-428e-ba83-722f9a8b52d0)

</div>

## ✨ Key Features

- **Answer Retrieval System** - Obtain answers for any Kahoot quiz using Quiz ID or Game PIN
- **Multi-bot Participation** - Create multiple automated quiz participants with configurable behaviors
- **Cross-Platform Support** - Works on Windows, macOS, Linux, and Android (via Termux)
- **Modern GUI Interface** - Sleek, intuitive graphical user interface with dark theme
- **Export Functionality** - Save quiz answers in text format for future reference
- **Enhanced CLI Mode** - Full functionality available via command line for low-resource environments

<div align="center">
  <img src="https://github.com/user-attachments/assets/ab185a22-f7a3-41f5-a507-0cfcf6c453cd" width="80%" />
</div>

## 🚀 Installation Guide

### Prerequisites

- Python 3.6+ 
- Git 
- Node.js (for Flooder functionality)

### Installation by Platform

<details>
<summary><b>Windows</b></summary>

1. Install Python from [python.org/downloads](https://www.python.org/downloads/) (ensure "Add to PATH" is checked)
2. Install Git from [git-scm.com/download/win](https://git-scm.com/download/win)
3. Open Command Prompt and run:
   ```
   git clone https://github.com/CPScript/Kitty-Tools
   cd Kitty-Tools
   python main.py
   ```
</details>

<details>
<summary><b>Linux/macOS</b></summary>

1. Install required packages:
   ```bash
   # Ubuntu/Debian
   sudo apt install python3 python3-pip git
   
   # Fedora
   sudo dnf install python3 python3-pip git
   
   # macOS (with Homebrew)
   brew install python git
   ```

2. Clone and run:
   ```bash
   git clone https://github.com/CPScript/Kitty-Tools
   cd Kitty-Tools
   python3 main.py
   ```
</details>

<details>
<summary><b>Mobile</b></summary>

1. Install Termux by *F-Droid* **And** IOS using [iSH](https://ish.app/)
2. Install requirements:
   ```bash
   pkg install python git
   git clone https://github.com/CPScript/Kitty-Tools
   cd Kitty-Tools/LITE
   python lite.py
   ```
</details>

<details>
<summary><b>GitHub Codespace / Replit</b></summary>

#### Codespace
1. Create a new Codespace based on the repository
2. In the terminal, run:
   ```bash
   python main.py
   ```

#### Replit
1. Use this replit link
   ```bash
   https://replit.com/@Kitty-Tools/Kitty-Tools
   ```
</details>

## 📊 Usage Guide

### 1. Answer Viewer

The Answer Viewer module allows you to retrieve answers for Kahoot quizzes:

1. Start the application with `python main.py`
2. Select "Answer Hack" from the main menu
3. Enter the Kahoot Quiz ID or Game PIN
4. View answers displayed in an organized format
5. Optionally export answers to a text file

### 2. Kahoot Flooder

The Flooder creates multiple bot participants in a Kahoot game:

1. Start the application with `python main.py`
2. Select "Kahoot Flooder" from the main menu
3. Configure bot settings:
   - Game PIN
   - Number of bots
   - Name generation options
   - Bot behavior settings
4. Start the flooder and optionally control bot responses

### 3. Graphical Interface

For a more user-friendly experience:

1. Start the application with `python main.py`
2. Select "GUI" from the main menu
3. Use the intuitive tabbed interface to access all features

## 🔧 Advanced Configuration

Kitty-Tools supports various advanced configurations and custom settings:

- **Name Generation** - Generate random names or use custom prefixes
- **Anti-Detection Mode** - Implement techniques to avoid bot detection
- **Export Format Control** - Customize how answers are exported
- **Bot Behavior Patterns** - Configure response timing and answer selection

## ❓ Troubleshooting

**Common Issues:**

- **Module Not Found** - Run `pip install <module-name>` for any missing dependencies
- **Node.js Not Found** - Install Node.js for Flooder functionality
- **Game PIN Connection Fails** - Verify the PIN and ensure the Kahoot game is active
- **Performance Issues** - Use LITE version on low-resource systems

## 📜 Legal Disclaimer

Kitty-Tools is provided for **educational purposes only**. This software is designed to demonstrate educational platform vulnerabilities and to be used in controlled, ethical environments.

The developers do not endorse or encourage any use of this software that violates terms of service of educational platforms or disrupts educational activities. Use at your own risk and responsibility.

## 🤝 Contributors

A special thanks to all contributors who have helped make Kitty-Tools better:

- **@CPScript** - Lead Developer & Project Maintainer
- **@Ccode-lang** - Core Development & API Integration
- **@xTobyPlayZ** - Flooder Module Development
- **@cheepling** - Quality Assurance & Bug Reporting
- **@Zacky2613** - Technical Support & Issue Resolution
- **@KiraKenjiro** - Code Review & Optimization

## 📱 Mobile Support

For mobile devices, we provide Kitty-Tools LITE - a streamlined version designed specifically for Android via Termux:

```bash
cd Kitty-Tools/LITE
python lite.py
```

The LITE version offers core functionality with reduced resource requirements.

## 🌟 Star the Project

If you find Kitty-Tools useful, please consider giving it a star on GitHub to help others discover it!

---

<p align="center">
  &copy; 2025 Kitty-Tools | All rights reserved
</p>
