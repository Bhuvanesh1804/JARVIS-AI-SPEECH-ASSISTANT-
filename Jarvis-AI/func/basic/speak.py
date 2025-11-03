"""
Text-to-Speech Module
Handles voice output for the assistant
"""

import pyttsx3
import threading
from typing import Optional
import platform


class VoiceSpeaker:
    """
    Voice speaker class for text-to-speech output
    """

    def __init__(self, rate: int = 150, volume: float = 0.9, voice_id: Optional[int] = None):
        """
        Initialize the voice speaker

        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
            voice_id: Voice ID to use (0 for male, 1 for female, None for default)
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

        voices = self.engine.getProperty('voices')
        if voice_id is not None and 0 <= voice_id < len(voices):
            self.engine.setProperty('voice', voices[voice_id].id)

        self.is_speaking = False
        self.lock = threading.Lock()

    def speak(self, text: str, async_mode: bool = False) -> None:
        """
        Convert text to speech

        Args:
            text: Text to speak
            async_mode: If True, speak in background thread
        """
        if not text:
            return

        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)

    def _speak_sync(self, text: str) -> None:
        """
        Synchronous speak method

        Args:
            text: Text to speak
        """
        with self.lock:
            try:
                self.is_speaking = True
                print(f"JARVIS: {text}")
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Error in speak: {e}")
            finally:
                self.is_speaking = False

    def stop(self) -> None:
        """
        Stop current speech
        """
        try:
            self.engine.stop()
            self.is_speaking = False
        except Exception as e:
            print(f"Error stopping speech: {e}")

    def set_rate(self, rate: int) -> None:
        """
        Set speech rate

        Args:
            rate: Speech rate (words per minute)
        """
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float) -> None:
        """
        Set volume level

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.engine.setProperty('volume', max(0.0, min(1.0, volume)))

    def get_available_voices(self) -> list:
        """
        Get list of available voices

        Returns:
            List of voice objects
        """
        return self.engine.getProperty('voices')


_global_speaker = None


def speak(text: str, rate: int = 150, volume: float = 0.9, async_mode: bool = False) -> None:
    """
    Quick function to speak text

    Args:
        text: Text to speak
        rate: Speech rate
        volume: Volume level
        async_mode: If True, speak in background
    """
    global _global_speaker

    if _global_speaker is None:
        _global_speaker = VoiceSpeaker(rate=rate, volume=volume)

    _global_speaker.speak(text, async_mode=async_mode)


def stop_speaking() -> None:
    """
    Stop current speech output
    """
    global _global_speaker
    if _global_speaker:
        _global_speaker.stop()
