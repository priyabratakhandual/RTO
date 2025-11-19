# RAG Chatbot - AI Enrollment & Marketing System

An intelligent AI enrollment and marketing automation system with both CLI and web interfaces, supporting voice output and text input.

## Features

- 🌐 **Web Interface** - Modern, responsive web dashboard (Flask-based)
- 💻 **CLI Interface** - Text input with voice output
- 🤖 **AI-Powered Agent** - Uses Groq for intelligent conversations
- 🔊 **Browser Voice Output** - Web Speech API with female voice synthesis
- 📊 **Student Management** - Track inquiries, follow-ups, and enrollments
- 📈 **Dashboard Analytics** - Real-time enrollment metrics
- 💬 **Real-time Chat** - Interactive conversations with students
- 🎓 **Scholarship Portal** - Comprehensive scholarship information and applications
- 📁 **Modular Architecture** - Clean separation of concerns
- 🎤 **Voice Toggle** - Enable/disable voice output in browser

## Project Structure

```
RAG Chatbot/
├── app/                    # Main application package
│   ├── __init__.py        # Package initialization
│   ├── models.py          # Data models and database
│   ├── agents.py          # AI agents and enrollment manager
│   ├── voice.py           # Voice input/output handlers
│   └── api.py             # Flask web API
├── templates/             # HTML templates
│   └── index.html         # Web interface
├── main.py                # CLI interface
├── run.sh                 # Launcher script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # Documentation
```

## Setup

### 1. Install Dependencies

Make sure you're using the virtual environment:

```bash
# Activate virtual environment
source venv/bin/activate

# Install/update packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your-groq-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

Get your API keys:
- Groq: https://console.groq.com/
- OpenAI: https://platform.openai.com/api-keys

### 3. Run the Application

**Option 1: Using the launcher script (recommended)**
```bash
./run.sh
```

**Option 2: Manual activation**
```bash
source venv/bin/activate
python3 main.py
```

## System Requirements

### Linux
- Install `ffmpeg` for MP3 audio support:
  ```bash
  sudo apt-get install ffmpeg
  ```

### macOS
- Usually works out of the box

### Windows
- Usually works out of the box

## Browser Compatibility

### Voice Output (Web Speech API)
- ✅ **Chrome/Chromium** - Full support with high-quality voices
- ✅ **Edge** - Full support with Microsoft voices
- ✅ **Safari** - Good support (macOS/iOS)
- ✅ **Firefox** - Basic support, may have fewer voices
- ❌ **Internet Explorer** - Not supported

### Recommended Browsers
- **Chrome/Edge**: Best voice quality and most female voices
- **Safari**: Good for macOS users
- **Firefox**: Functional but fewer voice options

### Voice Features
- **Automatic female voice selection** - System tries to pick the best female voice
- **Voice toggle button** - Appears next to the main title
- **Visual speaking indicator** - Shows when the system is speaking
- **Fallback handling** - Gracefully degrades if voice is not supported

## Troubleshooting

### No Voice Output in Web Interface

1. **Browser compatibility**: Use Chrome, Edge, or Safari for best voice support
2. **Check browser permissions**: Allow microphone/speaker access if prompted
3. **Voice toggle**: Make sure the voice toggle button shows "Voice: ON"
4. **Console check**: Open browser developer tools (F12) and check for errors
5. **Voice selection**: System automatically selects female voice; check browser settings if needed

### No Voice Output in CLI

1. **Check API keys**: Make sure `OPENAI_API_KEY` is set in `.env`
2. **Test audio system**: Run `python3 test_voice.py` to diagnose issues
3. **Check audio packages**: Ensure `pydub`, `pygame`, or `playsound` is installed
4. **Linux users**: Install `ffmpeg` for MP3 support

### Voice Input Not Working

1. **Check microphone**: Ensure microphone is connected and working
2. **Install audio libraries**: 
   ```bash
   sudo apt-get install portaudio19-dev  # Linux
   ```
3. **Test recording**: Check if `sounddevice` can access your microphone

### Import Errors

If you see import errors, make sure you're using the virtual environment:
```bash
source venv/bin/activate
```

## Usage

### Web Interface (Default)

1. **Start the web server (default):**
   ```bash
   source venv/bin/activate
   python3 main.py
   ```
   Or use the launcher:
   ```bash
   ./run.sh
   ```

2. **Open in browser:**
   ```
   http://localhost:5000
   ```

3. **Features available:**
   - Create new student inquiries with forms (voice responses)
   - Chat with students in real-time web interface (voice responses)
   - View enrollment dashboard with live metrics
   - Manage student records in a table
   - Export data as JSON (voice confirmation)
   - **Scholarship Portal**: Browse and apply for scholarships (voice-guided)
   - **Voice Toggle**: Enable/disable voice output with the button next to the title
   - **Speaking Indicator**: Visual feedback when the system is speaking

### CLI Interface

1. **Start the CLI:**
   ```bash
   source venv/bin/activate
   python3 main.py --cli
   ```
   Or use the launcher:
   ```bash
   ./run.sh --cli
   ```

2. **Follow text prompts** for all interactions
3. **Voice output** for agent responses and system messages

### Testing

Run the diagnostic test:
```bash
source venv/bin/activate
python3 test_voice.py
```

This will test:
- Environment variables
- Package installation
- OpenAI TTS generation
- Audio playback methods
- Fallback TTS system

## API Endpoints

The web interface provides REST API endpoints:

- `POST /api/new_inquiry` - Create new student inquiry
- `POST /api/chat` - Send message to student
- `GET /api/followup/<student_id>` - Generate follow-up message
- `GET /api/dashboard` - Get dashboard metrics
- `GET /api/export` - Export all student data
- `GET /api/students` - Get all students

## CLI Commands

- Type **"exit"**, **"quit"**, **"stop"**, or **"end"** to exit conversations
- Voice output provides audio feedback for agent responses

## Quick Start Commands

```bash
# 1. Activate environment
cd "/home/akrati/Desktop/RAG Chatbot"
source venv/bin/activate

# 2. Quick health check
python3 test_voice.py

# 3. Start web interface (default)
./run.sh
# Then visit: http://localhost:5000

# 4. Start CLI interface
./run.sh --cli
```

## Detailed Testing

### Test Web Interface (Default):
```bash
source venv/bin/activate
python3 main.py
# Open http://localhost:5000
```

### Test CLI Interface:
```bash
source venv/bin/activate
python3 main.py --cli
```

### Run System Diagnostics:
```bash
source venv/bin/activate
python3 test_voice.py
```

This will test:
- Environment variables
- Package installation
- OpenAI TTS generation
- Audio playback methods
- Fallback TTS system

