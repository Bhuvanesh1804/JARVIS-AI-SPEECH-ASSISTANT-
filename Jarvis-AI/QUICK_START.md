# JARVIS AI - Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Dependencies
```bash
python setup.py
```

### Step 2: Add API Key (Optional but recommended)
1. Get free Gemini API key: https://makersuite.google.com/app/apikey
2. Open `config/config.json`
3. Paste your key in `"GEMINI_API"` field

### Step 3: Run JARVIS
```bash
python main.py
```

## First Commands to Try

1. Click **"Listen Once"** button
2. Say one of these commands:
   - "What time is it?"
   - "Search Python tutorial"
   - "Open notepad"
   - "Tell me a joke"

## Quick Tips

- **Start Listening**: Continuous mode (say "jarvis" before each command)
- **Listen Once**: Single command mode (no wake word needed)
- **Conversation Mode**: Toggle to skip wake word entirely

## Troubleshooting

**Microphone not working?**
- Check system permissions
- Speak clearly and close to mic

**API errors?**
- Add Gemini API key in config/config.json
- Check internet connection

**Import errors?**
- Run: `pip install -r requirements.txt`

## Available Commands

### Basic
- Time/date queries
- Screenshots
- System info

### Apps & Web
- Open applications
- Web searches
- YouTube/Wikipedia

### Vision
- Take photos
- Detect faces
- Read text (OCR)

### AI Chat
- Ask anything!
- Get intelligent responses

See **README.md** for complete documentation.
