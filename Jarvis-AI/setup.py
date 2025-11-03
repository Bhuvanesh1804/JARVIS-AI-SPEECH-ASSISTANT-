"""
JARVIS AI Setup Script
Automated setup for dependencies and configuration
"""

import subprocess
import sys
import os
import json
from pathlib import Path


def print_header(message):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f" {message}")
    print("=" * 60 + "\n")


def install_requirements():
    """Install required packages from requirements.txt"""
    print_header("Installing Dependencies")

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        print("Pip upgraded successfully\n")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not upgrade pip: {e}\n")

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\nAll dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError installing dependencies: {e}")
        return False


def setup_config():
    """Setup configuration file"""
    print_header("Setting Up Configuration")

    config_path = Path("config/config.json")

    if config_path.exists():
        print("Configuration file already exists.")
        response = input("Do you want to reconfigure? (y/n): ").lower()
        if response != 'y':
            print("Skipping configuration setup.")
            return True

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error reading config: {e}")
        config = {}

    print("\nCurrent API Keys Configuration:")
    print(f"Gemini API: {'Set' if config.get('GEMINI_API') else 'Not Set'}")
    print(f"OpenAI API: {'Set' if config.get('OPENAI_API') else 'Not Set'}")

    update = input("\nDo you want to update API keys? (y/n): ").lower()

    if update == 'y':
        print("\nEnter API keys (press Enter to skip):")

        gemini_api = input("Gemini API Key: ").strip()
        if gemini_api:
            config['GEMINI_API'] = gemini_api

        openai_api = input("OpenAI API Key: ").strip()
        if openai_api:
            config['OPENAI_API'] = openai_api

        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print("\nConfiguration saved successfully!")
            return True
        except Exception as e:
            print(f"\nError saving configuration: {e}")
            return False
    else:
        print("Configuration unchanged.")
        return True


def check_pyaudio():
    """Check and provide instructions for PyAudio installation"""
    print_header("Checking PyAudio Installation")

    try:
        import pyaudio
        print("PyAudio is already installed!")
        return True
    except ImportError:
        print("PyAudio not found. Installing...")

        if sys.platform == "win32":
            print("\nFor Windows, you may need to install PyAudio manually:")
            print("1. Download the appropriate .whl file from:")
            print("   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
            print("2. Install using: pip install [downloaded_file].whl")
        elif sys.platform == "darwin":
            print("\nFor macOS, run:")
            print("   brew install portaudio")
            print("   pip install pyaudio")
        else:
            print("\nFor Linux, run:")
            print("   sudo apt-get install python3-pyaudio portaudio19-dev")

        return False


def create_directories():
    """Create necessary directories"""
    print_header("Creating Directory Structure")

    directories = [
        "config",
        "func/basic",
        "logs",
        "data"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created: {directory}")

    print("\nDirectory structure created successfully!")
    return True


def test_imports():
    """Test if all required modules can be imported"""
    print_header("Testing Module Imports")

    required_modules = [
        "PyQt5",
        "speech_recognition",
        "pyttsx3",
        "cv2",
        "numpy",
        "requests",
        "bs4",
        "wikipedia"
    ]

    failed_modules = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - FAILED")
            failed_modules.append(module)

    if failed_modules:
        print(f"\nWarning: The following modules failed to import: {', '.join(failed_modules)}")
        return False
    else:
        print("\nAll required modules imported successfully!")
        return True


def main():
    """Main setup function"""
    print_header("JARVIS AI Assistant - Setup")

    print("This script will set up JARVIS AI Assistant on your system.")
    print("It will:")
    print("  1. Install required Python packages")
    print("  2. Create necessary directories")
    print("  3. Configure API keys")
    print("  4. Test imports")

    response = input("\nDo you want to continue? (y/n): ").lower()

    if response != 'y':
        print("Setup cancelled.")
        return

    success = True

    success = create_directories() and success

    success = install_requirements() and success

    success = setup_config() and success

    check_pyaudio()

    success = test_imports() and success

    print_header("Setup Complete")

    if success:
        print("JARVIS AI Assistant has been set up successfully!")
        print("\nTo run the application:")
        print("  python main.py")
        print("\nFor command-line mode:")
        print("  python jarvis_core.py")
    else:
        print("Setup completed with some warnings.")
        print("Please review the messages above and fix any issues.")

    print("\nNote: Make sure to configure your API keys in config/config.json")
    print("for AI conversation features to work.")


if __name__ == "__main__":
    main()
