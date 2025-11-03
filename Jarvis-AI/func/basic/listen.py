"""
Speech Recognition Module
Handles listening to user voice commands
"""

import speech_recognition as sr
from typing import Optional


class VoiceListener:
    """
    Voice listener class for capturing and recognizing speech
    """

    def __init__(self, language: str = "en-US"):
        """
        Initialize the voice listener

        Args:
            language: Language code for recognition (default: en-US)
        """
        self.recognizer = sr.Recognizer()
        self.language = language
        self.microphone = None

        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input and convert to text

        Args:
            timeout: Maximum time to wait for speech to start
            phrase_time_limit: Maximum time for phrase duration

        Returns:
            Recognized text or None if recognition fails
        """
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            print("Recognizing...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"You said: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            print("Listening timed out")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error in listen: {e}")
            return None

    def listen_background(self, callback):
        """
        Listen in background mode (non-blocking)

        Args:
            callback: Function to call with recognized text
        """
        def audio_callback(recognizer, audio):
            try:
                text = recognizer.recognize_google(audio, language=self.language)
                callback(text.lower())
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Recognition error: {e}")

        if self.microphone is None:
            self.microphone = sr.Microphone()

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        return self.recognizer.listen_in_background(self.microphone, audio_callback)


def listen_once(language: str = "en-US", timeout: int = 5) -> Optional[str]:
    """
    Quick function to listen once and return text

    Args:
        language: Language code for recognition
        timeout: Maximum time to wait

    Returns:
        Recognized text or None
    """
    listener = VoiceListener(language)
    return listener.listen(timeout=timeout)
