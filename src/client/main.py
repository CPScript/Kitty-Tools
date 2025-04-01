#!/usr/bin/env python3
import os
import sys
import json
import time
import random
import platform
import subprocess
import threading
import urllib.request
import urllib.error
from urllib.parse import urlparse
from datetime import datetime
from functools import partial

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTabWidget, QTextEdit, 
                             QScrollArea, QFrame, QMessageBox, QProgressBar,
                             QGridLayout, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem,
                             QHeaderView, QComboBox, QFileDialog, QCheckBox, QGroupBox, QStackedWidget)
from PyQt5.QtCore import (Qt, QThread, pyqtSignal, QSize, QTimer, QRect)
from PyQt5.QtGui import (QFont, QColor, QPalette, QIcon, QPainter)

class ThemeEngine:
    class Colors:
        DARK_BG = "#151515"
        MID_BG = "#1E1E1E"
        LIGHT_BG = "#282828"
        BORDER = "#383838"
        
        PUMPKIN = "#FF6D00"
        PUMPKIN_LIGHT = "#FF8F40"
        
        TEXT_PRIMARY = "#F8F8F8"
        TEXT_SECONDARY = "#B8B8B8"
        TEXT_DISABLED = "#707070"
        
        SUCCESS = "#4CAF50"
        WARNING = "#FFC107"
        ERROR = "#F44336"
        INFO = "#03A9F4"
    
    class Fonts:
        FAMILY_MAIN = "Segoe UI"
        FAMILY_FALLBACK = "Arial, sans-serif"
        FAMILY_MONO = "Consolas, 'Courier New', monospace"
        
        SIZE_SMALL = 9
        SIZE_NORMAL = 10
        SIZE_MEDIUM = 12
        SIZE_LARGE = 14
        
        @staticmethod
        def get_font(size=10, weight=QFont.Normal, italic=False):
            font = QFont(ThemeEngine.Fonts.FAMILY_MAIN, int(size), weight)
            font.setItalic(italic)
            return font
        
        @staticmethod
        def get_mono_font(size=10, weight=QFont.Normal):
            font = QFont(ThemeEngine.Fonts.FAMILY_MONO.split(",")[0].strip(), size, weight)
            return font
    
    @staticmethod
    def get_stylesheet():
        colors = ThemeEngine.Colors
        
        return f"""
        QWidget {{
            background-color: {colors.DARK_BG};
            color: {colors.TEXT_PRIMARY};
            font-family: "{ThemeEngine.Fonts.FAMILY_MAIN}", {ThemeEngine.Fonts.FAMILY_FALLBACK};
            font-size: {ThemeEngine.Fonts.SIZE_NORMAL}pt;
            outline: none;
        }}
        
        QLabel {{
            background-color: transparent;
            color: {colors.TEXT_PRIMARY};
        }}
        
        QLabel[heading="true"] {{
            font-size: {ThemeEngine.Fonts.SIZE_LARGE}pt;
            font-weight: bold;
            color: {colors.PUMPKIN};
        }}
        
        QFrame[frameShape="4"] {{
            background-color: {colors.BORDER};
            max-height: 1px;
        }}
        
        QFrame[frameShape="5"] {{
            background-color: {colors.BORDER};
            max-width: 1px;
        }}
        
        QFrame#cardFrame {{
            background-color: {colors.MID_BG};
            border-radius: 8px;
            border: 1px solid {colors.BORDER};
        }}
        
        QPushButton {{
            background-color: {colors.MID_BG};
            color: {colors.TEXT_PRIMARY};
            border: 1px solid {colors.BORDER};
            border-radius: 8px;
            padding: 8px 16px;
            min-height: 36px;
            text-align: center;
        }}
        
        QPushButton:hover {{
            background-color: {colors.LIGHT_BG};
            border-color: {colors.PUMPKIN};
        }}
        
        QPushButton:pressed {{
            background-color: {colors.DARK_BG};
            border-color: {colors.PUMPKIN};
        }}
        
        QPushButton:disabled {{
            background-color: {colors.DARK_BG};
            color: {colors.TEXT_DISABLED};
            border-color: {colors.BORDER};
        }}
        
        QPushButton[accent="true"] {{
            background-color: {colors.PUMPKIN};
            color: {colors.DARK_BG};
            font-weight: bold;
            border: none;
        }}
        
        QPushButton[accent="true"]:hover {{
            background-color: {colors.PUMPKIN_LIGHT};
        }}
        
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {colors.MID_BG};
            color: {colors.TEXT_PRIMARY};
            border: 1px solid {colors.BORDER};
            border-radius: 8px;
            padding: 8px;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border: 1px solid {colors.PUMPKIN};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {colors.BORDER};
            border-radius: 8px;
            background-color: {colors.DARK_BG};
            top: -1px;
        }}
        
        QTabBar::tab {{
            background-color: {colors.MID_BG};
            color: {colors.TEXT_SECONDARY};
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 8px 16px;
            margin-right: 2px;
            font-size: {ThemeEngine.Fonts.SIZE_NORMAL}pt;
            min-width: 120px;
            min-height: 32px;
        }}
        
        QTabBar::tab:hover {{
            background-color: {colors.LIGHT_BG};
            color: {colors.TEXT_PRIMARY};
        }}
        
        QTabBar::tab:selected {{
            background-color: {colors.DARK_BG};
            color: {colors.PUMPKIN};
            border-bottom: 2px solid {colors.PUMPKIN};
            font-weight: bold;
        }}
        
        QScrollBar:vertical {{
            background-color: {colors.DARK_BG};
            width: 12px;
            margin: 0px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors.LIGHT_BG};
            min-height: 30px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors.PUMPKIN};
        }}
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QTableWidget {{
            background-color: {colors.MID_BG};
            alternate-background-color: {colors.LIGHT_BG};
            color: {colors.TEXT_PRIMARY};
            border: 1px solid {colors.BORDER};
            border-radius: 8px;
            gridline-color: {colors.BORDER};
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {colors.BORDER};
        }}
        
        QTableWidget::item:selected {{
            background-color: {colors.PUMPKIN};
            color: {colors.DARK_BG};
        }}
        
        QHeaderView::section {{
            background-color: {colors.DARK_BG};
            color: {colors.PUMPKIN};
            font-weight: bold;
            padding: 16px 8px;
            border: none;
            border-right: 1px solid {colors.BORDER};
            border-bottom: 1px solid {colors.BORDER};
        }}
        
        QProgressBar {{
            border: 1px solid {colors.BORDER};
            border-radius: 8px;
            background-color: {colors.MID_BG};
            text-align: center;
            color: {colors.TEXT_PRIMARY};
            font-weight: bold;
            height: 16px;
        }}
        
        QProgressBar::chunk {{
            background-color: {colors.PUMPKIN};
            border-radius: 7px;
        }}
        
        QComboBox {{
            background-color: {colors.MID_BG};
            color: {colors.TEXT_PRIMARY};
            border: 1px solid {colors.BORDER};
            border-radius: 8px;
            padding: 8px 16px;
            min-height: 36px;
        }}
        
        QGroupBox {{
            font-weight: bold;
            border: 1px solid {colors.BORDER};
            border-radius: 8px;
            margin-top: 1.5ex;
            padding: 16px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 16px;
            top: -1ex;
            padding: 0 8px;
            color: {colors.PUMPKIN};
            background-color: {colors.MID_BG};
        }}
        
        QCheckBox {{
            spacing: 8px;
            background-color: transparent;
            min-height: 24px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 1px solid {colors.BORDER};
            border-radius: 4px;
            background-color: {colors.MID_BG};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {colors.PUMPKIN};
        }}
        
        #consoleTextEdit {{
            background-color: {colors.DARK_BG};
            color: {colors.TEXT_PRIMARY};
            border: 1px solid {colors.BORDER};
            border-radius: 8px;
            padding: 8px;
            font-family: {ThemeEngine.Fonts.FAMILY_MONO};
            font-size: {ThemeEngine.Fonts.SIZE_NORMAL}pt;
            line-height: 1.3;
        }}
        """

class CardFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("cardFrame")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(16)

class KahootAPI:
    BASE_API = "https://play.kahoot.it/rest/kahoots/"
    CHALLENGE_API = "https://kahoot.it/rest/challenges/pin/"
    
    @staticmethod
    def get_quiz_by_id(quiz_id):
        try:
            url = f"{KahootAPI.BASE_API}{quiz_id}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json'
            }
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_quiz_id_from_pin(pin):
        try:
            url = f"{KahootAPI.CHALLENGE_API}{pin}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json'
            }
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                return {'quiz_id': data.get('id')}
        except Exception as e:
            return {"error": str(e)}

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
            details.update({
                "question": self._clean_text(question.get("question", "")),
                "choices": [],
                "amount_of_answers": len(question.get("choices", [])),
                "amount_of_correct_answers": 0
            })
            
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
            return None
        
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
                        if details.get('description'):
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
            return False

class KahootWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, str)
    
    def __init__(self, operation, data=None):
        super().__init__()
        self.operation = operation
        self.data = data
    
    def run(self):
        try:
            if self.operation == "get_quiz":
                self.progress.emit(10, "Connecting to Kahoot servers...")
                quiz_id = self.data
                
                if quiz_id.isdigit():
                    self.progress.emit(20, "Detected game PIN. Resolving Quiz ID...")
                    result = KahootAPI.get_quiz_id_from_pin(quiz_id)
                    
                    if "error" in result:
                        self.error.emit(f"Failed to get quiz ID from PIN: {result['error']}")
                        return
                    
                    quiz_id = result["quiz_id"]
                    self.progress.emit(40, f"Found Quiz ID: {quiz_id}")
                
                self.progress.emit(60, "Retrieving quiz data...")
                quiz_data = KahootAPI.get_quiz_by_id(quiz_id)
                
                if "error" in quiz_data:
                    self.error.emit(f"Failed to fetch quiz: {quiz_data['error']}")
                    return
                
                self.progress.emit(80, "Processing quiz data...")
                kahoot = KahootQuiz(quiz_data)
                
                if not kahoot.valid:
                    self.error.emit("Invalid quiz data returned from Kahoot")
                    return
                
                self.progress.emit(100, "Quiz loaded successfully!")
                self.finished.emit(kahoot)
            
            elif self.operation == "export_answers":
                kahoot, filename = self.data
                self.progress.emit(50, "Exporting answers to file...")
                
                if kahoot.export_answers_to_file(filename):
                    self.progress.emit(100, "Answers exported successfully!")
                    self.finished.emit(True)
                else:
                    self.error.emit("Failed to export answers to file")
            
            elif self.operation == "run_flooder":
                self.progress.emit(10, "Checking for Node.js...")
                
                try:
                    subprocess.run(["node", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.progress.emit(30, "Node.js found, checking for required modules...")
                    
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    base_dir = os.path.dirname(os.path.dirname(script_dir))
                    flood_js_path = os.path.join(base_dir, "src", "flood.js")
                    
                    if not os.path.exists(flood_js_path):
                        self.error.emit(f"Flood script not found at: {flood_js_path}")
                        return
                    
                    self.progress.emit(50, "Starting Kahoot flooder...")
                    
                    process = subprocess.Popen(
                        ["node", flood_js_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1,
                        universal_newlines=True
                    )
                    
                    self.progress.emit(100, "Flooder started successfully!")
                    self.finished.emit(process)
                
                except subprocess.CalledProcessError:
                    self.error.emit("Node.js is not installed. Please install Node.js to use the flooder.")
                except Exception as e:
                    self.error.emit(f"Error starting flooder: {str(e)}")
        
        except Exception as e:
            self.error.emit(f"Operation failed: {str(e)}")

class ConsoleWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("cardFrame")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        header_layout = QHBoxLayout()
        
        title = QLabel("Console Output")
        title.setProperty("heading", "true")
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedWidth(80)
        self.clear_button.clicked.connect(self.clear_console)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.clear_button)
        
        self.console = QTextEdit()
        self.console.setObjectName("consoleTextEdit")
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QTextEdit.NoWrap)
        self.console.setFont(ThemeEngine.Fonts.get_mono_font(ThemeEngine.Fonts.SIZE_NORMAL))
        
        layout.addLayout(header_layout)
        layout.addWidget(self.console)
    
    def append_text(self, text, color=None):
        if color:
            self.console.append(f'<span style="color:{color};">{text}</span>')
        else:
            self.console.append(text)
        
        scrollbar = self.console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_console(self):
        self.console.clear()
        self.append_text("Console cleared.", ThemeEngine.Colors.TEXT_SECONDARY)

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setMinimumWidth(300)
        
        self.status_label = QLabel("Loading...")
        self.status_label.setStyleSheet(f"color: {ThemeEngine.Colors.TEXT_PRIMARY}; background-color: transparent;")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.progress, 0, Qt.AlignCenter)
        layout.addWidget(self.status_label, 0, Qt.AlignCenter)
        
        self.setAutoFillBackground(True)
        palette = self.palette()
        bg_color = QColor(ThemeEngine.Colors.DARK_BG)
        bg_color.setAlpha(220)
        palette.setColor(QPalette.Window, bg_color)
        self.setPalette(palette)
        
        self.hide()
    
    def set_progress(self, value, text=None):
        if text:
            self.status_label.setText(text)
        
        self.progress.setValue(value)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.setGeometry(self.parent().rect())
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setGeometry(self.parent().rect())

class AnswerViewerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.current_kahoot = None
    
    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(main_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        
        search_card = CardFrame()
        search_layout = QVBoxLayout()
        
        search_title = QLabel("Find Kahoot Answers")
        search_title.setProperty("heading", "true")
        
        search_description = QLabel(
            "Enter a Kahoot Quiz ID or Game PIN to retrieve all answers. "
            "Quiz IDs are alphanumeric, Game PINs are numeric."
        )
        search_description.setWordWrap(True)
        
        input_layout = QHBoxLayout()
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter Kahoot Quiz ID or Game PIN")
        
        self.load_button = QPushButton("Load Quiz")
        self.load_button.setProperty("accent", "true")
        self.load_button.setFixedWidth(130)
        self.load_button.clicked.connect(self.load_quiz)
        
        input_layout.addWidget(self.id_input)
        input_layout.addWidget(self.load_button)
        
        search_layout.addWidget(search_title)
        search_layout.addWidget(search_description)
        search_layout.addLayout(input_layout)
        
        search_card.layout.addLayout(search_layout)
        
        info_card = CardFrame()
        info_layout = QVBoxLayout()
        
        info_title = QLabel("Quiz Information")
        info_title.setProperty("heading", "true")
        
        self.quiz_info = QTextEdit()
        self.quiz_info.setReadOnly(True)
        self.quiz_info.setMaximumHeight(150)
        
        button_layout = QHBoxLayout()
        
        self.export_button = QPushButton("Export Answers")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.export_answers)
        
        self.copy_button = QPushButton("Copy Quiz ID")
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_quiz_id)
        
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addStretch()
        
        info_layout.addWidget(info_title)
        info_layout.addWidget(self.quiz_info)
        info_layout.addLayout(button_layout)
        
        info_card.layout.addLayout(info_layout)
        
        answers_card = CardFrame()
        answers_layout = QVBoxLayout()
        
        answers_title = QLabel("Quiz Answers")
        answers_title.setProperty("heading", "true")
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["#", "Question", "Answer"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(200)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        answers_layout.addWidget(answers_title)
        answers_layout.addWidget(self.table)
        
        answers_card.layout.addLayout(answers_layout)
        
        layout.addWidget(search_card)
        layout.addWidget(info_card)
        layout.addWidget(answers_card, 1)
        
        self.loading_overlay = LoadingOverlay(self)
    
    def load_quiz(self):
        quiz_id = self.id_input.text().strip()
        
        if not quiz_id:
            QMessageBox.warning(
                self, 
                "Input Error", 
                "Please enter a Kahoot Quiz ID or Game PIN",
                QMessageBox.Ok
            )
            return
        
        self.loading_overlay.set_progress(0, "Initializing...")
        self.loading_overlay.show()
        
        self.worker = KahootWorker("get_quiz", quiz_id)
        self.worker.progress.connect(self.loading_overlay.set_progress)
        self.worker.finished.connect(self.handle_quiz_loaded)
        self.worker.error.connect(self.handle_error)
        self.worker.start()
    
    def handle_quiz_loaded(self, kahoot):
        self.loading_overlay.hide()
        self.current_kahoot = kahoot
        
        details = kahoot.get_quiz_details()
        
        self.quiz_info.clear()
        
        html_content = f"""
        <div style="font-family: '{ThemeEngine.Fonts.FAMILY_MAIN}', {ThemeEngine.Fonts.FAMILY_FALLBACK};">
            <h2 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-bottom: 10px;">{details['title']}</h2>
            <p><b style="color: {ThemeEngine.Colors.PUMPKIN};">Creator:</b> {details['creator_username']}</p>
            <p><b style="color: {ThemeEngine.Colors.PUMPKIN};">Quiz ID:</b> {details['uuid']}</p>
            <p><b style="color: {ThemeEngine.Colors.PUMPKIN};">Questions:</b> {details['question_count']}</p>
        """
        
        if details['description']:
            html_content += f"<p><b style='color: {ThemeEngine.Colors.PUMPKIN};'>Description:</b> {details['description']}</p>"
        
        html_content += "</div>"
        
        self.quiz_info.setHtml(html_content)
        
        self.table.setRowCount(0)
        
        for i in range(kahoot.get_quiz_length()):
            details = kahoot.get_question_details(i)
            
            if details["type"] == "content":
                continue
            
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            number_item = QTableWidgetItem(str(row + 1))
            number_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, number_item)
            
            question_item = QTableWidgetItem(details["question"])
            self.table.setItem(row, 1, question_item)
            
            answers = kahoot.get_answer(i)
            answer_text = ', '.join(answers) if answers else "No correct answers found"
            
            answer_item = QTableWidgetItem(answer_text)
            
            if answers:
                answer_item.setForeground(QColor(ThemeEngine.Colors.SUCCESS))
            else:
                answer_item.setForeground(QColor(ThemeEngine.Colors.ERROR))
            
            self.table.setItem(row, 2, answer_item)
        
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, 36)
        
        self.export_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        
        QMessageBox.information(
            self,
            "Quiz Loaded",
            f"Successfully loaded quiz: {details['title']}",
            QMessageBox.Ok
        )
    
    def handle_error(self, error_msg):
        self.loading_overlay.hide()
        
        QMessageBox.critical(
            self,
            "Error",
            f"An error occurred: {error_msg}",
            QMessageBox.Ok
        )
    
    def export_answers(self):
        if not self.current_kahoot:
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Export Answers",
            "kahoot_answers.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not filename:
            return
        
        self.loading_overlay.set_progress(0, "Exporting answers...")
        self.loading_overlay.show()
        
        self.worker = KahootWorker("export_answers", (self.current_kahoot, filename))
        self.worker.progress.connect(self.loading_overlay.set_progress)
        self.worker.finished.connect(lambda _: self.handle_export_finished(filename))
        self.worker.error.connect(self.handle_error)
        self.worker.start()
    
    def handle_export_finished(self, filename):
        self.loading_overlay.hide()
        
        QMessageBox.information(
            self,
            "Export Successful",
            f"Answers have been exported to:\n{filename}",
            QMessageBox.Ok
        )
    
    def copy_quiz_id(self):
        if not self.current_kahoot:
            return
        
        details = self.current_kahoot.get_quiz_details()
        quiz_id = details["uuid"]
        
        clipboard = QApplication.clipboard()
        clipboard.setText(quiz_id)
        
        QMessageBox.information(
            self,
            "Copy Successful",
            "Quiz ID copied to clipboard!",
            QMessageBox.Ok
        )

class FlooderTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.flooder_process = None
        self.stdout_thread = None
    
    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(main_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        
        content_layout = QHBoxLayout()
        
        settings_card = CardFrame()
        settings_title = QLabel("Flooder Settings")
        settings_title.setProperty("heading", "true")
        
        settings_form = QGridLayout()
        settings_form.setVerticalSpacing(12)
        settings_form.setHorizontalSpacing(16)
        
        settings_form.addWidget(QLabel("Game PIN:"), 0, 0)
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("Enter Kahoot Game PIN")
        settings_form.addWidget(self.pin_input, 0, 1)
        
        settings_form.addWidget(QLabel("Number of bots:"), 1, 0)
        self.bot_count = QLineEdit()
        self.bot_count.setPlaceholderText("Enter number (1-100)")
        self.bot_count.setText("10")
        settings_form.addWidget(self.bot_count, 1, 1)
        
        settings_form.addWidget(QLabel("Bot Name Prefix:"), 2, 0)
        self.bot_name = QLineEdit()
        self.bot_name.setPlaceholderText("Enter bot name prefix (optional)")
        settings_form.addWidget(self.bot_name, 2, 1)
        
        options_group = QGroupBox("Bot Options")
        options_layout = QVBoxLayout(options_group)
        
        self.random_names = QCheckBox("Use random names")
        self.random_names.setChecked(True)
        self.random_names.toggled.connect(self.update_name_field_state)
        
        self.antibot_mode = QCheckBox("Use anti-bot mode")
        self.name_bypass = QCheckBox("Use name formatting bypass")
        self.user_control = QCheckBox("Control bots manually")
        
        options_layout.addWidget(self.random_names)
        options_layout.addWidget(self.antibot_mode)
        options_layout.addWidget(self.name_bypass)
        options_layout.addWidget(self.user_control)
        
        settings_form.addWidget(options_group, 3, 0, 1, 2)
        
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Flooder")
        self.start_button.setProperty("accent", "true")
        self.start_button.clicked.connect(self.start_flooder)
        
        self.stop_button = QPushButton("Stop Flooder")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_flooder)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        
        settings_form.addLayout(button_layout, 4, 0, 1, 2)
        
        settings_card.layout.addWidget(settings_title)
        settings_card.layout.addLayout(settings_form)
        
        console_column = QVBoxLayout()
        
        status_card = CardFrame()
        status_layout = QHBoxLayout()
        
        status_label = QLabel("Status:")
        self.status_text = QLabel("Ready")
        self.status_text.setStyleSheet(f"color: {ThemeEngine.Colors.INFO};")
        
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_text, 1)
        
        status_card.layout.addLayout(status_layout)
        
        self.console_widget = ConsoleWidget()
        
        console_column.addWidget(status_card)
        console_column.addWidget(self.console_widget, 1)
        
        content_layout.addWidget(settings_card)
        content_layout.addLayout(console_column)
        
        warning_card = CardFrame()
        warning_layout = QHBoxLayout()
        
        warning_text = QLabel(
            "This tool is for educational purposes only. Using this tool to disrupt "
            "Kahoot games may violate Kahoot's terms of service. Use responsibly."
        )
        warning_text.setWordWrap(True)
        warning_text.setStyleSheet(f"color: {ThemeEngine.Colors.WARNING};")
        
        warning_layout.addWidget(warning_text, 1)
        
        warning_card.layout.addLayout(warning_layout)
        
        layout.addWidget(warning_card)
        layout.addLayout(content_layout, 1)
        
        self.loading_overlay = LoadingOverlay(self)
        
        self.console_widget.append_text("Kahoot Flooder initialized and ready.", ThemeEngine.Colors.INFO)
        self.console_widget.append_text("Enter a Game PIN and click 'Start Flooder' to begin.", ThemeEngine.Colors.TEXT_SECONDARY)
    
    def update_name_field_state(self, random_names_enabled):
        self.bot_name.setEnabled(not random_names_enabled)
        if random_names_enabled:
            self.bot_name.setPlaceholderText("Random names will be used")
        else:
            self.bot_name.setPlaceholderText("Enter bot name prefix")
    
    def start_flooder(self):
        pin = self.pin_input.text().strip()
        
        if not pin or not pin.isdigit():
            QMessageBox.warning(
                self, 
                "Input Error", 
                "Please enter a valid Kahoot Game PIN (numbers only)",
                QMessageBox.Ok
            )
            return
        
        try:
            bot_count = int(self.bot_count.text().strip())
            if bot_count < 1 or bot_count > 100:
                raise ValueError("Bot count must be between 1 and 100")
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e), QMessageBox.Ok)
            return
        
        self.loading_overlay.set_progress(0, "Initializing flooder...")
        self.loading_overlay.show()
        
        self.console_widget.append_text("Starting Kahoot flooder...", ThemeEngine.Colors.PUMPKIN)
        self.console_widget.append_text(f"Game PIN: {pin}", ThemeEngine.Colors.TEXT_SECONDARY)
        self.console_widget.append_text(f"Number of bots: {bot_count}", ThemeEngine.Colors.TEXT_SECONDARY)
        
        self.worker = KahootWorker("run_flooder")
        self.worker.progress.connect(self.loading_overlay.set_progress)
        self.worker.finished.connect(self.handle_flooder_started)
        self.worker.error.connect(self.handle_error)
        self.worker.start()
    
    def handle_flooder_started(self, process):
        self.loading_overlay.hide()
        self.flooder_process = process
        
        self.status_text.setText("Flooder running")
        self.status_text.setStyleSheet(f"color: {ThemeEngine.Colors.SUCCESS};")
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        self.pin_input.setEnabled(False)
        self.bot_count.setEnabled(False)
        self.bot_name.setEnabled(False)
        self.random_names.setEnabled(False)
        self.antibot_mode.setEnabled(False)
        self.name_bypass.setEnabled(False)
        self.user_control.setEnabled(False)
        
        self.console_widget.append_text("Flooder process started successfully!", ThemeEngine.Colors.SUCCESS)
        self.console_widget.append_text("Connecting bots to the game...", ThemeEngine.Colors.TEXT_PRIMARY)
        
        self.stdout_thread = threading.Thread(target=self.read_stdout, daemon=True)
        self.stdout_thread.start()
    
    def read_stdout(self):
        try:
            for line in iter(self.flooder_process.stdout.readline, ''):
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                    
                line_color = ThemeEngine.Colors.TEXT_PRIMARY
                
                if "error" in line_stripped.lower() or "failed" in line_stripped.lower():
                    line_color = ThemeEngine.Colors.ERROR
                elif "success" in line_stripped.lower() or "correct" in line_stripped.lower():
                    line_color = ThemeEngine.Colors.SUCCESS
                elif "connected" in line_stripped.lower():
                    line_color = ThemeEngine.Colors.INFO
                
                QApplication.instance().processEvents()
                self.console_widget.append_text(line_stripped, line_color)
        except Exception as e:
            QApplication.instance().processEvents()
            self.console_widget.append_text(f"Error reading process output: {str(e)}", ThemeEngine.Colors.ERROR)
    
    def stop_flooder(self):
        if self.flooder_process:
            try:
                self.flooder_process.terminate()
                try:
                    self.flooder_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.flooder_process.kill()
                
                self.flooder_process = None
                
                self.status_text.setText("Flooder stopped")
                self.status_text.setStyleSheet(f"color: {ThemeEngine.Colors.WARNING};")
                
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                
                self.pin_input.setEnabled(True)
                self.bot_count.setEnabled(True)
                self.bot_name.setEnabled(not self.random_names.isChecked())
                self.random_names.setEnabled(True)
                self.antibot_mode.setEnabled(True)
                self.name_bypass.setEnabled(True)
                self.user_control.setEnabled(True)
                
                self.console_widget.append_text("Flooder stopped by user.", ThemeEngine.Colors.WARNING)
            except Exception as e:
                self.console_widget.append_text(f"Error stopping flooder: {str(e)}", ThemeEngine.Colors.ERROR)
    
    def handle_error(self, error_msg):
        self.loading_overlay.hide()
        
        self.status_text.setText("Error occurred")
        self.status_text.setStyleSheet(f"color: {ThemeEngine.Colors.ERROR};")
        
        self.console_widget.append_text(f"ERROR: {error_msg}", ThemeEngine.Colors.ERROR)
        
        QMessageBox.critical(self, "Error", error_msg, QMessageBox.Ok)

class InfoTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(24)  # Increased spacing between cards
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(main_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        
        # Header Card with Version Information
        header_card = CardFrame()
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Kitty Tools")
        title.setStyleSheet(f"""
            color: {ThemeEngine.Colors.PUMPKIN};
            font-size: 32pt;
            font-weight: bold;
            text-align: center;
        """)
        title.setAlignment(Qt.AlignCenter)
        
        version = QLabel("Version 2.1.0")
        version.setStyleSheet(f"""
            color: {ThemeEngine.Colors.TEXT_SECONDARY};
            font-size: 14pt;
            margin-top: 5px;
            text-align: center;
        """)
        version.setAlignment(Qt.AlignCenter)
        
        tagline = QLabel("Advanced Kahoot Quiz Utility Suite")
        tagline.setStyleSheet(f"""
            color: {ThemeEngine.Colors.TEXT_PRIMARY};
            font-size: 16pt;
            margin-top: 10px;
            text-align: center;
        """)
        tagline.setAlignment(Qt.AlignCenter)
        
        header_separator = QFrame()
        header_separator.setFrameShape(QFrame.HLine)
        header_separator.setStyleSheet(f"background-color: {ThemeEngine.Colors.PUMPKIN}; max-height: 2px;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(version)
        header_layout.addWidget(tagline)
        header_layout.addWidget(header_separator)
        
        header_card.layout.addLayout(header_layout)
        
        # About Card with Enhanced Content
        about_card = CardFrame()
        
        about_title = QLabel("About Kitty Tools")
        about_title.setProperty("heading", "true")
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setFrameStyle(QFrame.NoFrame)
        about_text.setStyleSheet("background-color: transparent;")
        about_text.setMinimumHeight(180)  # Force more space
        
        about_text.setHtml(f"""
            <div style="color: {ThemeEngine.Colors.TEXT_PRIMARY}; font-family: '{ThemeEngine.Fonts.FAMILY_MAIN}', {ThemeEngine.Fonts.FAMILY_FALLBACK};">
                <p style="font-size: 12pt; line-height: 1.4;">
                    Kitty Tools is a suite of utilities designed for Kahoot quizzes, providing educators, 
                    students, and enthusiasts with advanced features to enhance their Kahoot experience. With a 
                    focus on educational purposes, this toolset offers powerful capabilities for quiz analysis, 
                    answer retrieval, and automated participation.
                </p>
                
                <h3 style="color: {ThemeEngine.Colors.PUMPKIN}; font-size: 14pt; margin-top: 16px;">Key Features</h3>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; grid-gap: 20px; margin-top: 10px;">
                    <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px; border-left: 3px solid {ThemeEngine.Colors.PUMPKIN};">
                        <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">Advanced Answer Viewer</h4>
                        <p>Instantly retrieve answers for any Kahoot quiz using either Quiz ID or Game PIN(Game pin might not work for some quizes). 
                        Support for all question types including multiple-choice, true/false, and puzzle formats.</p>
                    </div>
                    
                    <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px; border-left: 3px solid {ThemeEngine.Colors.PUMPKIN};">
                        <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">Kahoot Flooder</h4>
                        <p>Create multiple automated bots with customizable behavior for testing quiz performance. 
                        Features include random name generation and anti-detection capabilities.</p>
                    </div>
                    
                    <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px; border-left: 3px solid {ThemeEngine.Colors.PUMPKIN};">
                        <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">Export Functionality</h4>
                        <p>Save quiz answers in text format for future reference or study purposes.
                        Organized output includes questions, answers, and quiz metadata.</p>
                    </div>
                    
                    <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px; border-left: 3px solid {ThemeEngine.Colors.PUMPKIN};">
                        <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">Modern User Interface</h4>
                        <p>Enjoy a sleek, responsive design with a customized dark theme for reduced eye strain.
                        Intuitive controls and visual feedback for all operations.</p>
                    </div>
                </div>
            </div>
        """)
        
        about_card.layout.addWidget(about_title)
        about_card.layout.addWidget(about_text)
        
        # Development Team Card with Enhanced Layout
        contributors_card = CardFrame()
        
        contributors_title = QLabel("Development Team")
        contributors_title.setProperty("heading", "true")
        
        contributors_text = QTextEdit()
        contributors_text.setReadOnly(True)
        contributors_text.setFrameStyle(QFrame.NoFrame)
        contributors_text.setStyleSheet("background-color: transparent;")
        contributors_text.setMinimumHeight(200)
        
        contributors_text.setHtml(f"""
            <div style="color: {ThemeEngine.Colors.TEXT_PRIMARY}; font-family: '{ThemeEngine.Fonts.FAMILY_MAIN}', {ThemeEngine.Fonts.FAMILY_FALLBACK};">
                <p style="font-size: 12pt; margin-bottom: 15px;">
                    The Kitty Tools project is maintained by a dedicated developer and contributors
                    who are passionate about educational technology and software development.
                </p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; grid-gap: 20px;">
                    <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px;">
                        <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">Developer</h4>
                        <ul style="list-style-type: none; padding-left: 5px;">
                            <li style="margin-bottom: 10px;"><b style="color: {ThemeEngine.Colors.PUMPKIN};">CPScript</b> - Lead Developer & Project Architect</li>
                        </ul>
                    </div>
                    
                    <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px;">
                        <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">Contributors</h4>
                        <ul style="list-style-type: none; padding-left: 5px;">
                            <li style="margin-bottom: 10px;"><b style="color: {ThemeEngine.Colors.PUMPKIN};">@Ccode-lang</b> - Core Development & API Integration</li>
                            <li style="margin-bottom: 10px;"><b style="color: {ThemeEngine.Colors.PUMPKIN};">@xTobyPlayZ</b> - Flooder Module Development</li>
                            <li style="margin-bottom: 10px;"><b style="color: {ThemeEngine.Colors.PUMPKIN};">@cheepling</b> - Quality Assurance & Bug Reporting</li>
                            <li style="margin-bottom: 10px;"><b style="color: {ThemeEngine.Colors.PUMPKIN};">@Zacky2613</b> - Technical Support & Issue Resolution</li>
                            <li style="margin-bottom: 10px;"><b style="color: {ThemeEngine.Colors.PUMPKIN};">@KiraKenjiro</b> - Code Review & Optimization</li>
                        </ul>
                    </div>
                </div>
                
                <div style="margin-top: 15px; background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0;">
                        <b>Want to contribute?</b> Visit our repository to learn how you can help improve Kitty Tools.
                    </p>
                </div>
            </div>
        """)
        
        contributors_card.layout.addWidget(contributors_title)
        contributors_card.layout.addWidget(contributors_text)
        
        # Technical Details Card
        tech_card = CardFrame()
        
        tech_title = QLabel("Technical Information")
        tech_title.setProperty("heading", "true")
        
        tech_text = QTextEdit()
        tech_text.setReadOnly(True)
        tech_text.setFrameStyle(QFrame.NoFrame)
        tech_text.setStyleSheet("background-color: transparent;")
        tech_text.setMinimumHeight(180)
        
        tech_text.setHtml(f"""
            <div style="color: {ThemeEngine.Colors.TEXT_PRIMARY}; font-family: '{ThemeEngine.Fonts.FAMILY_MAIN}', {ThemeEngine.Fonts.FAMILY_FALLBACK};">
                <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">System Requirements</h4>
                    <ul>
                        <li><b>Operating System:</b> Windows 7/8/10/11, macOS 10.14+, Linux (most distributions)</li>
                        <li><b>Python:</b> Version 3.6 or higher</li>
                        <li><b>Required Libraries:</b> PyQt5, requests, urllib3</li>
                        <li><b>Node.js:</b> Required for Flooder functionality (v12.0.0+)</li>
                        <li><b>Disk Space:</b> ~20MB for installation</li>
                    </ul>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; grid-gap: 20px;">
                    <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px;">
                        <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">Architecture</h4>
                        <p>Kitty Tools is built with a modular architecture that separates the user interface from the core functionality. The application uses:</p>
                        <ul>
                            <li>PyQt5 for the graphical interface</li>
                            <li>Threaded operations for non-blocking API requests</li>
                            <li>Node.js subprocess handling for the flooder module</li>
                        </ul>
                    </div>
                    
                    <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px;">
                        <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">Version History</h4>
                        <ul>
                            <li><b>v2.1.0</b> - Current release with improved UI</li>
                            <li><b>v2.0.0</b> - Major redesign with new theming engine</li>
                            <li><b>v1.5.0</b> - Added flooder capabilities</li>
                            <li><b>v1.0.0</b> - Initial release with basic answer viewing</li>
                        </ul>
                    </div>
                </div>
            </div>
        """)
        
        tech_card.layout.addWidget(tech_title)
        tech_card.layout.addWidget(tech_text)
        
        # Legal Card with Enhanced Content
        legal_card = CardFrame()
        
        legal_title = QLabel("Legal Information")
        legal_title.setProperty("heading", "true")
        
        legal_text = QTextEdit()
        legal_text.setReadOnly(True)
        legal_text.setFrameStyle(QFrame.NoFrame)
        legal_text.setStyleSheet("background-color: transparent;")
        legal_text.setMinimumHeight(150)
        
        legal_text.setHtml(f"""
            <div style="color: {ThemeEngine.Colors.TEXT_PRIMARY}; font-family: '{ThemeEngine.Fonts.FAMILY_MAIN}', {ThemeEngine.Fonts.FAMILY_FALLBACK};">
                <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 20px; border-radius: 8px; border-left: 4px solid {ThemeEngine.Colors.WARNING};">
                    <h4 style="color: {ThemeEngine.Colors.WARNING}; margin-top: 0px;">Important Disclaimer</h4>
                    <p style="font-size: 12pt; line-height: 1.4;">
                        This software is provided for educational purposes only. The developers of Kitty Tools do not
                        endorse or encourage any use of this software that violates the terms of service of Kahoot
                        or disrupts educational activities. Use at your own risk and responsibility.
                    </p>
                </div>
                
                <div style="margin-top: 15px; display: grid; grid-template-columns: 1fr 1fr; grid-gap: 20px;">
                    <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px;">
                        <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">Terms of Use</h4>
                        <p>By using this software, you agree to:</p>
                        <ul>
                            <li>Use responsibly and ethically</li>
                            <li>Accept full responsibility for your actions</li>
                            <li>Not hold the developers liable for misuse</li>
                        </ul>
                    </div>
                    
                    <div style="background-color: {ThemeEngine.Colors.DARK_BG}; padding: 15px; border-radius: 8px;">
                        <h4 style="color: {ThemeEngine.Colors.PUMPKIN}; margin-top: 0px;">License</h4>
                        <p>Kitty Tools is distributed under the MIT License, which allows for:</p>
                        <ul>
                            <li>Free use in both private and commercial settings</li>
                            <li>Modification and distribution of the code</li>
                            <li>Subject to proper attribution</li>
                        </ul>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 20px; padding: 10px; font-weight: bold; color: {ThemeEngine.Colors.PUMPKIN};">
                    © 2025 Kitty Tools Development Team. All rights reserved. | CPScript
                </div>
            </div>
        """)
        
        legal_card.layout.addWidget(legal_title)
        legal_card.layout.addWidget(legal_text)
        
        # Add all cards to the layout
        layout.addWidget(header_card)
        layout.addWidget(about_card)
        layout.addWidget(contributors_card)
        layout.addWidget(tech_card)
        layout.addWidget(legal_card)
        layout.addStretch(1)

class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None, accent=False):
        super().__init__(text, parent)
        
        self._scale = 1.0
        self.accent = accent
        
        if accent:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ThemeEngine.Colors.PUMPKIN};
                    color: {ThemeEngine.Colors.DARK_BG};
                    border: none;
                    border-radius: 12px;
                    padding: 5px 15px;
                    font-weight: bold;
                }}
                
                QPushButton:hover {{
                    background-color: {ThemeEngine.Colors.PUMPKIN_LIGHT};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ThemeEngine.Colors.MID_BG};
                    color: {ThemeEngine.Colors.TEXT_PRIMARY};
                    border: 1px solid {ThemeEngine.Colors.BORDER};
                    border-radius: 12px;
                    padding: 5px 15px;
                }}
                
                QPushButton:hover {{
                    background-color: {ThemeEngine.Colors.LIGHT_BG};
                    border-color: {ThemeEngine.Colors.PUMPKIN};
                }}
            """)
        
        self.setCursor(Qt.PointingHandCursor)
        
        # Animation effect for hover
        self.animation = QTimer()
        self.animation.timeout.connect(self.update)
        self.animation.setInterval(5)
        self.growing = False
        
    def enterEvent(self, event):
        self.growing = True
        self.animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.growing = False
        self.animation.start()
        super().leaveEvent(event)
        
    def update(self):
        if self.growing and self._scale < 1.1:
            self._scale += 0.01
            self.updateGeometry()
            self.repaint()
        elif not self.growing and self._scale > 1.0:
            self._scale -= 0.01
            self.updateGeometry()
            self.repaint()
        else:
            self.animation.stop()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Save current state
        painter.save()
        
        # Apply scale transformation
        center = self.rect().center()
        painter.translate(center)
        painter.scale(self._scale, self._scale)
        painter.translate(-center.x(), -center.y())
        
        # Draw button
        if self.accent:
            painter.setBrush(QColor(ThemeEngine.Colors.PUMPKIN))
            painter.setPen(Qt.NoPen)
        else:
            painter.setBrush(QColor(ThemeEngine.Colors.MID_BG))
            painter.setPen(QColor(ThemeEngine.Colors.BORDER))
            
        painter.drawRoundedRect(self.rect(), 12, 12)
        
        # Draw text
        if self.accent:
            painter.setPen(QColor(ThemeEngine.Colors.DARK_BG))
        else:
            painter.setPen(QColor(ThemeEngine.Colors.TEXT_PRIMARY))
            
        font = painter.font()
        font.setBold(self.accent)
        painter.setFont(font)
        
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())
        
        # Restore painter
        painter.restore()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Kitty Tools GUI")
        self.setMinimumSize(900, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header with version and centered tab buttons
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            background-color: {ThemeEngine.Colors.DARK_BG};
            border-bottom: 1px solid {ThemeEngine.Colors.BORDER};
        """)
        header_frame.setMinimumHeight(60)
        header_frame.setMaximumHeight(60)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 8, 16, 8)
        
        # Title with version
        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        
        title_label = QLabel("Kitty Tools")
        title_label.setStyleSheet(f"color: {ThemeEngine.Colors.PUMPKIN}; font-size: 18pt; font-weight: bold;")
        
        version_label = QLabel("Graphical | v2.1.0")
        version_label.setStyleSheet(f"color: {ThemeEngine.Colors.TEXT_SECONDARY}; font-size: 9pt;")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(version_label)
        
        # Center tab buttons
        tab_button_layout = QHBoxLayout()
        tab_button_layout.setSpacing(10)
        tab_button_layout.setAlignment(Qt.AlignCenter)
        
        self.answer_button = AnimatedButton("Answer Viewer")
        self.flooder_button = AnimatedButton("Kahoot Flooder")
        self.info_button = AnimatedButton("Information")
        
        # Set initial selected state
        self.answer_button.setProperty("accent", "true")
        self.answer_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {ThemeEngine.Colors.PUMPKIN};
                color: {ThemeEngine.Colors.DARK_BG};
                border: none;
                border-radius: 12px;
                padding: 5px 15px;
                font-weight: bold;
            }}
        """)
        
        # Connect button clicks
        self.answer_button.clicked.connect(lambda: self.switch_tab(0))
        self.flooder_button.clicked.connect(lambda: self.switch_tab(1))
        self.info_button.clicked.connect(lambda: self.switch_tab(2))
        
        tab_button_layout.addWidget(self.answer_button)
        tab_button_layout.addWidget(self.flooder_button)
        tab_button_layout.addWidget(self.info_button)
        
        # Status indicator
        self.status_indicator = QLabel("Ready")
        self.status_indicator.setStyleSheet(f"color: {ThemeEngine.Colors.INFO};")
        
        # Add all elements to header
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(tab_button_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.status_indicator)
        
        # Stacked widget instead of tab widget
        self.stack = QStackedWidget()
        
        self.answer_tab = AnswerViewerTab()
        self.flooder_tab = FlooderTab()
        self.info_tab = InfoTab()
        
        self.stack.addWidget(self.answer_tab)
        self.stack.addWidget(self.flooder_tab)
        self.stack.addWidget(self.info_tab)
        
        main_layout.addWidget(header_frame)
        main_layout.addWidget(self.stack, 1)
        
        self.apply_global_style()
        self.update_status_for_tab(0)
    
    def switch_tab(self, index):
        # Update button states
        buttons = [self.answer_button, self.flooder_button, self.info_button]
        
        for i, button in enumerate(buttons):
            if i == index:
                button.setProperty("accent", "true")
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {ThemeEngine.Colors.PUMPKIN};
                        color: {ThemeEngine.Colors.DARK_BG};
                        border: none;
                        border-radius: 12px;
                        padding: 5px 15px;
                        font-weight: bold;
                    }}
                """)
            else:
                button.setProperty("accent", "false")
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {ThemeEngine.Colors.MID_BG};
                        color: {ThemeEngine.Colors.TEXT_PRIMARY};
                        border: 1px solid {ThemeEngine.Colors.BORDER};
                        border-radius: 12px;
                        padding: 5px 15px;
                    }}
                    
                    QPushButton:hover {{
                        background-color: {ThemeEngine.Colors.LIGHT_BG};
                        border-color: {ThemeEngine.Colors.PUMPKIN};
                    }}
                """)
        
        # Switch to the selected tab
        self.stack.setCurrentIndex(index)
        self.update_status_for_tab(index)
    
    def apply_global_style(self):
        self.setStyleSheet(ThemeEngine.get_stylesheet())
    
    def update_status_for_tab(self, index):
        tab_names = ["Answer Viewer", "Kahoot Flooder", "Information"]
        tab_name = tab_names[index]
        
        if tab_name == "Answer Viewer":
            self.status_indicator.setText("Ready to fetch quiz answers")
            self.status_indicator.setStyleSheet(f"color: {ThemeEngine.Colors.INFO};")
        elif tab_name == "Kahoot Flooder":
            self.status_indicator.setText("Configure flooder settings")
            self.status_indicator.setStyleSheet(f"color: {ThemeEngine.Colors.WARNING};")
        else:
            self.status_indicator.setText("Information")
            self.status_indicator.setStyleSheet(f"color: {ThemeEngine.Colors.TEXT_SECONDARY};")
    
    def closeEvent(self, event):
        if hasattr(self.flooder_tab, 'flooder_process') and self.flooder_tab.flooder_process:
            reply = QMessageBox.question(
                self, 
                "Confirm Exit", 
                "The Kahoot Flooder is still running. Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.flooder_tab.stop_flooder()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        min_height = 600
        min_width = 900
        
        if self.height() < min_height or self.width() < min_width:
            self.setMinimumHeight(min_height)
            self.setMinimumWidth(min_width)

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Kitty Tools")
    app.setApplicationVersion("2.1.0")
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
