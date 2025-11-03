"""
JARVIS AI Assistant - Main GUI Application
PyQt5 GUI interface for voice assistant
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTextEdit, QLabel,
                             QGroupBox, QCheckBox, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon, QTextCursor
import threading

from jarvis_core import JarvisCore


class JarvisWorker(QThread):
    """
    Worker thread for JARVIS operations
    """
    response_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, jarvis_core):
        super().__init__()
        self.jarvis = jarvis_core
        self.is_running = False
        self.listen_once = False

    def run(self):
        """
        Main worker thread loop
        """
        self.is_running = True

        while self.is_running:
            try:
                if self.listen_once or self.jarvis.is_active:
                    self.status_signal.emit("Listening...")

                    command = self.jarvis.listen(timeout=10)

                    if command:
                        self.response_signal.emit(f"You: {command}")
                        self.status_signal.emit("Processing...")

                        response = self.jarvis.process_command(command)

                        self.response_signal.emit(f"JARVIS: {response}")
                        self.jarvis.speak(response)
                        self.status_signal.emit("Ready")

                        if self.listen_once:
                            self.listen_once = False
                            self.is_running = False
                    else:
                        self.status_signal.emit("Ready")

                else:
                    self.msleep(100)

            except Exception as e:
                self.error_signal.emit(f"Error: {str(e)}")
                self.status_signal.emit("Error occurred")

    def stop(self):
        """
        Stop the worker thread
        """
        self.is_running = False
        self.jarvis.is_active = False


class JarvisGUI(QMainWindow):
    """
    Main GUI window for JARVIS AI Assistant
    """

    def __init__(self):
        super().__init__()
        self.jarvis = JarvisCore()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface
        """
        self.setWindowTitle("JARVIS AI Assistant")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New';
                font-size: 12px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #1e1e1e;
            }
            QPushButton:pressed {
                background-color: #00aa00;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #666666;
                border-color: #666666;
            }
            QLabel {
                color: #00ff00;
                font-size: 14px;
            }
            QGroupBox {
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QCheckBox {
                color: #00ff00;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #00ff00;
                border-radius: 3px;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                background-color: #00ff00;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        title_label = QLabel("J.A.R.V.I.S")
        title_font = QFont("Arial", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("Just A Rather Very Intelligent System")
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMinimumHeight(300)
        main_layout.addWidget(self.log_display)

        self.status_label = QLabel("Status: Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont("Arial", 12, QFont.Bold)
        self.status_label.setFont(status_font)
        main_layout.addWidget(self.status_label)

        control_group = QGroupBox("Voice Controls")
        control_layout = QHBoxLayout()

        self.start_btn = QPushButton("Start Listening")
        self.start_btn.clicked.connect(self.start_listening)
        control_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop Listening")
        self.stop_btn.clicked.connect(self.stop_listening)
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.stop_btn)

        self.listen_once_btn = QPushButton("Listen Once")
        self.listen_once_btn.clicked.connect(self.listen_once)
        control_layout.addWidget(self.listen_once_btn)

        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)

        options_group = QGroupBox("Options")
        options_layout = QHBoxLayout()

        self.conversation_mode_checkbox = QCheckBox("Conversation Mode (No Wake Word)")
        self.conversation_mode_checkbox.stateChanged.connect(self.toggle_conversation_mode)
        options_layout.addWidget(self.conversation_mode_checkbox)

        self.camera_checkbox = QCheckBox("Enable Camera")
        options_layout.addWidget(self.camera_checkbox)

        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        button_layout = QHBoxLayout()

        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.clicked.connect(self.clear_log)
        button_layout.addWidget(self.clear_btn)

        self.help_btn = QPushButton("Help")
        self.help_btn.clicked.connect(self.show_help)
        button_layout.addWidget(self.help_btn)

        self.exit_btn = QPushButton("Exit")
        self.exit_btn.clicked.connect(self.close_application)
        button_layout.addWidget(self.exit_btn)

        main_layout.addLayout(button_layout)

        self.log_message("JARVIS AI Assistant initialized")
        self.log_message("Click 'Start Listening' to begin")
        self.log_message("=" * 50)

    def log_message(self, message: str):
        """
        Add message to log display

        Args:
            message: Message to log
        """
        self.log_display.append(message)
        self.log_display.moveCursor(QTextCursor.End)

    def update_status(self, status: str):
        """
        Update status label

        Args:
            status: Status message
        """
        self.status_label.setText(f"Status: {status}")

    def start_listening(self):
        """
        Start continuous listening mode
        """
        if self.worker is None or not self.worker.isRunning():
            self.jarvis.is_active = True
            self.worker = JarvisWorker(self.jarvis)
            self.worker.response_signal.connect(self.log_message)
            self.worker.status_signal.connect(self.update_status)
            self.worker.error_signal.connect(self.log_message)
            self.worker.start()

            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.listen_once_btn.setEnabled(False)
            self.log_message("Started continuous listening mode")

    def stop_listening(self):
        """
        Stop continuous listening mode
        """
        if self.worker:
            self.worker.stop()
            self.worker.wait()

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.listen_once_btn.setEnabled(True)
        self.update_status("Ready")
        self.log_message("Stopped listening")

    def listen_once(self):
        """
        Listen for a single command
        """
        if self.worker is None or not self.worker.isRunning():
            self.worker = JarvisWorker(self.jarvis)
            self.worker.listen_once = True
            self.worker.response_signal.connect(self.log_message)
            self.worker.status_signal.connect(self.update_status)
            self.worker.error_signal.connect(self.log_message)
            self.worker.start()

            self.listen_once_btn.setEnabled(False)
            self.start_btn.setEnabled(False)

            def enable_buttons():
                self.listen_once_btn.setEnabled(True)
                self.start_btn.setEnabled(True)

            self.worker.finished.connect(enable_buttons)

    def toggle_conversation_mode(self, state):
        """
        Toggle conversation mode

        Args:
            state: Checkbox state
        """
        self.jarvis.conversation_mode = (state == Qt.Checked)
        mode = "enabled" if self.jarvis.conversation_mode else "disabled"
        self.log_message(f"Conversation mode {mode}")

    def clear_log(self):
        """
        Clear the log display
        """
        self.log_display.clear()
        self.log_message("Log cleared")

    def show_help(self):
        """
        Show help dialog with available commands
        """
        help_text = """
        JARVIS AI Assistant - Available Commands:

        Basic Commands:
        - "What time is it?" / "Tell me the time"
        - "What's the date?" / "Tell me the date"
        - "Take a screenshot"
        - "System info" / "System status"

        Application Control:
        - "Open [app name]" (e.g., "Open notepad")
        - "Close [app name]"
        - "Volume up/down/mute"

        Web & Search:
        - "Search [query]"
        - "Google/Bing/DuckDuckGo [query]"
        - "YouTube [query]"
        - "Wikipedia [query]"
        - "Open [website.com]"

        Vision & Camera:
        - "Take a photo"
        - "Detect faces"
        - "Read text" (OCR)

        AI Conversation:
        - Ask any question for AI response

        Exit:
        - "Exit" / "Goodbye" / "Quit"

        Note: Enable "Conversation Mode" to skip wake word
        """

        msg = QMessageBox()
        msg.setWindowTitle("JARVIS Help")
        msg.setText(help_text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #00ff00;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 5px 15px;
            }
        """)
        msg.exec_()

    def close_application(self):
        """
        Close the application
        """
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()

        self.jarvis.speak("Shutting down JARVIS. Goodbye!")
        self.close()

    def closeEvent(self, event):
        """
        Handle window close event

        Args:
            event: Close event
        """
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()


def main():
    """
    Main entry point for the application
    """
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = JarvisGUI()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
