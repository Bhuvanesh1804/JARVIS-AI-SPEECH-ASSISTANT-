"""
Basic Task Automation Module
Handles simple automation tasks like opening apps, screenshots, etc.
"""

import os
import platform
import subprocess
import webbrowser
import pyautogui
import datetime
import psutil
from typing import Optional, Dict


class TaskAutomation:
    """
    Class for handling basic automation tasks
    """

    def __init__(self):
        """
        Initialize task automation
        """
        self.system = platform.system()

    def get_time(self) -> str:
        """
        Get current time

        Returns:
            Current time as string
        """
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")

    def get_date(self) -> str:
        """
        Get current date

        Returns:
            Current date as string
        """
        now = datetime.datetime.now()
        return now.strftime("%A, %B %d, %Y")

    def get_datetime(self) -> Dict[str, str]:
        """
        Get current date and time

        Returns:
            Dictionary with date and time
        """
        return {
            "time": self.get_time(),
            "date": self.get_date()
        }

    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """
        Take a screenshot

        Args:
            filename: Optional filename to save screenshot

        Returns:
            Path to saved screenshot
        """
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = os.path.join(os.path.expanduser("~"), "Pictures", filename)

        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            screenshot_path = filename
            pyautogui.screenshot(screenshot_path)
            return screenshot_path

    def open_application(self, app_name: str) -> bool:
        """
        Open an application

        Args:
            app_name: Name of application to open

        Returns:
            True if successful, False otherwise
        """
        app_name_lower = app_name.lower()

        common_apps = {
            "notepad": "notepad.exe" if self.system == "Windows" else "TextEdit",
            "calculator": "calc.exe" if self.system == "Windows" else "Calculator",
            "chrome": "chrome" if self.system == "Windows" else "Google Chrome",
            "firefox": "firefox",
            "edge": "msedge" if self.system == "Windows" else "Microsoft Edge",
            "explorer": "explorer.exe" if self.system == "Windows" else "Finder",
            "cmd": "cmd.exe" if self.system == "Windows" else "Terminal",
            "terminal": "cmd.exe" if self.system == "Windows" else "Terminal",
        }

        app_command = common_apps.get(app_name_lower, app_name)

        try:
            if self.system == "Windows":
                os.startfile(app_command) if app_command.endswith('.exe') else subprocess.Popen([app_command])
            elif self.system == "Darwin":
                subprocess.Popen(["open", "-a", app_command])
            else:
                subprocess.Popen([app_command])
            return True
        except Exception as e:
            print(f"Error opening application: {e}")
            return False

    def open_website(self, url: str) -> bool:
        """
        Open a website in default browser

        Args:
            url: URL to open

        Returns:
            True if successful, False otherwise
        """
        try:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error opening website: {e}")
            return False

    def get_system_info(self) -> Dict[str, str]:
        """
        Get system information

        Returns:
            Dictionary with system info
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            return {
                "system": self.system,
                "cpu_usage": f"{cpu_percent}%",
                "memory_usage": f"{memory.percent}%",
                "disk_usage": f"{disk.percent}%",
                "memory_available": f"{memory.available / (1024**3):.2f} GB"
            }
        except Exception as e:
            print(f"Error getting system info: {e}")
            return {"error": str(e)}

    def close_application(self, app_name: str) -> bool:
        """
        Close a running application

        Args:
            app_name: Name of application to close

        Returns:
            True if successful, False otherwise
        """
        try:
            for proc in psutil.process_iter(['name']):
                if app_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    return True
            return False
        except Exception as e:
            print(f"Error closing application: {e}")
            return False

    def volume_control(self, action: str) -> bool:
        """
        Control system volume

        Args:
            action: "up", "down", or "mute"

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.system == "Windows":
                if action == "up":
                    pyautogui.press("volumeup")
                elif action == "down":
                    pyautogui.press("volumedown")
                elif action == "mute":
                    pyautogui.press("volumemute")
                return True
            else:
                print("Volume control not implemented for this OS")
                return False
        except Exception as e:
            print(f"Error controlling volume: {e}")
            return False


task_automation = TaskAutomation()
