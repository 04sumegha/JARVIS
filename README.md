# JARVIS

JARVIS is a voice-controlled AI assistant that listens for wake words, transcribes speech to text, processes commands via a large language model (LLM), executes actions, and responds via text-to-speech.

## Features

- **Wake-Word Detection**: Uses PicoVoice Porcupine to detect the wake word "Hey Jarvis" and start listening for commands.
- **Speech-to-Text**: Transcribes recorded audio using PicoVoice Leopard.
- **LLM Integration**: Processes transcribed text with Groq's Llama model to understand intent and select actions.
- **Tool Execution**: Supports various tools like screen brightness control.
- **Text-to-Speech**: Speaks responses using PicoVoice Orca.
- **Modes**: Run in wake-word mode (voice interaction) or CLI mode (text input).

## Prerequisites

- Python 3.8+
- PicoVoice account for access keys (Porcupine, Leopard, Orca)
- Groq API key

## Installation

1. **Clone the repository**:
   ```bash
   git clone <REPO_URL>
   cd JARVIS
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root with:
   ```
   API_KEY=your_groq_api_key_here
   PICOVOICE_ACCESS_KEY=your_picovoice_access_key_here
   ```

## Usage

### Wake-Word Mode (Default)
Run the assistant in voice mode:
```bash
python main.py
```
- Say "Hey Jarvis" to wake the assistant.
- Speak your command (e.g., "increase brightness").
- The assistant will transcribe, process, execute, and speak the response.

### CLI Mode
Run in text input mode for testing:
```bash
python main.py --mode cli
```
Type commands like "increase brightness" and press Enter.

### Additional Options
- `--wav-path`: Specify path to save recorded audio (default: `command.wav`).
- `--picovoice-key`: Override PicoVoice key (not recommended for security).

## Project Structure

```
JARVIS/
├── config.py              # Environment variable configuration
├── main.py                # Main entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── llm/                   # LLM integration
│   ├── client.py
│   ├── intent_recognition.py
│   └── tool_service.py
├── services/              # Core services
│   └── keyboard.py        # Tool implementations
├── src/                   # Audio processing modules
│   ├── wake_word.py       # Wake-word detection
│   ├── speech_to_text.py  # Speech-to-text
│   └── text_to_speech.py  # Text-to-speech
└── scripts/               # Utility scripts
    └── start_jarvis.bat   # Windows launcher
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
