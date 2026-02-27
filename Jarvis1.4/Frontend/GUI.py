from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os
import json
import random
import time

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom" ,"can you","what's","where's","how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:    
            new_query += "?"

    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data', "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(Filename):
    Path = rf'{GraphicsDirPath}\{Filename}'
    return Path

def TempDirectoryPath(Filename):
    Path = rf'{TempDirPath}\{Filename}'
    return Path

def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Responses.data', "w", encoding='utf-8') as file:
        file.write(Text)

def GetRandomChat():
    chat_log_path = os.path.join(current_dir, "Data", "ChatLog.json")
    try:
        with open(chat_log_path, 'r', encoding='utf-8') as file:
            chat_data = json.load(file)
            
        # Get a random conversation pair (user + assistant)
        max_index = len(chat_data) - 2  # Ensure we can get pairs
        start_index = random.randrange(0, max_index, 2)  # Only start with user messages
        
        conversation = chat_data[start_index:start_index + 2]
        formatted_chat = f"User: {conversation[0]['content']}\n{Assistantname}: {conversation[1]['content']}"
        return formatted_chat
    except Exception as e:
        return f"Error loading chat: {str(e)}"

class ChatSection(QWidget):
    
    def __init__(self):
        super(ChatSection, self).__init__()
        self.last_update_time = 0
        self.current_conversations = []

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Create chat text edit
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.chat_text_edit.setFrameStyle(QFrame.StyledPanel)
        self.chat_text_edit.setMinimumHeight(400)
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        layout.addWidget(self.chat_text_edit)

        # Create floating latest button
        self.latest_button = QPushButton()
        self.latest_button.setIcon(QIcon(GraphicsDirectoryPath('arrow-down.png')))
        self.latest_button.setIconSize(QSize(24, 24))
        self.latest_button.setFixedSize(40, 40)
        self.latest_button.setText("↓")
        self.latest_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                border: none;
                border-radius: 20px;
                margin: 10px;
                padding: 5px;
                font-size: 20px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.latest_button.setToolTip("Scroll to latest messages")
        self.latest_button.clicked.connect(self.scrollToLatest)
        self.latest_button.show()

        # Create mic button (same as InitialScreen)
        self.mic_button = QLabel()
        self.mic_button.setFixedSize(60, 60)
        self.mic_button.setAlignment(Qt.AlignCenter)
        self.mic_toggled = self.get_mic_status()
        self.update_mic_icon()
        self.mic_button.mousePressEvent = self.toggle_mic

        # Floating button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.latest_button)
        button_layout.addWidget(self.mic_button)
        button_layout.setContentsMargins(0, 0, 20, 20)
        layout.addLayout(button_layout)

        # Connect scroll signal
        self.chat_text_edit.verticalScrollBar().valueChanged.connect(self.onScroll)
    def get_mic_status(self):
        # Shared mic status from file
        try:
            with open(TempDirectoryPath('Mic.data'), "r", encoding='utf-8') as file:
                status = file.read().strip()
            return status == "True"
        except:
            return False

    def set_mic_status(self, status):
        with open(TempDirectoryPath('Mic.data'), "w", encoding='utf-8') as file:
            file.write("True" if status else "False")

    def update_mic_icon(self):
        if self.get_mic_status():
            pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.png')).scaled(60, 60)
        else:
            pixmap = QPixmap(GraphicsDirectoryPath('Mic_off.png')).scaled(60, 60)
        self.mic_button.setPixmap(pixmap)

    def toggle_mic(self, event=None):
        new_status = not self.get_mic_status()
        self.set_mic_status(new_status)
        self.update_mic_icon()
        # Sync with InitialScreen if exists
        if hasattr(self.parent(), 'sync_mic_buttons'):
            self.parent().sync_mic_buttons(new_status)

    def loadMessages(self):
        try:
            # Store current scroll position
            scrollbar = self.chat_text_edit.verticalScrollBar()
            current_scroll = scrollbar.value()
            
            # Load chat history from ChatLog.json
            chat_log_path = os.path.join(current_dir, "Data", "ChatLog.json")
            with open(chat_log_path, 'r', encoding='utf-8') as file:
                chat_data = json.load(file)
            
            # Get current response first (if any)
            current_message = ""
            with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
                current_message = file.read().strip()
            
            # Format the chat history
            formatted_chat = ""
            
            # Add chat history in chronological order (oldest first)
            for i in range(0, len(chat_data), 2):
                if i + 1 < len(chat_data):
                    user_msg = chat_data[i]
                    assistant_msg = chat_data[i+1]
                    formatted_chat += f"User: {user_msg['content']}\nJarvis: {assistant_msg['content']}\n\n"
            
            # Add current message at the bottom if it exists
            if current_message:
                global old_chat_message
                if current_message != old_chat_message:
                    formatted_chat += f"{current_message}\n\n"
                    old_chat_message = current_message

            # Display the messages
            if formatted_chat:
                self.addMessage(formatted_chat, 'White')
                # Restore scroll position unless there's new content
                if current_message == old_chat_message:
                    scrollbar.setValue(current_scroll)
                    
        except Exception as e:
            print(f"Error loading messages: {str(e)}")

    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('voice.png'), 60, 60)
            MicButtonInitialed()

        else:
            self.load_icon(GraphicsDirectoryPath('mic.png'), 60, 60)
            MicButtonClosed()

        self.toggled = not self.toggled

    def addMessage(self, message, color):
        self.chat_text_edit.clear()
        cursor = self.chat_text_edit.textCursor()
        
        # Create formats
        user_format = QTextCharFormat()
        user_format.setForeground(QColor('#4CAF50'))  # Green for user
        user_format.setFontWeight(QFont.Bold)
        
        assistant_format = QTextCharFormat()
        assistant_format.setForeground(QColor('#2196F3'))  # Blue for assistant
        assistant_format.setFontWeight(QFont.Bold)
        
        text_format = QTextCharFormat()
        text_format.setForeground(QColor('white'))
        
        # Set block format
        block_format = QTextBlockFormat()
        block_format.setLineHeight(150, QTextBlockFormat.ProportionalHeight)
        block_format.setAlignment(Qt.AlignLeft)
        
        # Split message into lines and format
        lines = message.split('\n')
        for line in lines:
            if line.startswith('User: '):
                cursor.setCharFormat(user_format)
                cursor.insertText('User: ')
                cursor.setCharFormat(text_format)
                cursor.insertText(line[6:] + '\n')
            elif line.startswith('Jarvis: '):
                cursor.setCharFormat(assistant_format)
                cursor.insertText('Jarvis: ')
                cursor.setCharFormat(text_format)
                cursor.insertText(line[8:] + '\n')
            else:
                cursor.setCharFormat(text_format)
                cursor.insertText(line + '\n')
            
            cursor.setBlockFormat(block_format)

    def scrollToLatest(self):
        # Scroll to the bottom to see latest messages
        scrollbar = self.chat_text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def onScroll(self, value):
        scrollbar = self.chat_text_edit.verticalScrollBar()
        # Show button when not at bottom
        if value < scrollbar.maximum() - 20:
            self.latest_button.show()
        else:
            self.latest_button.hide()

    def displayRandomChat(self):
        random_chat = GetRandomChat()
        self.chat_text_edit.clear()  # Clear previous chat
        self.addMessage(random_chat, 'White')

