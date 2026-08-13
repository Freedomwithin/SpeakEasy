#!/usr/bin/env python3
"""
SpeakEasy Launcher - Voice Command Launcher
Fast Start: opens microphone stream FIRST, then loads Vosk model.

Anything you say while the model loads gets buffered, not lost.
"""

import queue
import sys
import json
import signal
import subprocess
import os
import shutil
import urllib.parse
from pathlib import Path
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# ============= CONFIGURATION =============
# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()
PARENT_DIR = SCRIPT_DIR.parent
MODEL_PATH = PARENT_DIR / "vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
BLOCK_SIZE = 4000
QUEUE_TIMEOUT = 0.2

# Flexible Command Mapping
# Edit this dictionary to add your own applications
VOICE_COMMANDS = {
    # ============================================
    # COMMON APPLICATIONS (works on most systems)
    # ============================================
    
    # Text Editors
    "sublime": ["subl"],
    "open sublime": ["subl"],
    "vim": ["vim"],
    "open vim": ["vim"],
    "nvim": ["nvim"],
    "open nvim": ["nvim"],
    
    # Browsers
    "brave": ["brave-browser"],
    "open brave": ["brave-browser"],
    "firefox": ["firefox"],
    "open firefox": ["firefox"],
    "chrome": ["google-chrome"],
    "open chrome": ["google-chrome"],
    "chromium": ["chromium-browser"],
    "open chromium": ["chromium-browser"],
    
    # Terminals
    "kitty": ["kitty"],
    "open kitty": ["kitty"],
    "terminal": ["gnome-terminal"],
    "open terminal": ["gnome-terminal"],
    "alacritty": ["alacritty"],
    "open alacritty": ["alacritty"],
    
    # File Managers
    "nemo": ["nemo"],
    "open nemo": ["nemo"],
    "files": ["nemo"],
    "nautilus": ["nautilus"],
    "open nautilus": ["nautilus"],
    "thunar": ["thunar"],
    "open thunar": ["thunar"],
    
    # ============================================
    # COMMON APPLICATIONS (check if installed)
    # ============================================
    
    # Creative
    "gimp": ["gimp"],
    "open gimp": ["gimp"],
    "inkscape": ["inkscape"],
    "open inkscape": ["inkscape"],
    "blender": ["blender"],
    "open blender": ["blender"],
    
    # Media
    "spotify": ["spotify"],
    "open spotify": ["spotify"],
    "vlc": ["vlc"],
    "open vlc": ["vlc"],
    "mpv": ["mpv"],
    "open mpv": ["mpv"],
    
    # Development
    "vs code": ["code"],
    "open vs code": ["code"],
    "vscode": ["code"],
    "open vscode": ["code"],
    "pycharm": ["pycharm-community"],
    "open pycharm": ["pycharm-community"],
    "intellij": ["idea"],
    "open intellij": ["idea"],
    
    # Utilities
    "calculator": ["gnome-calculator"],
    "open calculator": ["gnome-calculator"],
    "disk": ["gnome-disk-utility"],
    "open disk": ["gnome-disk-utility"],
    "system monitor": ["gnome-system-monitor"],
    "open system monitor": ["gnome-system-monitor"],
    
    # ============================================
    # DESKTOP FILES (gtk-launch examples)
    # ============================================
    # Uncomment and modify these to match your system:
    # "slack": ["gtk-launch", "slack.desktop"],
    # "open slack": ["gtk-launch", "slack.desktop"],
    # "discord": ["gtk-launch", "discord.desktop"],
    # "open discord": ["gtk-launch", "discord.desktop"],
    # "zoom": ["gtk-launch", "zoom.desktop"],
    # "open zoom": ["gtk-launch", "zoom.desktop"],
    
    # ============================================
    # CUSTOM EXAMPLES (edit these to match your paths)
    # ============================================
    # Example: Open a folder in Nemo
    # "projects": ["nemo", "/home/username/projects"],
    # "open projects": ["nemo", "/home/username/projects"],
    
    # Example: Open a config file in Sublime
    # "config": ["subl", "/home/username/.config/app/config.conf"],
    # "open config": ["subl", "/home/username/.config/app/config.conf"],
    
    # Example: Open a website
    # "docs": ["xdg-open", "https://docs.example.com"],
    # "open docs": ["xdg-open", "https://docs.example.com"],
}
# ============================================
# NOTE: "google" is handled dynamically below
# Say "google <query>" for web searches
# ============================================


