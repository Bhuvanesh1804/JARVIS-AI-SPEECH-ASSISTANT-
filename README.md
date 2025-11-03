# JARVIS-AI-SPEECH-ASSISTANT-
JARVIS-AI is a Python-based speech assistant with a PyQt5 GUI interface.
It listens to voice commands, processes them, performs tasks, and replies through speech — like a personal AI assistant.


| File               | Purpose                                                                                  |
| ------------------ | ---------------------------------------------------------------------------------------- |
| `main.py`          | Runs the **GUI** and manages the assistant through worker threads.                       |
| `jarvis_core.py`   | Contains the **core logic** — speech recognition, text processing, and command handling. |
| `func/`            | Likely contains helper modules (e.g., system control, weather, music, Wikipedia, etc.).  |
| `.env`             | Stores API keys (if used, like for OpenAI or WolframAlpha).                              |
| `requirements.txt` | Lists Python dependencies.                                                               |


##    Some of the libraries used are  
"PyQt5" -  GUI (buttons, labels, text area, thread-safe updates).
"speech_recognition" -  Converts speech → text using Google Speech Recognition API (free, no API key needed).
"pyttsx3" - Converts text → speech offline (no API key required).
"wikipedia" - Fetches Wikipedia summaries.


##    API keys -
The project includes a .env file, which may optionally hold: OpenAI API key (for ChatGPT-like replies if extended)

However, based on your main.py and standard jarvis_core.py setups:
Google Speech Recognition API → used without an API key.
pyttsx3 → offline, no API key.
So, the core project can run fully offline, except for voice recognition (which uses Google’s free endpoint).


##    Methodologies used here is 

"Rule-based NLP" - Matches commands based on keywords instead of AI model understanding.
"Event-driven GUI" - PyQt5 events trigger actions (button clicks, thread signals).

"Multithreading" - Speech listening runs in background thread.

"Hybrid Offline/Online"- Speech recognition uses the cloud; all other actions are local.


##    Conclusion 

Your JARVIS AI Speech Assistant is a hybrid offline/online, modular voice assistant built using Python + PyQt5.
It applies:

Speech-to-text and text-to-speech algorithms

Rule-based natural language understanding

Multithreading for smooth GUI performance

Optional API integrations (if .env configured)

It’s a solid implementation of a lightweight AI assistant framework


##   commands 

1. Create & activate a virtual environment
cd C:\path\to\project\JARVIS-AI
python -m venv .venv
# activate
.venv\Scripts\Activate.ps1
# or in cmd:
.venv\Scripts\activate.bat

2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

Notes / common fixes
PyAudio often fails to build:
Windows: use pipwin to install the prebuilt binary:

pip install pipwin
pipwin install pyaudio

torch: requirements.txt pins torch==2.1.0 — if you have GPU and want CUDA builds, install the appropriate torch wheel from PyTorch site instead of the pinned CPU wheel:

pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

3. Configuration (API keys, microphones, etc.)(created in seperate environment in config)

mkdir -p config
cat > config/config.json <<'JSON'
{
  "GEMINI_API": "",
  "OPENAI_API_KEY": "",
  "OTHER_SETTINGS": {}
}
JSON

4. Run the app from terminal (fast)
   # activate venv if not already
python main.py