class InitialScreen(QWidget):
    def get_mic_status(self):
        try:
            with open(TempDirectoryPath('Mic.data'), "r", encoding='utf-8') as file:
                status = file.read().strip()
            return status == "True"
        except:
            return False

    def set_mic_status(self, status):
        with open(TempDirectoryPath('Mic.data'), "w", encoding='utf-8') as file:
            file.write("True" if status else "False")

    def update_mic_icon(self):
        if self.get_mic_status():
            pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.png')).scaled(60, 60)
        else:
            pixmap = QPixmap(GraphicsDirectoryPath('Mic_off.png')).scaled(60, 60)
        self.icon_label.setPixmap(pixmap)

    def toggle_mic(self, event=None):
        new_status = not self.get_mic_status()
        self.set_mic_status(new_status)
        self.update_mic_icon()
        # Sync with ChatSection if exists
        if hasattr(self.parent(), 'sync_mic_buttons'):
            self.parent().sync_mic_buttons(new_status)

    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        gif_label.setMovie(movie)
        max_gif_size_H = int(screen_width / 16 * 9)
        movie.setScaledSize(QSize(screen_width, max_gif_size_H))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Mic button
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(60, 60)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.update_mic_icon()
        self.icon_label.mousePressEvent = self.toggle_mic

        # Status label
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px ; margin-bottom:0;")

        # Layout
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.Data'), "r", encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)
    
    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):

        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
            MicButtonInitialed()

        else:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
            MicButtonClosed()

        self.toggled = not self.toggled

class MessageScreen(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        # Create main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Add chat section
        self.chat_section = ChatSection()
        layout.addWidget(self.chat_section)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        # Load messages on startup
        self.chat_section.loadMessages()

class CustomTopBar(QWidget):

    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen = None
        self.stacked_widget = stacked_widget

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        home_button = QPushButton()
        home_icon = QIcon(GraphicsDirectoryPath("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText("  Home")
        button_style = """
            QPushButton {
                height: 40px;
                line-height: 40px;
                background-color: rgba(60, 60, 60, 0.7);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 0 15px;
                margin: 0 5px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 0.9);
            }
            QPushButton:pressed {
                background-color: rgba(40, 40, 40, 0.9);
            }
        """
        home_button.setStyleSheet(button_style)
        message_button = QPushButton()
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("  Chat")
        message_button.setStyleSheet(button_style)    
        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicsDirectoryPath('Minimize2.png'))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet(button_style)
        minimize_button.clicked.connect(self.minimizeWindow)
        self.maximize_button= QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
        self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color:grey")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        close_button = QPushButton()
        close_icon = QIcon(GraphicsDirectoryPath('Close.png' ))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:grey")
        close_button.clicked.connect(self.closeWindow)
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color:grey;")
        title_label = QLabel(f" {str(Assistantname).capitalize()} AI    ")  
        title_label.setStyleSheet("""
            color: #ffffff;
            font-size: 18px;
            font-weight: bold;
            padding: 5px 15px;
            background: transparent;
        """)
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable = True
        self.offset = None
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(40, 40, 40, 230))
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.parent().close()
    
    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        initial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen = initial_screen

class MainWindow(QMainWindow):
    def sync_mic_buttons(self, status):
        # Sync mic button icons in both InitialScreen and ChatSection
        try:
            # InitialScreen
            initial_screen = self.centralWidget().widget(0)
            if hasattr(initial_screen, 'update_mic_icon'):
                initial_screen.update_mic_icon()
            # ChatSection
            message_screen = self.centralWidget().widget(1)
            chat_section = message_screen.findChild(ChatSection)
            if chat_section and hasattr(chat_section, 'update_mic_icon'):
                chat_section.update_mic_icon()
        except Exception as e:
            print(f"Mic sync error: {e}")
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)
        # Show chat screen by default for testing
        stacked_widget.setCurrentIndex(1)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()