class SpeakEasyLauncher:
    def __init__(self):
        os.environ["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"
        os.environ["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{os.getuid()}/bus"

        if not Path(MODEL_PATH).exists():
            print(f"❌ Vosk model not found at {MODEL_PATH}")
            sys.exit(1)

        self.model = None
        self.recognizer = None
        self.audio_queue = queue.Queue()
        self.is_running = True
        self.command_fired = False

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def send_notification(self, title, message, timeout=2000):
        try:
            subprocess.Popen(["notify-send", title, message, "-t", str(timeout)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def signal_handler(self, sig, frame):
        self.is_running = False

    def audio_callback(self, indata, frames, time, status):
        if self.is_running and not self.command_fired:
            self.audio_queue.put(bytes(indata))

    def run(self):
        try:
            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            ):
                print("🎙️ Listening... Speak your command clearly.")

                self.model = Model(str(MODEL_PATH))
                self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)

                while self.is_running and not self.command_fired:
                    try:
                        data = self.audio_queue.get(timeout=QUEUE_TIMEOUT)
                    except queue.Empty:
                        continue

                    if self.recognizer.AcceptWaveform(data):
                        if self.command_fired:
                            break
                        result = json.loads(self.recognizer.Result())
                        text = result.get("text", "").lower().strip()
                        if text:
                            self.process_command(text)
                    else:
                        if self.command_fired:
                            break
                        partial = json.loads(self.recognizer.PartialResult())
                        text = partial.get("partial", "").lower().strip()
                        if text and text in VOICE_COMMANDS:
                            print(f"⚡ Fast-triggered: '{text}'")
                            self.execute_app(text, VOICE_COMMANDS[text])
                            return
        except Exception as e:
            print(f"❌ Audio error: {e}")
            self.send_notification("SpeakEasy Error", f"❌ Audio crash: {str(e)[:60]}", timeout=3000)

    def process_command(self, text):
        if self.command_fired:
            return
        print(f"🗣️ Processing: '{text}'")

        # Dynamic Google search
        if text == "google" or text.startswith("google "):
            query = text[len("google"):].strip()
            self.execute_google_search(query)
            return

        # Check for direct phrase match
        for phrase, cmd_args in VOICE_COMMANDS.items():
            if phrase == text or (phrase in text and len(text.split()) > 1):
                self.execute_app(phrase, cmd_args)
                return

        print(f"⚠️ Command not understood: '{text}'")
        self.send_notification("SpeakEasy", f"❓ Command not understood: '{text}'", timeout=3000)
        self.command_fired = True
        self.is_running = False

    def execute_google_search(self, query):
        if self.command_fired:
            return
        self.command_fired = True
        self.is_running = False

        opener = "xdg-open"
        if not shutil.which(opener):
            self.send_notification("SpeakEasy Error", f"❌ '{opener}' not found", timeout=3000)
            return

        if query:
            encoded = urllib.parse.quote_plus(query)
            url = f"https://www.google.com/search?q={encoded}"
        else:
            url = "https://www.google.com"

        try:
            print(f"🚀 Google search: {query!r}")
            subprocess.Popen([opener, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            self.send_notification("SpeakEasy Error", f"❌ Failed: {str(e)[:40]}", timeout=3000)

    def execute_app(self, phrase, cmd_args):
        if self.command_fired:
            return
        self.command_fired = True
        self.is_running = False

        binary = cmd_args[0]
        if binary != "gtk-launch" and not shutil.which(binary):
            self.send_notification("SpeakEasy Error", f"❌ '{binary}' not found", timeout=3000)
            return

        try:
            print(f"🚀 Launching: {cmd_args}")
            subprocess.Popen(cmd_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            self.send_notification("SpeakEasy Error", f"❌ Failed: {str(e)[:40]}", timeout=3000)


if __name__ == "__main__":
    launcher = SpeakEasyLauncher()
    launcher.run()
