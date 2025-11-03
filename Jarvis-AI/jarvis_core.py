"""
JARVIS Core Module
Main logic and command routing for the AI assistant
"""

import json
import os
import re
from typing import Optional, Dict, Any, Callable
from func.basic.listen import VoiceListener
from func.basic.speak import VoiceSpeaker
from func.basic.tasks import task_automation
from func.basic.web_search import web_searcher
from func.basic.vision import vision_system


class JarvisCore:
    """
    Core class for JARVIS AI Assistant
    Handles command processing and task routing
    """

    def __init__(self, config_path: str = "config/config.json"):
        """
        Initialize JARVIS core

        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.listener = VoiceListener(language=self.config.get('language', 'en-US'))
        self.speaker = VoiceSpeaker(
            rate=self.config.get('voice_rate', 150),
            volume=self.config.get('voice_volume', 0.9)
        )

        self.wake_word = self.config.get('wake_word', 'jarvis').lower()
        self.is_active = False
        self.conversation_mode = False

        self.gemini_client = None
        self.openai_client = None
        self._init_ai_clients()

        self.command_handlers = self._register_commands()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file

        Args:
            config_path: Path to config file

        Returns:
            Configuration dictionary
        """
        try:
            if not os.path.exists(config_path):
                config_path = os.path.join(os.path.dirname(__file__), config_path)

            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def _init_ai_clients(self) -> None:
        """
        Initialize AI API clients (Gemini/OpenAI)
        """
        gemini_api = self.config.get('GEMINI_API')
        if gemini_api:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_api)
                self.gemini_client = genai.GenerativeModel('gemini-pro')
                print("Gemini AI initialized")
            except Exception as e:
                print(f"Error initializing Gemini: {e}")

        openai_api = self.config.get('OPENAI_API')
        if openai_api:
            try:
                import openai
                openai.api_key = openai_api
                self.openai_client = openai
                print("OpenAI initialized")
            except Exception as e:
                print(f"Error initializing OpenAI: {e}")

    def _register_commands(self) -> Dict[str, Callable]:
        """
        Register command handlers

        Returns:
            Dictionary of command patterns to handler functions
        """
        return {
            r'(what|tell).*time': self.handle_time,
            r'(what|tell).*date': self.handle_date,
            r'screenshot': self.handle_screenshot,
            r'open (.+)': self.handle_open,
            r'search (.+) on (.+)': self.handle_search_on,
            r'search (.+)': self.handle_search,
            r'(google|bing|duckduckgo) (.+)': self.handle_search_engine,
            r'youtube (.+)': self.handle_youtube,
            r'wikipedia (.+)': self.handle_wikipedia,
            r'system (info|status)': self.handle_system_info,
            r'take (photo|picture)': self.handle_take_photo,
            r'detect face': self.handle_detect_faces,
            r'read text': self.handle_ocr,
            r'(volume|sound) (up|down|mute)': self.handle_volume,
            r'close (.+)': self.handle_close_app,
            r'(exit|quit|goodbye|bye)': self.handle_exit,
            r'(hello|hi|hey)': self.handle_greeting,
        }

    def speak(self, text: str, async_mode: bool = False) -> None:
        """
        Speak text using voice speaker

        Args:
            text: Text to speak
            async_mode: If True, speak in background
        """
        self.speaker.speak(text, async_mode=async_mode)

    def listen(self, timeout: int = 5) -> Optional[str]:
        """
        Listen for voice input

        Args:
            timeout: Maximum wait time

        Returns:
            Recognized text or None
        """
        return self.listener.listen(timeout=timeout)

    def process_command(self, command: str) -> str:
        """
        Process voice command and execute appropriate action

        Args:
            command: Voice command text

        Returns:
            Response text
        """
        command = command.lower().strip()

        for pattern, handler in self.command_handlers.items():
            match = re.search(pattern, command)
            if match:
                try:
                    return handler(command, match)
                except Exception as e:
                    return f"Error processing command: {str(e)}"

        return self.handle_ai_conversation(command)

    def handle_time(self, command: str, match: re.Match) -> str:
        """Handle time query"""
        current_time = task_automation.get_time()
        return f"The current time is {current_time}"

    def handle_date(self, command: str, match: re.Match) -> str:
        """Handle date query"""
        current_date = task_automation.get_date()
        return f"Today is {current_date}"

    def handle_screenshot(self, command: str, match: re.Match) -> str:
        """Handle screenshot command"""
        path = task_automation.take_screenshot()
        return f"Screenshot saved to {path}"

    def handle_open(self, command: str, match: re.Match) -> str:
        """Handle open application command"""
        app_name = command.replace('open', '').strip()

        if any(domain in app_name for domain in ['.com', '.org', '.net', 'www']):
            success = task_automation.open_website(app_name)
            return f"Opening {app_name}" if success else f"Failed to open {app_name}"
        else:
            success = task_automation.open_application(app_name)
            return f"Opening {app_name}" if success else f"Failed to open {app_name}"

    def handle_search(self, command: str, match: re.Match) -> str:
        """Handle general search command"""
        query = command.replace('search', '').strip()
        web_searcher.search_google(query)
        return f"Searching for {query}"

    def handle_search_on(self, command: str, match: re.Match) -> str:
        """Handle search on specific engine"""
        parts = command.split(' on ')
        if len(parts) == 2:
            query = parts[0].replace('search', '').strip()
            engine = parts[1].strip()

            if 'google' in engine:
                web_searcher.search_google(query)
            elif 'bing' in engine:
                web_searcher.search_bing(query)
            elif 'duckduckgo' in engine:
                web_searcher.search_duckduckgo(query)

            return f"Searching {query} on {engine}"
        return "Could not understand search command"

    def handle_search_engine(self, command: str, match: re.Match) -> str:
        """Handle search engine specific command"""
        engine = match.group(1)
        query = match.group(2)

        if engine == 'google':
            web_searcher.search_google(query)
        elif engine == 'bing':
            web_searcher.search_bing(query)
        elif engine == 'duckduckgo':
            web_searcher.search_duckduckgo(query)

        return f"Searching {query} on {engine}"

    def handle_youtube(self, command: str, match: re.Match) -> str:
        """Handle YouTube search"""
        query = command.replace('youtube', '').strip()
        web_searcher.search_youtube(query)
        return f"Searching YouTube for {query}"

    def handle_wikipedia(self, command: str, match: re.Match) -> str:
        """Handle Wikipedia search"""
        query = command.replace('wikipedia', '').strip()
        result = web_searcher.search_wikipedia(query)
        return result if result else "Could not find information on Wikipedia"

    def handle_system_info(self, command: str, match: re.Match) -> str:
        """Handle system info query"""
        info = task_automation.get_system_info()
        response = f"System: {info.get('system', 'Unknown')}, "
        response += f"CPU usage: {info.get('cpu_usage', 'N/A')}, "
        response += f"Memory usage: {info.get('memory_usage', 'N/A')}"
        return response

    def handle_take_photo(self, command: str, match: re.Match) -> str:
        """Handle take photo command"""
        path = vision_system.capture_photo()
        return f"Photo captured and saved to {path}" if path else "Failed to capture photo"

    def handle_detect_faces(self, command: str, match: re.Match) -> str:
        """Handle face detection command"""
        count, _ = vision_system.detect_faces(use_camera=True)
        if count > 0:
            return f"I detected {count} face{'s' if count > 1 else ''}"
        return "No faces detected"

    def handle_ocr(self, command: str, match: re.Match) -> str:
        """Handle OCR command"""
        photo_path = vision_system.capture_photo()
        if photo_path:
            text = vision_system.perform_ocr(photo_path)
            return f"I found this text: {text}" if text else "No text found in image"
        return "Failed to capture image for OCR"

    def handle_volume(self, command: str, match: re.Match) -> str:
        """Handle volume control"""
        action = match.group(2)
        success = task_automation.volume_control(action)
        return f"Volume {action}" if success else "Failed to control volume"

    def handle_close_app(self, command: str, match: re.Match) -> str:
        """Handle close application command"""
        app_name = match.group(1)
        success = task_automation.close_application(app_name)
        return f"Closing {app_name}" if success else f"Could not close {app_name}"

    def handle_exit(self, command: str, match: re.Match) -> str:
        """Handle exit command"""
        self.is_active = False
        return "Goodbye! Have a great day."

    def handle_greeting(self, command: str, match: re.Match) -> str:
        """Handle greeting"""
        import random
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! I'm here to assist you.",
            "Greetings! How may I be of service?"
        ]
        return random.choice(greetings)

    def handle_ai_conversation(self, message: str) -> str:
        """
        Handle AI conversation using Gemini or OpenAI

        Args:
            message: User message

        Returns:
            AI response
        """
        if self.gemini_client:
            try:
                response = self.gemini_client.generate_content(message)
                return response.text
            except Exception as e:
                print(f"Gemini error: {e}")

        if self.openai_client:
            try:
                response = self.openai_client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": message}]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI error: {e}")

        return "I'm not sure how to help with that. Try asking me to search, open apps, or perform tasks."

    def run(self) -> None:
        """
        Main run loop for JARVIS
        """
        self.is_active = True
        self.speak("JARVIS online. How can I help you?")

        while self.is_active:
            try:
                command = self.listen(timeout=10)

                if command:
                    if not self.conversation_mode and self.wake_word not in command:
                        continue

                    command = command.replace(self.wake_word, '').strip()

                    if command:
                        response = self.process_command(command)
                        self.speak(response)

            except KeyboardInterrupt:
                self.speak("Shutting down JARVIS")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")


if __name__ == "__main__":
    jarvis = JarvisCore()
    jarvis.run()
