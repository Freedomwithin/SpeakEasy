# SpeakEasy

[![Latest Release](https://img.shields.io/github/v/release/Freedomwithin/SpeakEasy)](https://github.com/Freedomwithin/SpeakEasy/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![AppImage](https://img.shields.io/badge/AppImage-Download-green.svg)](https://github.com/Freedomwithin/SpeakEasy/releases/latest)

Offline voice tools for low-spec Linux systems. Built for Intel Pentium Silver N6000 and similar CPUs.

## Overview

SpeakEasy provides two complementary voice-controlled tools that run entirely offline using the Vosk speech recognition engine. No cloud services, no GPU requirements, no network dependency.

- **Dictation**: Voice-to-text typing with punctuation commands and automatic capitalization
- **Program Launcher**: Voice-activated application launcher for common tools and utilities

![SpeakEasy Settings GUI](SpeakEasy_Settings.png)

## What Makes SpeakEasy Unique

| Feature | SpeakEasy | Most Alternatives |
|---------|-----------|-------------------|
| **Offline-first** | ✅ 100% local | Mixed — many require cloud |
| **VOSK lightweight** | ✅ Optimized for low-spec | Often use heavier Whisper models |
| **Dual-purpose** | ✅ Dictation + Launcher | Usually one or the other |
| **Hotkey toggles** | ✅ Super+V / Super+A | Often require GUI or always-on |
| **Clean Phrase Dump** | ✅ No double-typing | Many tools struggle with this |
| **System Tray** | ✅ Visual status indicator | Most lack this |
| **GUI Settings** | ✅ No-code customization | Requires editing config files |
| **Voice Feedback** | ✅ Audio confirmations | Silent or terminal-only |
| **Category Organization** | ✅ Apps, Browsers, Dev Tools, etc. | Flat, unorganized lists |
| **Pentium Silver N6000** | ✅ Tested and working | Most assume modern hardware |
| **Linux-first** | ✅ Native Linux | Often Windows/Mac first |

## Comparison to Other Tools

SpeakEasy was built because existing solutions were either too heavy, too simple, or didn't work well on low-end hardware.

| Tool | Focus | SpeakEasy Advantage |
|------|-------|---------------------|
| **Nerd Dictation** | VOSK-based dictation | More polished, easier setup, includes launcher, tray, GUI with categories |
| **Talon Voice** | Full hands-free computing | Free, lighter, no subscription |
| **Whisper-based tools** | High-accuracy transcription | Runs on Pentium Silver, no GPU needed |
| **Cloud STT** | Web-based transcription | 100% offline, privacy-first |
| **Speech Note** | Note-taking + translation | Simpler, dual-purpose (dictation + launcher) |

SpeakEasy hits the sweet spot: lightweight, dual-purpose, hotkey-driven, and actually tested on low-end hardware.

## Features

- ✅ **100% Offline** - No cloud, no data sent anywhere
- ✅ **System Tray Icon** - Green/red status indicator
- ✅ **GUI Settings Manager** - Add/edit/delete commands without touching code
- ✅ **Category Organization** - Apps, Browsers, Terminals, Files, Media, Dev Tools, Utilities, Web, Custom
- ✅ **Voice Feedback** - Audio confirmations for actions
- ✅ **GUI Error Dialogs** - User-friendly error messages
- ✅ **JSON Configuration** - Easy to backup and share
- ✅ **Hotkey Toggle** - Super+V for dictation, Super+A for launcher
- ✅ **Punctuation Commands** - Speak "period", "comma", "new line", etc.
- ✅ **Auto-capitalization** - Sentences and "I" are properly capitalized
- ✅ **Clean Phrase Dump** - No double-typing or text corruption

## Requirements

- Linux (tested on Mint 22.3 Zena / Cinnamon)
- Python 3.8+
- Microphone (PipeWire or PulseAudio)
- 4GB+ RAM recommended (model loads ~40MB into memory)
- Optional: espeak (for voice feedback), zenity (for GUI dialogs)

## Quick Install

```bash
git clone https://github.com/Freedomwithin/SpeakEasy
cd SpeakEasy
./install.sh
```

The install script will:
- Create a Python virtual environment
- Install all dependencies
- Check for optional packages (espeak, zenity)
- Make scripts executable
- Verify the Vosk model is present

## Manual Installation

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x voice_to_text_dictation.sh
chmod +x Program_Launcher/start_voice_assistant.sh
```

## Tools

### 1. Dictation Engine

**Hotkey:** Super + V

Speak naturally and your words are typed into the active window. The engine ignores live partial recognition and only types finalized phrases.

**Features:**
- Spoken punctuation: "period", "comma", "question mark", "exclamation point", "new line", "new paragraph", "open paren", "close paren", "semicolon", "colon", "hyphen", "dash"
- Automatic capitalization of sentences and "I"
- Toggleable fix for Vosk mishearing "comma" as "come on"
- System tray shows green when active
- Voice confirmation: "Dictation started" / "Dictation stopped"

**Usage:**
- Press Super + V to start dictation
- Speak clearly into your microphone
- Press Super + V again to stop

### 2. Program Launcher

**Hotkey:** Super + A

Speak an application name and it launches immediately. The launcher listens once, executes the command, and exits.

**Default Applications:**
- `sublime` - Sublime Text editor
- `brave` - Brave Browser
- `kitty` - Kitty terminal
- `nemo` - Nemo file manager
- `files` - Nemo file manager (alias)
- `firefox` - Firefox Browser
- `gimp` - GIMP image editor
- `spotify` - Spotify (if installed)

**Dynamic search:** Say "google" followed by a query to perform a web search (e.g., "google linux kernel architecture").

## GUI Settings Manager

Launch the GUI settings manager:

```bash
python3 settings_gui.py
```

**Features:**
- **Category Tabs**: Apps, Browsers, Terminals, Files, Media, Dev Tools, Utilities, Web, Custom
- **View all commands**: Clean list with phrase, command, and category
- **Add new commands**: Enter phrase, command path, select category
- **Edit existing commands**: Modify any field
- **Delete commands**: Remove unwanted entries
- **Settings toggles**: Voice Feedback, Comma Fix, Tray Icon
- **One-click save**: Changes saved to `~/.config/speakeasy/config.json`

![SpeakEasy Settings GUI](SpeakEasy_Settings.png)

## Hotkey Configuration (Cinnamon)

1. Open Menu → Keyboard → Shortcuts → Custom Shortcuts
2. Click "Add custom shortcut" (or edit existing ones)
3. Configure:

**Dictation (Super+V):**
- Name: "SpeakEasy Dictation"
- Command: `/home/username/Software/Github/SpeakEasy/voice_to_text_dictation.sh`
- Key: Super + V

**Program Launcher (Super+A):**
- Name: "SpeakEasy Launcher"
- Command: `/home/username/Software/Github/SpeakEasy/Program_Launcher/start_voice_assistant.sh`
- Key: Super + A

*Replace `/home/username/Software/Github/SpeakEasy/` with the actual path where you cloned the repository.*

## Customizing Commands

### Method 1: GUI Settings (Recommended)

Run `python3 settings_gui.py` to add, edit, or delete commands visually with category organization.

### Method 2: Edit Config File

Edit `~/.config/speakeasy/config.json` directly:

```json
{
  "voice_commands": {
    "myapp": ["/path/to/application"],
    "open myapp": ["/path/to/application"]
  }
}
```

### Method 3: Edit Python File

Edit `Program_Launcher/voice_assistant.py` and find the `VOICE_COMMANDS` dictionary.

**Examples:**

Open a folder in Nemo:
```python
"projects": ["nemo", "/home/username/projects"],
"open projects": ["nemo", "/home/username/projects"],
```

Open a config file in Sublime:
```python
"config": ["subl", "/home/username/.config/app/config.conf"],
"open config": ["subl", "/home/username/.config/app/config.conf"],
```

Open a website:
```python
"docs": ["xdg-open", "https://docs.example.com"],
"open docs": ["xdg-open", "https://docs.example.com"],
```

Launch a .desktop file:
```python
"myapp": ["gtk-launch", "myapp.desktop"],
"open myapp": ["gtk-launch", "myapp.desktop"],
```

### Command Structure

Each command entry has:
- **Key**: The phrase you speak (e.g., `"open firefox"`)
- **Value**: A list where:
  - First element is the binary or command
  - Additional elements are arguments

## Project Structure

```
SpeakEasy/
├── Program_Launcher/                # Application launcher
│   ├── voice_assistant.py           # Launcher engine
│   └── start_voice_assistant.sh     # Super+A trigger script
├── voice_to_text_dictation.py       # Dictation engine
├── voice_to_text_dictation.sh       # Super+V toggle script
├── config_manager.py                # JSON config loader/saver
├── settings_gui.py                  # GUI settings manager
├── tray_icon.py                     # System tray status indicator
├── SpeakEasy_Settings.png           # GUI screenshot
├── vosk-model-small-en-us-0.15/     # Vosk speech recognition model
├── requirements.txt                 # Python dependencies
├── install.sh                       # One-click installer
├── CHANGELOG.md                     # Version history
└── README.md                        # This file
```

## Technical Details

### Architecture

The dictation engine uses a "Clean Phrase Dump" approach:
- Only finalized phrases are typed (partial recognition is ignored)
- Punctuation and capitalization are applied post-recognition
- No backspacing or correction loops

The program launcher uses a "Fast Start" pattern:
- The microphone opens immediately (before the model loads)
- Audio is buffered while the model initializes
- No speech is lost during startup
- Partial matches can trigger immediate execution

### Configuration

Settings are stored in `~/.config/speakeasy/config.json`:
- `voice_commands`: Dictionary of command phrases to actions
- `aggressive_comma_fix`: Convert "come on" to ","
- `voice_feedback`: Enable/disable audio feedback
- `tray_enabled`: Enable/disable system tray
- `active_model`: Which Vosk model to use
- `capitalize_words`: Custom capitalization rules

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Known Limitations

- The Vosk small model uses phonetic recognition with no grammar layer
- "Comma" is frequently misheard as "come on" (toggleable fix included)
- No wake word or noise gate - the microphone stays open when active
- Background noise may be transcribed (stop dictation when not in use)
- Voice feedback requires espeak or spd-say installed

## Troubleshooting

**Dictation doesn't start:**
- Verify the microphone is working: `arecord -l`
- Check the model exists: `ls vosk-model-small-en-us-0.15/`
- Run the script directly: `python3 voice_to_text_dictation.py`

**Launcher doesn't respond:**
- Check the hotkey path points to the correct `.sh` file
- Verify scripts are executable: `chmod +x Program_Launcher/start_voice_assistant.sh`

**"Command not understood":**
- The spoken phrase doesn't match any entry in `VOICE_COMMANDS`
- Check `Program_Launcher/voice_assistant.py` or use `settings_gui.py`
- Add alternative phrasings if needed

**Binary not found error:**
- Verify the application is installed: `which application-name`
- For `.desktop` files, ensure they exist in `~/.local/share/applications/`

**Tray icon not showing:**
- Install pystray: `pip install pystray Pillow`
- Some desktop environments may require additional configuration

**Voice feedback not working:**
- Install espeak: `sudo apt install espeak`
- Or spd-say: `sudo apt install speech-dispatcher`

## License

MIT License - See LICENSE file for details.

## Hardware Notes

SpeakEasy is optimized for low-power systems:
- **CPU:** Intel Pentium Silver N6000 (4 cores, 800MHz-1.1GHz)
- **RAM:** 4GB+ (model loads ~40MB into memory)
- **Audio:** PipeWire 1.0.5 or PulseAudio
- Tested on Linux Mint 22.3 Zena / Cinnamon