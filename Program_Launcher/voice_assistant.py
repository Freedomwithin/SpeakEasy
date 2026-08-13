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
VOICE_COMMANDS = {
    # Base Utilities
    "sublime": ["subl"],
    "open sublime": ["subl"],
    "brave": ["brave-browser-beta"],
    "open brave": ["brave-browser-beta"],
    "kitty": ["kitty"],
    "open kitty": ["kitty"],
    "nemo": ["nemo"],
    "open nemo": ["nemo"],
    "files": ["nemo"],

    # Custom Security & AI Tools
    "proxy": ["gtk-launch", "Brave_Proxy.desktop"],
    "open proxy": ["gtk-launch", "Brave_Proxy.desktop"],
    "burp": ["gtk-launch", "Burp_Pro_2026.desktop"],
    "open burp": ["gtk-launch", "Burp_Pro_2026.desktop"],
    "claude": ["gtk-launch", "claude.desktop"],
    "open claude": ["gtk-launch", "claude.desktop"],
    "deep seek": ["gtk-launch", "deepseek.desktop"],
    "open deep seek": ["gtk-launch", "deepseek.desktop"],
    "gemini": ["gtk-launch", "gemini.desktop"],
    "open gemini": ["gtk-launch", "gemini.desktop"],

    # Sovereign & Maya Ecosystem
    "anti gravity": ["gtk-launch", "Anti_Gravity.desktop"],
    "open anti gravity": ["gtk-launch", "Anti_Gravity.desktop"],
    "glyph": ["gtk-launch", "Glyph.desktop"],
    "open glyph": ["gtk-launch", "Glyph.desktop"],
    "swarm hub": ["gtk-launch", "sovereign-swarm-hub-v5.desktop"],
    "open swarm hub": ["gtk-launch", "sovereign-swarm-hub-v5.desktop"],
    "neural dashboard": ["gtk-launch", "sovereign-neural-dashboard.desktop"],
    "open neural dashboard": ["gtk-launch", "sovereign-neural-dashboard.desktop"],
    "scratch pad": ["gtk-launch", "sovereign-scratchpad.desktop"],
    "open scratch pad": ["gtk-launch", "sovereign-scratchpad.desktop"],
    "vault": ["gtk-launch", "sovereign-vault.desktop"],
    "open vault": ["gtk-launch", "sovereign-vault.desktop"],
    "call maya": ["gtk-launch", "call_maya.desktop"],

    # General Launchers
    "calendar": ["gtk-launch", "Aeon Calendar Working.desktop"],
    "open calendar": ["gtk-launch", "Aeon Calendar Working.desktop"],
    "gimp": ["gtk-launch", "gimp.desktop"],
    "open gimp": ["gtk-launch", "gimp.desktop"],
    "spotify": ["gtk-launch", "spotify-lite.desktop"],
    "open spotify": ["gtk-launch", "spotify-lite.desktop"],
    "youtube downloader": ["gtk-launch", "youtube_downloader.desktop"],
    "open youtube downloader": ["gtk-launch", "youtube_downloader.desktop"],
}
# =========================================


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