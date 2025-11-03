# JARVIS AI Assistant

**J**ust **A** **R**ather **V**ery **I**ntelligent **S**ystem

A powerful desktop voice assistant built with Python, featuring speech recognition, AI conversation, computer vision, and task automation capabilities.

## Features

### Core Capabilities
- **Voice Recognition**: Listen and understand voice commands using Google Speech Recognition
- **Text-to-Speech**: Natural voice responses using pyttsx3
- **AI Conversation**: Intelligent conversations powered by Google Gemini or OpenAI
- **Web Search**: Search using Google, Bing, DuckDuckGo, YouTube, and Wikipedia
- **Computer Vision**: Face detection, object recognition, and OCR using OpenCV and EasyOCR
- **Task Automation**: Open apps, take screenshots, control volume, and more
- **GUI Interface**: Beautiful PyQt5 interface with dark theme

### Supported Platforms
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 20.04+)

## Installation

### Prerequisites
- Python 3.8 or higher
- Microphone and speakers
- Webcam (optional, for vision features)

### Quick Setup

1. **Clone or download the project**
   ```bash
   cd JARVIS-AI
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

   This will:
   - Install all required dependencies
   - Create necessary directories
   - Help you configure API keys

3. **Manual Installation (Alternative)**
   ```bash
   pip install -r requirements.txt
   ```

### Platform-Specific Notes

#### Windows
- PyAudio may require manual installation
- Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Install with: `pip install [downloaded_file].whl`

#### macOS
```bash
brew install portaudio
pip install pyaudio
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev
sudo apt-get install espeak libespeak-dev
```

## Configuration

Edit `config/config.json` to customize settings:

```json
{
  "GEMINI_API": "your_gemini_api_key",
  "OPENAI_API": "your_openai_api_key",
  "cookie_bing": "",
  "OCR_Colab": "",
  "camera": "0",
  "speech_engine": "pyttsx3",
  "voice_rate": 150,
  "voice_volume": 0.9,
  "language": "en",
  "wake_word": "jarvis"
}
```

### Getting API Keys

#### Google Gemini API (Recommended)
1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Add to `config.json`

#### OpenAI API (Optional)
1. Visit: https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `config.json`

## Usage

### GUI Mode (Recommended)

```bash
python main.py
```

**GUI Controls:**
- **Start Listening**: Continuous listening mode (use wake word "jarvis")
- **Stop Listening**: Stop continuous mode
- **Listen Once**: Listen for a single command
- **Conversation Mode**: Disable wake word requirement
- **Clear Log**: Clear the conversation log
- **Help**: Show available commands

### Command Line Mode

```bash
python jarvis_core.py
```

## Available Commands

### Basic Commands
- "What time is it?" / "Tell me the time"
- "What's the date?" / "Tell me the date"
- "Take a screenshot"
- "System info" / "System status"

### Application Control
- "Open notepad" / "Open calculator"
- "Open chrome" / "Open firefox"
- "Close [app name]"
- "Volume up" / "Volume down" / "Volume mute"

### Web & Search
- "Search [query]" (default Google search)
- "Google [query]"
- "Bing [query]"
- "DuckDuckGo [query]"
- "YouTube [query]"
- "Wikipedia [query]"
- "Open youtube.com" / "Open github.com"

### Computer Vision
- "Take a photo" / "Take a picture"
- "Detect faces"
- "Read text" (OCR from camera)

### AI Conversation
Ask any question:
- "What is the capital of France?"
- "Tell me a joke"
- "How does photosynthesis work?"
- "Write a poem about technology"

### Exit
- "Exit" / "Goodbye" / "Quit" / "Bye"

## Project Structure

```
JARVIS-AI/
│
├── main.py                 # GUI application entry point
├── jarvis_core.py          # Core logic and command routing
├── setup.py                # Setup script
├── requirements.txt        # Python dependencies
│
├── config/
│   └── config.json         # Configuration file
│
├── func/
│   └── basic/
│       ├── __init__.py
│       ├── listen.py       # Speech recognition module
│       ├── speak.py        # Text-to-speech module
│       ├── tasks.py        # Task automation module
│       ├── web_search.py   # Web search module
│       └── vision.py       # Computer vision module
│
├── logs/                   # Application logs (auto-created)
└── data/                   # User data (auto-created)
```

## Modules Overview

### listen.py
- Voice input capture
- Speech-to-text conversion
- Background listening support

### speak.py
- Text-to-speech output
- Voice customization
- Async speaking support

### tasks.py
- Time/date functions
- Screenshot capture
- Application control
- System information
- Volume control

### web_search.py
- Multi-engine search support
- Wikipedia integration
- Search results parsing

### vision.py
- Face detection
- Photo capture
- OCR (text extraction)
- Object detection

### jarvis_core.py
- Command parsing
- Task routing
- AI integration
- Main logic loop

## Troubleshooting

### Microphone not working
- Check system microphone permissions
- Test with: `python -m speech_recognition`
- Adjust `energy_threshold` in `listen.py`

### Text-to-speech not working
- Verify pyttsx3 installation
- Check system audio settings
- Try different voice IDs in config

### PyAudio installation fails
- Use platform-specific instructions above
- Try: `pip install pipwin && pipwin install pyaudio` (Windows)

### AI responses not working
- Verify API keys in `config/config.json`
- Check internet connection
- Review API quota limits

### Camera not detected
- Check camera permissions
- Try different camera index in config (0, 1, 2)
- Verify OpenCV installation

### Import errors
```bash
pip install --upgrade -r requirements.txt
```

## Advanced Configuration

### Custom Wake Word
Change in `config/config.json`:
```json
"wake_word": "computer"
```

### Voice Settings
Adjust speech rate and volume:
```json
"voice_rate": 150,    # 100-200 recommended
"voice_volume": 0.9   # 0.0 to 1.0
```

### Language Support
Change recognition language:
```json
"language": "en-US"   # en-US, en-GB, es-ES, fr-FR, etc.
```

## Dependencies

Core packages:
- PyQt5: GUI framework
- SpeechRecognition: Voice input
- pyttsx3: Text-to-speech
- pyaudio: Audio I/O
- opencv-python: Computer vision
- easyocr: Optical character recognition
- google-generativeai: AI conversation
- requests, beautifulsoup4: Web scraping
- wikipedia: Wikipedia API

See `requirements.txt` for complete list.

## Performance Tips

1. **Reduce OCR load time**: EasyOCR loads models on first use (may take time)
2. **Optimize voice recognition**: Adjust `energy_threshold` for your environment
3. **Improve response time**: Use conversation mode to skip wake word detection
4. **Save resources**: Close camera when not in use

## Security Notes

- Keep API keys confidential
- Never commit `config.json` with real API keys
- Use environment variables for production deployment
- Review permissions before running automation commands

## Contributing

This is a modular project. To add features:

1. Create new module in `func/basic/`
2. Add command patterns in `jarvis_core.py`
3. Register handlers in `_register_commands()`
4. Update documentation

## License

This project is provided as-is for educational purposes.

## Credits

Built with:
- Google Speech Recognition
- Google Gemini AI
- OpenCV
- EasyOCR
- PyQt5

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review module documentation
3. Test individual components
4. Check API service status

## Version

Version: 1.0.0
Last Updated: 2025

---

**Made with Python and AI**
