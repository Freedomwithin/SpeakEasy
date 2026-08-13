#!/usr/bin/env python3
"""
SpeakEasy Dictation Engine
Clean Dump + Expanded Grammar Engine

Builds on V3.4/V3.5/V3.6 with:
  - A longer, ordered command dictionary (multi-word commands checked
    before shorter ones so "new paragraph" doesn't get eaten by "new line")
  - A toggleable fix for Vosk's most common mishear ("come on" -> ",")
  - Sentence capitalization that works mid-block and carries across
    phrase boundaries
  - Fixed "jonathan" -> "Jonathon"
"""

import queue
import sys
import json
import signal
import os
import re
from pathlib import Path
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from pynput.keyboard import Controller

# ============= CONFIGURATION =============
# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()
MODEL_PATH = SCRIPT_DIR / "vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
BLOCK_SIZE = 4000
QUEUE_TIMEOUT = 0.2

# Vosk's small model very often mishears "comma" as "come on". Turning
# this on converts "come on" -> "," which fixes that, but will also fire
# if you ever genuinely dictate the phrase "come on". Flip to False if
# that starts happening more than the comma fix helps.
AGGRESSIVE_COMMA_FIX = True
# =========================================

# Longest/most-specific phrases first, so a multi-word command isn't
# partially consumed by a shorter rule that runs before it.
PUNCTUATION_COMMANDS = [
    (r"\bnew paragraph\b", "\n\n"),
    (r"\bnew line\b", "\n"),
    (r"\bquestion mark\b", "?"),
    (r"\bexclamation (mark|point)\b", "!"),
    (r"\bopen paren(thesis)?\b", "("),
    (r"\bclose paren(thesis)?\b", ")"),
    (r"\bopen quote\b", '"'),
    (r"\bclose quote\b", '"'),
    (r"\bsemi ?colon\b", ";"),
    (r"\bcolon\b", ":"),
    (r"\bhyphen\b", "-"),
    (r"\bdash\b", "-"),
    (r"\bperiod\b", "."),
    (r"\bcomma\b", ","),
]

CAPITALIZE_WORDS = {
    "i": "I",
    "i'm": "I'm",
    "i'll": "I'll",
    "i've": "I've",
    "i'd": "I'd",
    "jonathon": "Jonathon",
}


class SpeakEasyDictation:
    def __init__(self):
        os.environ["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"
        os.environ["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{os.getuid()}/bus"

        if not Path(MODEL_PATH).exists():
            raise FileNotFoundError(f"Model folder not found at: {MODEL_PATH}")

        self.model = None
        self.recognizer = None
        self.keyboard = Controller()
        self.audio_queue = queue.Queue()
        self.is_running = True
        self.capitalize_next = True

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def send_notification(self, title, message, timeout=1500):
        try:
            import subprocess
            subprocess.Popen(["notify-send", title, message, "-t", str(timeout)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def signal_handler(self, sig, frame):
        self.is_running = False

    def audio_callback(self, indata, frames, time, status):
        if self.is_running:
            self.audio_queue.put(bytes(indata))

    def format_and_type(self, raw_text):
        if not raw_text:
            return
        text = raw_text.lower()

        # 1. Phonetic mishear fix
        if AGGRESSIVE_COMMA_FIX:
            text = re.sub(r"\bcome on\b", ",", text)

        # 2. Spoken punctuation commands
        for pattern, replacement in PUNCTUATION_COMMANDS:
            text = re.sub(pattern, replacement, text)

        # 3. Clean up spacing
        text = re.sub(r"\s+([.,!?;:])", r"\1", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = text.strip()
        if not text:
            return

        # 4. Word-level capitalization
        def cap_word(m):
            w = m.group(0)
            return CAPITALIZE_WORDS.get(w.lower(), w)
        text = re.sub(r"[a-zA-Z']+", cap_word, text)

        # 5. Sentence capitalization
        chars = list(text)
        cap_next = self.capitalize_next
        for i, ch in enumerate(chars):
            if ch.isalpha() and cap_next:
                chars[i] = ch.upper()
                cap_next = False
            elif ch in ".!?\n":
                cap_next = True
        text = "".join(chars)
        self.capitalize_next = cap_next

        self.keyboard.type(text + " ")

    def run(self):
        try:
            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            ):
                self.send_notification("SpeakEasy", "🎤 Dictation Active - Speak Now")

                self.model = Model(str(MODEL_PATH))
                self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)

                while self.is_running:
                    try:
                        data = self.audio_queue.get(timeout=QUEUE_TIMEOUT)
                    except queue.Empty:
                        continue

                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        final_text = result.get("text", "").strip()
                        if final_text:
                            self.format_and_type(final_text)

        except Exception as e:
            self.send_notification("SpeakEasy Error", f"❌ Audio Crash: {str(e)[:30]}")


if __name__ == "__main__":
    typer = SpeakEasyDictation()
    typer.run()