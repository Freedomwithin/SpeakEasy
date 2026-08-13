import json
import os
import subprocess
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "speakeasy"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "sample_rate": 16000,
    "block_size": 4000,
    "aggressive_comma_fix": True,
    "voice_feedback": False,
    "tray_enabled": True,
    "active_model": "vosk-model-small-en-us-0.15",
    "capitalize_words": {
        "i": "I",
        "i'm": "I'm",
        "i'll": "I'll",
        "i've": "I've",
        "i'd": "I'd",
        "jonathon": "Jonathon"
    },
    "voice_commands": {
        "sublime": ["subl"],
        "open sublime": ["subl"],
        "vim": ["vim"],
        "open vim": ["vim"],
        "nvim": ["nvim"],
        "open nvim": ["nvim"],
        "brave": ["brave-browser"],
        "open brave": ["brave-browser"],
        "firefox": ["firefox"],
        "open firefox": ["firefox"],
        "chrome": ["google-chrome"],
        "open chrome": ["google-chrome"],
        "terminal": ["gnome-terminal"],
        "open terminal": ["gnome-terminal"],
        "kitty": ["kitty"],
        "open kitty": ["kitty"],
        "files": ["nemo"],
        "nemo": ["nemo"],
        "open nemo": ["nemo"],
        "vs code": ["code"],
        "open vs code": ["code"],
        "calculator": ["gnome-calculator"],
        "open calculator": ["gnome-calculator"],
        "system monitor": ["gnome-system-monitor"],
        "open system monitor": ["gnome-system-monitor"]
    }
}

def load_config():
    """Loads configuration from ~/.config/speakeasy/config.json with safe fallbacks."""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_FILE, "r") as f:
            user_config = json.load(f)
            # Merge missing default keys
            config = DEFAULT_CONFIG.copy()
            config.update(user_config)
            return config
    except Exception as e:
        print(f"⚠️ Error loading config: {e}. Falling back to default settings.")
        return DEFAULT_CONFIG

def save_config(config):
    """Saves configuration to ~/.config/speakeasy/config.json."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"❌ Error saving config: {e}")

def speak(text, enabled=True):
    """Voice confirmation feedback using espeak or spd-say."""
    if not enabled:
        return
    try:
        if subprocess.call(["which", "espeak"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            subprocess.Popen(["espeak", "-s", "160", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif subprocess.call(["which", "spd-say"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            subprocess.Popen(["spd-say", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def show_gui_error(title, message):
    """Displays a GUI error dialog using zenity, notify-send, or stderr fallback."""
    try:
        if subprocess.call(["which", "zenity"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            subprocess.Popen(["zenity", "--error", "--title", title, "--text", message],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(["notify-send", f"❌ {title}", message, "-t", "4000"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print(f"❌ [{title}] {message}")
