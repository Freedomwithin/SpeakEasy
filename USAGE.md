# SpeakEasy Usage Guide

## Quick Start

### AppImage (Recommended)

```bash
# Download the AppImage
wget https://github.com/Freedomwithin/SpeakEasy/releases/latest/download/SpeakEasy-x86_64.AppImage
chmod +x SpeakEasy-x86_64.AppImage
./SpeakEasy-x86_64.AppImage
```

The **Control Center GUI** will open automatically.

### From Source

```bash
git clone https://github.com/Freedomwithin/SpeakEasy
cd SpeakEasy
./install.sh
```

## Control Center GUI

When you launch SpeakEasy, you'll see a dark indigo window with:

| Button | Action |
|--------|--------|
| **▶ Start Dictation** | Begin voice-to-text typing |
| **⏹ Stop Dictation** | Stop listening |
| **🎯 Launch Applications** | Open the program launcher |
| **⚙️ Settings Manager** | Customize commands |
| **✕ Quit App** | Exit SpeakEasy |

### System Tray Menu

Right-click the tray icon for quick access:
- **Control Center** - Open the GUI
- **Toggle Dictation** - Start/stop dictation
- **Settings Manager** - Customize commands
- **Quit SpeakEasy** - Exit

## Hotkeys (Optional)

If you want keyboard shortcuts, set them up in your desktop environment:

| Hotkey | Action |
|--------|--------|
| Super + V | Toggle Dictation |
| Super + A | Open Launcher |

**Note:** Hotkeys are optional — the Control Center GUI works without them!

## Dictation Features

Speak naturally and your words are typed into the active window.

**Punctuation Commands:**
- "period" → .
- "comma" → ,
- "question mark" → ?
- "exclamation point" → !
- "new line" → \n
- "new paragraph" → \n\n
- "open paren" → (
- "close paren" → )
- "semicolon" → ;
- "colon" → :
- "hyphen" → -
- "dash" → -

**Auto-capitalization:**
- Sentences start with capital letters
- "I" is automatically capitalized
- "I'm", "I'll", "I've" are capitalized

## Program Launcher

Click **🎯 Launch Applications** in the Control Center, or press Super+A (if set up).

**Usage:**
1. Say an application name
2. The app launches automatically

**Default Apps:**
- Browsers: Brave, Firefox, Chrome, Chromium
- Terminals: Kitty, Terminal, Alacritty
- Text Editors: Sublime, Gedit, Vim, Neovim, VS Code
- File Managers: Nemo, Nautilus, Thunar
- Creative: GIMP, Inkscape, Spotify, VLC
- Utilities: Calculator, Calendar, System Monitor, Disk Utility, Screenshot
- Web Apps: Google, GitHub, Gmail, Drive, YouTube, Reddit, Google Docs

**Dynamic Search:**
- Say "google [query]" to search the web

## Settings Manager

Click **⚙️ Settings Manager** in the Control Center.

**Features:**
- Add/Edit/Delete commands
- Category organization
- Toggle Comma Fix
- Toggle Tray Icon

## Customization

### Add New Commands

1. Open Settings Manager
2. Click "Add New Command"
3. Enter phrase, command, category
4. Click Save

### Config File Location

`~/.config/speakeasy/config.json`

### Example Config

```json
{
  "voice_commands": {
    "myapp": ["/path/to/app"],
    "open myapp": ["/path/to/app"]
  },
  "aggressive_comma_fix": true,
  "voice_feedback": false,
  "tray_enabled": true
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Microphone not working | Check `arecord -l` |
| Model not found | Ensure `vosk-model-small-en-us-0.15/` exists |
| Tray icon not showing | Install pystray: `pip install pystray Pillow` |
| "Command not understood" | Check phrase in Settings Manager |
| White/blank GUI | Install customtkinter: `pip install customtkinter` |

## Keyboard Shortcuts (in Settings Manager)

| Shortcut | Action |
|----------|--------|
| Ctrl + S | Save config |
| Ctrl + Z | Undo |
| Ctrl + N | New command |
| Ctrl + Q | Quit |
| Escape | Clear selection |

## Advanced

### Run in Background

```bash
./SpeakEasy-x86_64.AppImage &
```

### Multiple Instances

Only one dictation instance can run at a time. Launcher mode runs separately.

### Custom Model

Edit `config.json` to change the model path.