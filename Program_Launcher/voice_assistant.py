#!/usr/bin/env python3
"""
SpeakEasy Launcher - Voice Command Launcher
Fast Start: opens microphone stream FIRST, then loads Vosk model.

Patched:
  - Command matching now uses word-boundary regex + longest-match-wins,
    instead of raw substring `in` checks. Fixes short phrases (e.g.
    "kitty") stealing matches meant for longer phrases that contain them
    (e.g. "open kitty config").
  - Added a duplicate-instance guard: if another voice_assistant.py is
    already running, this one notifies and exits instead of opening a
    second mic listener that would collide with the first.
"""

import sys
import os
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import queue
import json
import signal
import subprocess
import shutil
import urllib.parse
import sounddevice as sd
from vosk import Model, KaldiRecognizer

from config_manager import load_config, show_gui_error
from tray_icon import set_tray_state

SCRIPT_DIR = Path(__file__).parent.absolute()
PARENT_DIR = SCRIPT_DIR.parent
MODEL_PATH = PARENT_DIR / "vosk-model-small-en-us-0.15"
THIS_SCRIPT_NAME = Path(__file__).name

config = load_config()
SAMPLE_RATE = config.get('sample_rate', 16000)
BLOCK_SIZE = config.get('block_size', 4000)
QUEUE_TIMEOUT = 0.2

# HARDCODED VOICE COMMANDS — override config for reliability
VOICE_COMMANDS = {
    # BROWSERS
    "brave": ["brave-browser"],
    "open brave": ["brave-browser"],
    "firefox": ["firefox"],
    "open firefox": ["firefox"],
    "chrome": ["google-chrome"],
    "open chrome": ["google-chrome"],
    "chromium": ["chromium-browser"],
    "open chromium": ["chromium-browser"],

    # TERMINALS
    "kitty": ["kitty"],
    "open kitty": ["kitty"],
    "terminal": ["gnome-terminal"],
    "open terminal": ["gnome-terminal"],
    "alacritty": ["alacritty"],
    "open alacritty": ["alacritty"],

    # TEXT EDITORS
    "sublime": ["subl"],
    "open sublime": ["subl"],
    "text editor": ["gedit"],
    "open text editor": ["gedit"],
    "vim": ["vim"],
    "open vim": ["vim"],
    "nvim": ["nvim"],
    "open nvim": ["nvim"],
    "vs code": ["code"],
    "open vs code": ["code"],
    "vscode": ["code"],
    "open vscode": ["code"],

    # FILE MANAGERS
    "nemo": ["nemo"],
    "open nemo": ["nemo"],
    "files": ["nemo"],
    "nautilus": ["nautilus"],
    "open nautilus": ["nautilus"],
    "thunar": ["thunar"],
    "open thunar": ["thunar"],

    # CREATIVE / MEDIA
    "gimp": ["gimp"],
    "open gimp": ["gimp"],
    "inkscape": ["inkscape"],
    "open inkscape": ["inkscape"],
    "spotify": ["spotify"],
    "open spotify": ["spotify"],
    "vlc": ["vlc"],
    "open vlc": ["vlc"],

    # UTILITIES
    "calculator": ["gnome-calculator"],
    "open calculator": ["gnome-calculator"],
    "calendar": ["gnome-calendar"],
    "open calendar": ["gnome-calendar"],
    "system monitor": ["gnome-system-monitor"],
    "open system monitor": ["gnome-system-monitor"],
    "disk": ["gnome-disk-utility"],
    "open disk": ["gnome-disk-utility"],
    "screenshot": ["gnome-screenshot"],
    "open screenshot": ["gnome-screenshot"],

    # WEB APPS
    "google": ["xdg-open", "https://www.google.com"],
    "open google": ["xdg-open", "https://www.google.com"],
    "gmail": ["xdg-open", "https://mail.google.com"],
    "open gmail": ["xdg-open", "https://mail.google.com"],
    "drive": ["xdg-open", "https://drive.google.com"],
    "open drive": ["xdg-open", "https://drive.google.com"],
    "youtube": ["xdg-open", "https://youtube.com"],
    "open youtube": ["xdg-open", "https://youtube.com"],
    "reddit": ["xdg-open", "https://reddit.com"],
    "open reddit": ["xdg-open", "https://reddit.com"],
    "docs": ["xdg-open", "https://docs.google.com"],
    "open docs": ["xdg-open", "https://docs.google.com"],

    # AI TOOLS
    "claude": ["xdg-open", "https://claude.ai"],
    "open claude": ["xdg-open", "https://claude.ai"],
    "deepseek": ["xdg-open", "https://chat.deepseek.com"],
    "open deepseek": ["xdg-open", "https://chat.deepseek.com"],
    "gemini": ["xdg-open", "https://gemini.google.com"],
    "open gemini": ["xdg-open", "https://gemini.google.com"],

    # GITHUB VARIATIONS
    # "github" is not a real English word and this model's vocabulary
    # doesn't handle it reliably -- it substitutes a different wrong
    # guess almost every time. "repo" is a real, common word and should
    # land consistently; keep the github variants too in case they hit.
    "repo": ["xdg-open", "https://github.com/Freedomwithin"],
    "open repo": ["xdg-open", "https://github.com/Freedomwithin"],
    "repository": ["xdg-open", "https://github.com/Freedomwithin"],
    "open repository": ["xdg-open", "https://github.com/Freedomwithin"],
    "github": ["xdg-open", "https://github.com/Freedomwithin"],
    "open github": ["xdg-open", "https://github.com/Freedomwithin"],
    "git hub": ["xdg-open", "https://github.com/Freedomwithin"],
    "open git hub": ["xdg-open", "https://github.com/Freedomwithin"],
    "git tub": ["xdg-open", "https://github.com/Freedomwithin"],
    "open git tub": ["xdg-open", "https://github.com/Freedomwithin"],

    # SYSTEM TOOLS
    "settings": ["gnome-control-center"],
    "open settings": ["gnome-control-center"],
    "software": ["gnome-software"],
    "open software": ["gnome-software"],
    "bluetooth": ["gnome-control-center", "bluetooth"],
    "open bluetooth": ["gnome-control-center", "bluetooth"],
    "wifi": ["nm-connection-editor"],
    "open wifi": ["nm-connection-editor"],
    "system info": ["gnome-system-information"],
    "open system info": ["gnome-system-information"],

    # COMMUNICATION
    "discord": ["discord"],
    "open discord": ["discord"],
    "slack": ["slack"],
    "open slack": ["slack"],

    # DOCUMENTS
    "libreoffice": ["libreoffice"],
    "open libreoffice": ["libreoffice"],
    "word": ["libreoffice", "--writer"],
    "open word": ["libreoffice", "--writer"],
    "excel": ["libreoffice", "--calc"],
    "open excel": ["libreoffice", "--calc"],

    # TERMINAL MULTIPLEXERS
    "tmux": ["tmux"],
    "open tmux": ["tmux"],

    # JONATHON'S SPECIFICS
    "open maya": ["nemo", "/home/jonathon/gemini-jules/maya"],
    "maya": ["nemo", "/home/jonathon/gemini-jules/maya"],
    "open applications": ["nemo", "/home/jonathon/.local/share/applications"],
    "applications": ["nemo", "/home/jonathon/.local/share/applications"],
    "open kitty config": ["subl", "/home/jonathon/.config/kitty/kitty.conf"],
    "kitty config": ["subl", "/home/jonathon/.config/kitty/kitty.conf"]
}


