# SpeakEasy Usage Guide

## Quick Start

### Install

```bash
# Download the AppImage
wget https://github.com/Freedomwithin/SpeakEasy/releases/latest/download/SpeakEasy-x86_64.AppImage
chmod +x SpeakEasy-x86_64.AppImage
./SpeakEasy-x86_64.AppImage
```

### From Source

```bash
git clone https://github.com/Freedomwithin/SpeakEasy
cd SpeakEasy
./install.sh
```

## Three Modes

### 1. Dictation Mode (Default)

**Start:** Double-click AppImage or `./SpeakEasy-x86_64.AppImage`

**Hotkey:** Super + V (toggle on/off)

**Features:**
- "period" → .
- "comma" → ,
- "question mark" → ?
- "new line" → \n
- "new paragraph" → \n\n
- Auto-capitalization
- "come on" → , (if Comma Fix enabled)

### 2. Program Launcher Mode

**Start:** `./SpeakEasy-x86_64.AppImage --launcher`

**Hotkey:** Super + A

**Usage:**
1. Press Super + A
2. Say "sublime" or "open sublime"
3. App launches automatically

**Default Apps:**
- sublime, brave, kitty, nemo, files
- firefox, chrome, gimp, spotify

**Dynamic Search:**
- Say "google [query]" for web search

### 3. Settings GUI Mode

**Start:** `./SpeakEasy-x86_64.AppImage --settings`

**Features:**
- Add/Edit/Delete commands
- Category organization
- Toggle Voice Feedback
- Toggle Comma Fix
- Toggle Tray Icon

## Customization

### Add New Commands

1. Open Settings GUI: `./SpeakEasy-x86_64.AppImage --settings`
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
  "voice_feedback": true,
  "tray_enabled": true
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Microphone not working | Check `arecord -l` |
| Model not found | Ensure `vosk-model-small-en-us-0.15/` exists |
| Tray icon not showing | Install pystray: `pip install pystray Pillow` |
| Voice feedback not working | Install espeak: `sudo apt install espeak` |
| "Command not understood" | Check phrase in Settings GUI |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Super + V | Toggle Dictation |
| Super + A | Start Launcher |
| Ctrl + S | Save config (in Settings) |
| Ctrl + Z | Undo (in Settings) |

## Advanced

### Run in Background

```bash
./SpeakEasy-x86_64.AppImage &
```

### Multiple Instances

Only one dictation instance can run at a time. Launcher mode runs separately.

### Custom Model

Edit `config.json` to change the model path.
