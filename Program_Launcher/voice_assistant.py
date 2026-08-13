#!/usr/bin/env python3
"""
SpeakEasy Launcher - Voice Command Launcher
Fast Start: opens microphone stream FIRST, then loads Vosk model.

Anything you say while the model loads gets buffered, not lost.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path so we can import config_manager
sys.path.insert(0, str(Path(__file__).parent.parent))

import queue
import json
import signal
import subprocess
import shutil
import urllib.parse
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Import SpeakEasy modules
from config_manager import load_config, save_config, speak, show_gui_error
from tray_icon import set_tray_state

# ============= CONFIGURATION =============
# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()
PARENT_DIR = SCRIPT_DIR.parent
MODEL_PATH = PARENT_DIR / "vosk-model-small-en-us-0.15"

# Load config
config = load_config()
SAMPLE_RATE = config.get('sample_rate', 16000)
BLOCK_SIZE = config.get('block_size', 4000)
QUEUE_TIMEOUT = 0.2

# Build VOICE_COMMANDS from config
VOICE_COMMANDS = config.get('voice_commands', {})
# ============================================

class SpeakEasyLauncher:
    def __init__(self):
        os.environ["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"
        os.environ["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{os.getuid()}/bus"

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
            set_tray_state(True)  # Green = listening
            speak("Listening for commands")

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
            show_gui_error("Audio Error", f"Audio crash: {str(e)[:60]}")
        finally:
            set_tray_state(False)  # Red = stopped
            speak("Stopped listening")

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
        speak(f"Command not understood")
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
            print(f"🚀 Google search: {query!r}")
            subprocess.Popen([opener, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            speak(f"Searching for {query}", self.config.get("voice_feedback", False))
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
            speak(f"Command not found", self.config.get("voice_feedback", False))
            return

        try:
            print(f"🚀 Launching: {cmd_args}")
            subprocess.Popen(cmd_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            speak(f"Opening {phrase}", self.config.get("voice_feedback", False))
        except Exception as e:
            show_gui_error("Launch Error", f"Failed: {str(e)[:40]}")

if __name__ == "__main__":
    launcher = SpeakEasyLauncher()
    launcher.run()