class SpeakEasyLauncher:
    def __init__(self):
        os.environ["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"
        os.environ["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{os.getuid()}/bus"

        # Duplicate-instance guard: refuse to start a second listener if
        # one is already running -- prevents two processes fighting over
        # the same mic and producing garbled/wrong command matches.
        if self._already_running():
            msg = "SpeakEasy launcher is already running -- not starting a second one."
            print(f"⚠️ {msg}")
            self.send_notification("SpeakEasy", f"⚠️ {msg}", timeout=2500)
            sys.exit(0)

        if not Path(MODEL_PATH).exists():
            msg = f"Vosk model not found at {MODEL_PATH}"
            print(f"❌ {msg}")
            show_gui_error("Model Not Found", msg)
            sys.exit(1)

        self.model = None
        self.recognizer = None
        self.audio_queue = queue.Queue()
        self.is_running = True
        self.command_fired = False

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def _already_running(self):
        try:
            result = subprocess.run(
                ["pgrep", "-f", THIS_SCRIPT_NAME],
                capture_output=True, text=True
            )
            pids = [p for p in result.stdout.split() if p and int(p) != os.getpid()]
            return len(pids) > 0
        except Exception:
            # If pgrep itself fails for some reason, don't block startup
            # over it -- just proceed as normal.
            return False

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
            set_tray_state(True)

            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            ):
                self.send_notification("SpeakEasy", "🎙️ Voice Assistant Ready — start speaking", timeout=2000)

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
                            self.execute_app(text, VOICE_COMMANDS[text])
                            return
        except Exception as e:
            print(f"❌ Audio error: {e}")
            show_gui_error("Audio Error", f"Audio crash: {str(e)[:60]}")
        finally:
            set_tray_state(False)

    def find_best_match(self, text):
        """
        Word-boundary + longest-match-wins. Prevents a short phrase like
        "kitty" from matching inside a longer phrase like "open kitty
        config" just because it's dict-order first.
        """
        if text in VOICE_COMMANDS:
            return text

        best_phrase = None
        for phrase in VOICE_COMMANDS:
            if re.search(r"\b" + re.escape(phrase) + r"\b", text):
                if best_phrase is None or len(phrase) > len(best_phrase):
                    best_phrase = phrase
        return best_phrase

    def process_command(self, text):
        if self.command_fired:
            return
        print(f"🗣️ Processing: '{text}'")

        if text == "google" or text.startswith("google "):
            query = text[len("google"):].strip()
            self.execute_google_search(query)
            return

        best_phrase = self.find_best_match(text)
        if best_phrase:
            self.execute_app(best_phrase, VOICE_COMMANDS[best_phrase])
            return

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
            show_gui_error("Launch Error", f"'{opener}' not found")
            return

        if query:
            encoded = urllib.parse.quote_plus(query)
            url = f"https://www.google.com/search?q={encoded}"
        else:
            url = "https://www.google.com"

        try:
            subprocess.Popen([opener, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            show_gui_error("Launch Error", f"Failed: {str(e)[:40]}")

    def execute_app(self, phrase, cmd_args):
        if self.command_fired:
            return
        self.command_fired = True
        self.is_running = False

        binary = cmd_args[0]
        if binary != "gtk-launch" and not shutil.which(binary):
            show_gui_error("Launch Error", f"'{binary}' not found")
            return

        try:
            subprocess.Popen(cmd_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.send_notification("SpeakEasy", f"🚀 Launched: {phrase}", timeout=1500)
        except Exception as e:
            show_gui_error("Launch Error", f"Failed: {str(e)[:40]}")


if __name__ == "__main__":
    launcher = SpeakEasyLauncher()
    launcher.run()