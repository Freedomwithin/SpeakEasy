# SpeakEasy

Offline voice tools for low-spec Linux systems. Built for Intel Pentium Silver N6000 and similar CPUs.

## Overview

SpeakEasy provides two complementary voice-controlled tools that run entirely offline using the Vosk speech recognition engine. No cloud services, no GPU requirements, no network dependency.

- **Dictation**: Voice-to-text typing with punctuation commands and automatic capitalization
- **Program Launcher**: Voice-activated application launcher for common tools and utilities

## Requirements

- Linux (tested on Mint 22.3 Zena / Cinnamon)
- Python 3.8+
- 20GB RAM recommended (model loads into memory)
- Microphone (PipeWire or PulseAudio)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/SpeakEasy
cd SpeakEasy

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x voice_to_text_dictation.sh
chmod +x Program_Launcher/start_voice_assistant.sh
```

The Vosk model (`vosk-model-small-en-us-0.15`) is included in the repository.

## Tools

### 1. Dictation Engine

**Hotkey:** Super + V

Speak naturally and your words are typed into the active window. The engine ignores live partial recognition and only types finalized phrases, eliminating the double-typing and race conditions found in earlier versions.

**Features:**
- Spoken punctuation: "period", "comma", "question mark", "exclamation point", "new line", "new paragraph", "open paren", "close paren", "semicolon", "colon", "hyphen", "dash"
- Automatic capitalization of sentences and "I"
- Custom capitalization for proper nouns (e.g., "Jonathon")
- Toggleable fix for Vosk mishearing "comma" as "come on"

**Usage:**
- Press Super + V to start dictation
- Speak clearly into your microphone
- Press Super + V again to stop

**File:** `voice_to_text_dictation.py`

### 2. Program Launcher

**Hotkey:** Super + A

Speak an application name and it launches immediately. The launcher listens once, executes the command, and exits. This one-shot design prevents the microphone from staying open unnecessarily.

**Supported applications:**
- Base: `sublime`, `brave`, `kitty`, `nemo`, `files`
- AI Tools: `claude`, `deep seek`, `gemini`
- Security: `proxy`, `burp`
- Ecosystem: `anti gravity`, `glyph`, `swarm hub`, `neural dashboard`, `scratch pad`, `vault`, `call maya`
- General: `calendar`, `gimp`, `spotify`, `youtube downloader`

**Dynamic search:** Say "google" followed by a query to perform a web search (e.g., "google linux kernel architecture").

**Usage:**
- Press Super + A
- Speak the application name or command
- The application launches and the listener exits

**Files:** `Program_Launcher/voice_assistant.py` and `start_voice_assistant.sh`

## Hotkey Configuration (Cinnamon)

1. Open Menu → Keyboard → Shortcuts → Custom Shortcuts
2. Click "Add custom shortcut" (or edit existing ones)
3. Configure:
   - **Dictation:** Name: "SpeakEasy Dictation", Command: full path to `voice_to_text_dictation.sh`, Key: Super + V
   - **Launcher:** Name: "SpeakEasy Launcher", Command: full path to `Program_Launcher/start_voice_assistant.sh`, Key: Super + A

## Project Structure

```
SpeakEasy/
├── Program_Launcher/                # Application launcher
│   ├── voice_assistant.py           # Launcher engine
│   └── start_voice_assistant.sh     # Super+A trigger script
├── voice_to_text_dictation.py       # Dictation engine
├── voice_to_text_dictation.sh       # Super+V toggle script
├── vosk-model-small-en-us-0.15/     # Vosk speech recognition model
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Technical Details

### Architecture

The dictation engine uses a "Clean Phrase Dump" approach:
- Only finalized phrases are typed (partial recognition is ignored)
- Punctuation and capitalization are applied post-recognition
- No backspacing or correction loops, eliminating text corruption

The program launcher uses a "Fast Start" pattern:
- The microphone opens immediately (before the model loads)
- Audio is buffered while the model initializes
- No speech is lost during startup
- Partial matches can trigger immediate execution

### Version History

| Version | Dictation Approach | Status |
|---------|-------------------|--------|
| V3.1 | Live partial tracking | Unstable - race conditions |
| V3.2 | Word-history + backspacing | Unstable - text corruption |
| V3.3 | Clean phrase dump | Stable, no formatting |
| V3.4 | Clean dump + basic regex | Stable, basic punctuation |
| V3.5 | Clean dump + expanded grammar | Stable, full punctuation/capitalization |
| V3.6 | Clean dump + grammar + fixes | Current stable release |

## Known Limitations

- The Vosk small model uses phonetic recognition with no grammar layer
- "Comma" is frequently misheard as "come on" (toggleable fix included)
- No wake word or noise gate - the microphone stays open when active
- Background noise may be transcribed (stop dictation when not in use)

## Adding Custom Commands

### Dictation Corrections

Edit `PUNCTUATION_COMMANDS` in `voice_to_text_dictation.py` to add new spoken commands or phonetic fixes. Multi-word rules should be placed before single-word rules.

### Application Launcher Commands

Edit `VOICE_COMMANDS` in `Program_Launcher/voice_assistant.py`. Add both the bare phrase and "open ___" variant for flexibility:

```python
"application": ["binary-name"],
"open application": ["binary-name"],
```

For .desktop files, use `"gtk-launch"` as the binary and the `.desktop` filename as the second argument.

## Troubleshooting

**Dictation doesn't start:**
- Verify the microphone is working: `arecord -l`
- Check the model exists: `ls vosk-model-small-en-us-0.15/`
- Run the script directly to see errors: `python3 voice_to_text_dictation.py`

**Launcher doesn't respond:**
- Check the hotkey path points to the correct `.sh` file
- Verify scripts are executable: `chmod +x Program_Launcher/start_voice_assistant.sh`
- Check logs: `tail -f /tmp/voice_assistant.log`

**"Command not understood":**
- The spoken phrase doesn't match any entry in `VOICE_COMMANDS`
- Check `Program_Launcher/voice_assistant.py` for the exact phrasing
- Add alternative phrasings if needed

## License

MIT License - See LICENSE file for details.

## Hardware Notes

SpeakEasy is optimized for low-power systems:
- **CPU:** Intel Pentium Silver N6000 (4 cores, 800MHz-1.1GHz)
- **RAM:** 20GB (model preloaded into memory)
- **Audio:** PipeWire 1.0.5 or PulseAudio
- Tested on Linux Mint 22.3 Zena / Cinnamon
