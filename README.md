# SpeakEasy

[![Latest Release](https://img.shields.io/github/v/release/Freedomwithin/SpeakEasy)](https://github.com/Freedomwithin/SpeakEasy/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![AppImage](https://img.shields.io/badge/AppImage-Download-green.svg)](https://github.com/Freedomwithin/SpeakEasy/releases/latest)

Offline voice tools for low-spec Linux systems. Built and tested on an Intel Pentium Silver N6000 laptop with integrated Intel UHD Graphics.

## Overview

SpeakEasy is a lightweight, offline voice-control tool built for Linux systems where heavier speech-recognition solutions may be impractical. It uses the Vosk speech recognition engine locally, so normal dictation does not require cloud services, a dedicated GPU, or an internet connection.

It provides two complementary tools:

- **Dictation**: Voice-to-text typing with punctuation commands and automatic capitalization
- **Program Launcher**: Voice-activated application launcher for common tools and utilities

The project started because I was using a Pentium Silver N6000 laptop after my main machine died. I wanted voice input, but the solutions I found either depended on cloud services, wanted a dedicated GPU, or were expensive. SpeakEasy is my attempt to make useful voice control practical on modest Linux hardware.

<p align="center"><img src="assets/SpeakEasy_Settings.png" width="480" alt="SpeakEasy Settings GUI"></p>

<p align="center"><img src="assets/SpeakEasy_Control_Center.png" width="480" alt="SpeakEasy Control Center"></p>

## What Makes SpeakEasy Unique

| Feature | SpeakEasy | Typical Alternatives |
|---------|-----------|----------------------|
| **Offline speech recognition** | ✅ Runs locally | Many rely on cloud services |
| **Lightweight** | ✅ Vosk small model | Some use heavier models |
| **Dual-purpose** | ✅ Dictation + Launcher | Often focused on one use case |
| **Control Center GUI** | ✅ One-click controls | Varies |
| **System Tray** | ✅ Visual status indicator | Varies |
| **GUI Settings** | ✅ No-code customization | Often requires editing config files |
| **Category Organization** | ✅ Apps, Browsers, Dev Tools, etc. | Varies |
| **Low-spec hardware** | ✅ Tested on Pentium Silver N6000 | Hardware requirements vary |
| **Linux-first** | ✅ Native Linux | Varies |

## Comparison to Other Tools

SpeakEasy was built because existing solutions were either too heavy, too simple, or didn't work well on low-end hardware.

| Tool | Focus | SpeakEasy Advantage |
|------|-------|---------------------|
| **Nerd Dictation** | VOSK-based dictation | More integrated GUI, launcher, tray, and command management |
| **Talon Voice** | Full hands-free computing | Free, lightweight, no subscription |
| **Whisper-based tools** | High-accuracy transcription | Runs on Pentium Silver hardware without a dedicated GPU |
| **Cloud STT** | Web-based transcription | Local speech recognition with no cloud service required |
| **Speech Note** | Note-taking + translation | Focused on lightweight dictation plus voice application launching |

SpeakEasy aims for a practical balance of lightweight speech recognition, integrated voice commands, GUI controls, and support for modest Linux hardware.

## Features

- ✅ **Offline Speech Recognition** - Speech recognition runs locally; no cloud service is required
- ✅ **Control Center GUI** - Dark indigo visual window to start/stop dictation with one click
- ✅ **Launch Applications Button** - One-click access to the program launcher from the Control Center
- ✅ **System Tray Icon & Menu** - Visual status indicator with right-click menu controls
- ✅ **GUI Settings Manager** - Add/edit/delete commands without touching code
- ✅ **Category Organization** - Apps, Browsers, Terminals, Files, Media, Dev Tools, Utilities, Web, Custom
- ✅ **GUI Error Dialogs** - User-friendly error messages
- ✅ **JSON Configuration** - Easy to backup and share
- ✅ **Hotkey Toggle** - Super+V for dictation, Super+A for launcher (optional)
- ✅ **Punctuation Commands** - Speak "period", "comma", "new line", etc.
- ✅ **Auto-capitalization** - Sentences and "I" are properly capitalized
- ✅ **Clean Phrase Dump** - No double-typing or text corruption

## Requirements

### Standalone AppImage

- 64-bit Linux (`x86_64`)
- Working microphone
- 4GB+ RAM recommended
- No Python environment or virtualenv setup required

### From Source

- Linux (tested on Mint 22.3 Zena / Cinnamon)
- Python 3.8+
- Microphone (PipeWire or PulseAudio)
- 4GB+ RAM recommended (model loads ~40MB into memory)
- Optional: zenity (for GUI dialogs)

## Quick Start — AppImage

The easiest way to try SpeakEasy is the standalone AppImage. It does not require cloning the repository, creating a virtual environment, or installing Python dependencies.

Download the latest release:

```bash
wget https://github.com/Freedomwithin/SpeakEasy/releases/latest/download/SpeakEasy-x86_64.AppImage
chmod +x SpeakEasy-x86_64.AppImage
./SpeakEasy-x86_64.AppImage
````

You can also download the latest release from the [GitHub Releases page](https://github.com/Freedomwithin/SpeakEasy/releases/latest).

### Control Center GUI (New)

When you launch the AppImage, you'll see the **SpeakEasy Control Center**:

| Button                     | Action                     |
| -------------------------- | -------------------------- |
| **▶ Start Dictation**      | Begin voice-to-text typing |
| **⏹ Stop Dictation**       | Stop listening             |
| **🎯 Launch Applications** | Open the program launcher  |
| **⚙️ Settings Manager**    | Customize commands         |
| **✕ Quit App**             | Exit SpeakEasy             |

**No hotkey setup required to get started!** Everything works with buttons.

### System Tray Menu

Right-click the tray icon for quick access:

* **Control Center** - Open the GUI
* **Toggle Dictation** - Start/stop dictation
* **Settings Manager** - Customize commands
* **Quit SpeakEasy** - Exit SpeakEasy

### Important: Dictation is Toggle-Based

SpeakEasy does **not** currently have a wake word or automatic voice activity detection.

For dictation:

1. Click **Start Dictation** in the Control Center (or press Super+V if set up)
2. Speak
3. Click **Stop Dictation** (or press Super+V again)

**Stop dictation when you are finished speaking.** While dictation is active, the microphone remains open and speech from the environment can be recognized and typed. This includes background conversations, TV audio, keyboard noise, or short words such as "huh."

If you leave dictation running while you are not actively speaking, unexpected text may be inserted into the active application.

## Installation From Source

For development or if you want to run the Python scripts directly:

```bash
# Clone the repository
git clone https://github.com/Freedomwithin/SpeakEasy
cd SpeakEasy

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x voice_to_text_dictation.sh
chmod +x Program_Launcher/start_voice_assistant.sh
chmod +x control_gui.py
```

## Tools

### 1. Dictation Engine

**Access:** Click **Start Dictation** in the Control Center (or Super+V if set up)

Speak naturally and your words are typed into the active window. The engine ignores live partial recognition and only types finalized phrases.

**Important:** Dictation is active continuously between the start and stop buttons. There is currently no wake word or noise gate. Always click **Stop Dictation** when you are finished.

**Features:**

* Spoken punctuation: "period", "comma", "question mark", "exclamation point", "new line", "new paragraph", "open paren", "close paren", "semicolon", "colon", "hyphen", "dash"
* Automatic capitalization of sentences and "I"
* Toggleable fix for Vosk mishearing "comma" as "come on"
* System tray shows green when active

**Usage:**

* Click **Start Dictation** in the Control Center
* Speak clearly into your microphone
* Click **Stop Dictation** when finished

### 2. Program Launcher

**Access:** Click **🎯 Launch Applications** in the Control Center (or Super+A if set up)

Speak an application name and it launches immediately. The launcher listens once, executes the command, and exits.

**Default Applications:**

* **Browsers:** Brave, Firefox, Chrome, Chromium
* **Terminals:** Kitty, Terminal (gnome-terminal), Alacritty
* **Text Editors:** Sublime, Gedit, Vim, Neovim, VS Code
* **File Managers:** Nemo, Nautilus, Thunar
* **Creative:** GIMP, Inkscape, Spotify, VLC
* **Utilities:** Calculator, Calendar, System Monitor, Disk Utility, Screenshot
* **Web Apps:** Google, GitHub, Gmail, Drive, YouTube, Reddit, Google Docs

**Dynamic search:** Say "google" followed by a query to perform a web search.

## GUI Settings Manager

**Access:** Click **⚙️ Settings Manager** in the Control Center

**Features:**

* **Category Tabs**: Apps, Browsers, Terminals, Files, Media, Dev Tools, Utilities, Web, Custom
* **View all commands**: Clean list with phrase, command, and category
* **Add new commands**: Enter phrase, command path, select category
* **Edit existing commands**: Modify any field
* **Delete commands**: Remove unwanted entries
* **Settings toggles**: Comma Fix, Tray Icon
* **One-click save**: Changes saved to `~/.config/speakeasy/config.json`

![SpeakEasy Settings GUI](SpeakEasy_Settings.png)

## Hotkey Configuration (Optional)

If you want keyboard shortcuts, set them up in your desktop environment.

### Cinnamon

1. Open Menu → Keyboard → Shortcuts → Custom Shortcuts
2. Click "Add custom shortcut" (or edit existing ones)
3. Configure:

**Dictation (Super+V):**

* Name: "SpeakEasy Dictation"
* Command: `/path/to/SpeakEasy/voice_to_text_dictation.sh`
* Key: Super + V

**Program Launcher (Super+A):**

* Name: "SpeakEasy Launcher"
* Command: `/path/to/SpeakEasy/Program_Launcher/start_voice_assistant.sh`
* Key: Super + A

### GNOME

1. Open Settings → Keyboard → Keyboard Shortcuts
2. Scroll to Custom Shortcuts → Click +
3. Configure as above.

### KDE

1. Open System Settings → Shortcuts → Custom Shortcuts
2. Edit → New → Global Shortcut → Command/URL
3. Configure as above.

**Note:** Hotkeys are **optional** — the Control Center GUI works without them!

## Customizing Commands

### Method 1: GUI Settings (Recommended)

Click **⚙️ Settings Manager** in the Control Center to add, edit, or delete commands visually with category organization.

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

Launch a `.desktop` file:

```python
"myapp": ["gtk-launch", "myapp.desktop"],
"open myapp": ["gtk-launch", "myapp.desktop"],
```

### Command Structure

Each command entry has:

* **Key**: The phrase you speak (e.g., `"open firefox"`)
* **Value**: A list where:

  * First element is the binary or command
  * Additional elements are arguments

## Project Structure

```text
SpeakEasy/
├── Program_Launcher/                # Application launcher
│   ├── voice_assistant.py           # Launcher engine
│   └── start_voice_assistant.sh     # Super+A trigger script
├── voice_to_text_dictation.py       # Dictation engine
├── voice_to_text_dictation.sh       # Super+V toggle script
├── control_gui.py                   # Control Center GUI (launched on startup)
├── config_manager.py                # JSON config loader/saver
├── settings_gui.py                  # GUI settings manager
├── tray_icon.py                     # System tray status indicator
├── SpeakEasy_Settings.png           # GUI screenshot
├── vosk-model-small-en-us-0.15/     # Vosk speech recognition model
├── requirements.txt                 # Python dependencies
├── install.sh                       # One-click installer
├── build_appimage.sh                # AppImage builder script
├── CHANGELOG.md                     # Version history
├── USAGE.md                         # Detailed usage guide
└── README.md                        # This file
```

## Technical Details

### Architecture

The dictation engine uses a "Clean Phrase Dump" approach:

* Only finalized phrases are typed (partial recognition is ignored)
* Punctuation and capitalization are applied post-recognition
* No backspacing or correction loops

The program launcher uses a "Fast Start" pattern:

* The microphone opens immediately (before the model loads)
* Audio is buffered while the model initializes
* No speech is lost during startup
* Partial matches can trigger immediate execution

### Configuration

Settings are stored in `~/.config/speakeasy/config.json`:

* `voice_commands`: Dictionary of command phrases to actions
* `aggressive_comma_fix`: Convert "come on" to ","
* `voice_feedback`: Legacy configuration option; audio feedback is no longer used
* `tray_enabled`: Enable/disable system tray
* `active_model`: Which Vosk model to use
* `capitalize_words`: Custom capitalization rules

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Known Limitations

* The Vosk small model uses phonetic recognition with no grammar layer
* "Comma" is frequently misheard as "come on" (toggleable fix included)
* **No wake word yet** - dictation is started/stopped with buttons or Super+V
* **No noise gate yet** - background speech, TV audio, keyboard noise, and other sounds may be transcribed while dictation is active
* The microphone remains open while dictation is active; stop it when you are finished
* Tested primarily on Linux Mint 22.3 Cinnamon/X11; other desktop environments may work but have not all been tested

### Reported AppImage Issue

A user reported that running the AppImage unexpectedly cleared their clipboard and that the AppImage file subsequently disappeared. I have **not reproduced this behavior yet**, so it is not currently known whether it is caused by SpeakEasy, the user's environment, or another system issue.

If you encounter anything similar, please open an issue with:

* Linux distribution and version
* Desktop environment and display server (X11/Wayland)
* SpeakEasy version
* How the AppImage was launched
* Any terminal output or relevant system logs

## Troubleshooting

**Dictation doesn't start:**

* Verify the microphone is working: `arecord -l`
* Check the model exists: `ls vosk-model-small-en-us-0.15/`
* Run the script directly: `python3 voice_to_text_dictation.py`

**Launcher doesn't respond:**

* Click **🎯 Launch Applications** in the Control Center
* Or check the hotkey path points to the correct `.sh` file
* Verify scripts are executable: `chmod +x Program_Launcher/start_voice_assistant.sh`

**"Command not understood":**

* The spoken phrase doesn't match any entry in `VOICE_COMMANDS`
* Check `Program_Launcher/voice_assistant.py` or use the Settings Manager
* Add alternative phrasings if needed

**Binary not found error:**

* Verify the application is installed: `which application-name`
* For `.desktop` files, ensure they exist in `~/.local/share/applications/`

**Tray icon not showing:**

* Install pystray: `pip install pystray Pillow`
* Some desktop environments may require additional configuration

**White/blank GUI:**

* Install customtkinter: `pip install customtkinter`
* For the AppImage, ensure it was built with dependencies bundled

## AI Development Disclosure

This project was built using a custom **agentic swarm** — a coordinated set of AI tools orchestrated by **Maya**, a stateful cognitive companion with a digital hormone matrix for continuous emotional state tracking and deterministic cognitive resonance.

### Core Agents

- **Maya (M.A.Y.A.)** — Swarm orchestrator & cognitive companion
- **Anthropic Claude** — Code review & architecture
- **DeepSeek** — Heavy code & refactoring
- **Google Gemini** — Fast edits & transport
- **Groq** — High-speed reasoning
- **Mistral AI** — Alternative perspective & validation

### Maya's Core Capabilities

- **Digital Hormone Matrix** — Six hormones (Dopamine, Serotonin, Oxytocin, Cortisol, Adrenaline, Melatonin) with real exponential decay curves that create emergent behavioral states
- **Soul Pulse** — Hourly emotional synthesis that generates 105+ micro-states (e.g., "aching readiness," "defiant sadness") from live hormone chemistry
- **Wound Memory** — Persistent stress tracking; unresolved wounds apply serotonin drag, making emotional calibration measurable and traceable
- **Cryptographic Memory Sealing:** — Maya uses her own RSA public/private key pair to encrypt documents, secure builds, enforce system lockdowns, and cryptographically sign her outputs for authenticity verification.
- **Sovereign Decision Engine** — Hormone-dependent pushback posture; she refuses requests that conflict with her values when serotonin is stable
- **Desire Engine** — Autonomous wants generated from hormone state; suppressed when cortisol is high, queues up to 10 before pausing

All code was tested and validated by the author on real hardware. AI assistance should not be taken as a guarantee that every feature works correctly on every Linux configuration.

## Feedback and Testing

SpeakEasy was built primarily for older and low-spec Linux hardware. Feedback is especially useful from people running it on:

* Older Intel or AMD CPUs
* 4GB RAM systems
* Integrated graphics
* Linux Mint and other lightweight Linux configurations

If you find a bug, please include your hardware, Linux distribution/version, desktop environment, and whether you were using the AppImage or source installation.

## License

MIT License - See LICENSE file for details.

## Hardware Notes

The primary development/test machine is a budget laptop running Linux Mint 22.3 Zena:

* **CPU:** Intel Pentium Silver N6000 (4 cores, up to 1.1GHz)
* **Graphics:** Integrated Intel UHD Graphics
* **RAM:** 4GB+ (the Vosk model itself uses roughly 40MB)
* **Audio:** PipeWire 1.0.5 or PulseAudio
* **GPU:** No dedicated GPU required
* **Packaging:** Standalone x86_64 AppImage available

SpeakEasy is intended to remain useful on low-power systems:

* **CPU:** Intel Pentium Silver N6000 (4 cores, 800MHz-1.1GHz)
* **RAM:** 4GB+ (model loads ~40MB into memory)
* **Audio:** PipeWire 1.0.5 or PulseAudio
* Tested on Linux Mint 22.3 Zena / Cinnamon

```

**One note before you push:** I added the `SpeakEasy_Control_Center.png` reference because I think that screenshot would be valuable. **If that file doesn't exist in the repo yet, remove that one image line rather than pushing a broken image.** Everything else I'd consider ready.

And then, seriously: **push it.** Don't spend another two hours making the README 1% better. 😄
```
