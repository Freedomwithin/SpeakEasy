#!/usr/bin/env python3
"""
SpeakEasy Control Panel — Premium GUI Command Center
"""

import sys
import os
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

import customtkinter as ctk
from config_manager import load_config, show_gui_error

# Colour Palette
NIGHT_BG     = "#08080f"
DEEP_INDIGO  = "#0d0d1c"
PANEL_BG     = "#10101f"
CARD_BG      = "#13132a"
INPUT_BG     = "#1a1a2e"
BORDER       = "#1e1e40"
VIVID_INDIGO = "#6366f1"
STEEL        = "#6c6c8c"
WHITE        = "#ffffff"
LIGHT_GRAY   = "#c8c8e0"
LIME         = "#10b981"
CRIMSON      = "#ef4444"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class SpeakEasyControlApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SpeakEasy — Control Center")
        self.geometry("440x380")
        self.resizable(False, False)
        self.configure(fg_color=NIGHT_BG)

        self.dictation_process = None
        self.is_running = False
        self.build_ui()
        self.check_initial_status()

    def build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=PANEL_BG, border_color=BORDER, border_width=1, corner_radius=12)
        header.pack(fill="x", padx=16, pady=(16, 12))

        ctk.CTkLabel(header, text="🎙️ SpeakEasy Command Center",
                     font=ctk.CTkFont(family="Inter", size=16, weight="bold"),
                     text_color=WHITE).pack(pady=(12, 2))
        ctk.CTkLabel(header, text="Offline Voice Dictation & Program Launcher",
                     font=ctk.CTkFont(family="Inter", size=11),
                     text_color=STEEL).pack(pady=(0, 12))

        # Status
        status_card = ctk.CTkFrame(self, fg_color=CARD_BG, border_color=BORDER, border_width=1, corner_radius=10)
        status_card.pack(fill="x", padx=16, pady=6)

        self.status_indicator = ctk.CTkLabel(status_card, text="● DICTATION IDLE",
                                              font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                                              text_color=STEEL)
        self.status_indicator.pack(pady=12)

        # Dictation Toggle Button
        self.toggle_btn = ctk.CTkButton(self, text="▶  Start Dictation",
                                         font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
                                         fg_color=VIVID_INDIGO, hover_color="#4f46e5",
                                         height=46, corner_radius=10,
                                         command=self.toggle_dictation)
        self.toggle_btn.pack(fill="x", padx=16, pady=8)

        # Launcher Button
        launcher_btn = ctk.CTkButton(self, text="🎯 Launch Application",
                                      font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                                      fg_color="#0d1f2e", hover_color="#1a3344",
                                      border_color=BORDER, border_width=1,
                                      text_color=LIGHT_GRAY,
                                      height=40, corner_radius=10,
                                      command=self.open_launcher)
        launcher_btn.pack(fill="x", padx=16, pady=4)

        # Help
        help_card = ctk.CTkFrame(self, fg_color=DEEP_INDIGO, corner_radius=8)
        help_card.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(help_card,
                     text="💡 Hotkey: Super+V (Dictation) | Super+A (Launcher)\nRight-click tray icon for quick controls",
                     font=ctk.CTkFont(family="Inter", size=10),
                     text_color=LIGHT_GRAY, justify="center").pack(pady=8)

        # Bottom Buttons
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(0, 12))

        settings_btn = ctk.CTkButton(btn_row, text="⚙️ Settings Manager",
                                      font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
                                      fg_color=PANEL_BG, hover_color=DEEP_INDIGO,
                                      border_color=BORDER, border_width=1,
                                      text_color=LIGHT_GRAY, height=34, width=170,
                                      corner_radius=8, command=self.open_settings)
        settings_btn.pack(side="left")

        quit_btn = ctk.CTkButton(btn_row, text="✕ Quit App",
                                  font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
                                  fg_color="#1a101f", hover_color=CRIMSON,
                                  border_color="#3b111f", border_width=1,
                                  text_color="#fca5a5", height=34, width=100,
                                  corner_radius=8, command=self.quit_app)
        quit_btn.pack(side="right")

    def check_initial_status(self):
        p = subprocess.run(["pgrep", "-f", "voice_to_text_dictation.py"], capture_output=True)
        if p.returncode == 0:
            self.set_active_ui(True)

    def set_active_ui(self, active: bool):
        self.is_running = active
        if active:
            self.status_indicator.configure(text="● DICTATION ACTIVE", text_color=LIME)
            self.toggle_btn.configure(text="⏹  Stop Dictation", fg_color=CRIMSON, hover_color="#dc2626")
        else:
            self.status_indicator.configure(text="● DICTATION IDLE", text_color=STEEL)
            self.toggle_btn.configure(text="▶  Start Dictation", fg_color=VIVID_INDIGO, hover_color="#4f46e5")

    def toggle_dictation(self):
        dictation_script = SCRIPT_DIR / "voice_to_text_dictation.py"
        p = subprocess.run(["pgrep", "-f", "voice_to_text_dictation.py"], capture_output=True)

        if p.returncode == 0 or self.is_running:
            subprocess.run(["pkill", "-f", "voice_to_text_dictation.py"])
            if self.dictation_process:
                try:
                    self.dictation_process.terminate()
                except Exception:
                    pass
                self.dictation_process = None
            self.set_active_ui(False)
        else:
            try:
                self.dictation_process = subprocess.Popen([sys.executable, str(dictation_script)])
                self.set_active_ui(True)
            except Exception as e:
                show_gui_error("Launch Error", f"Failed to start dictation: {e}")

    def open_launcher(self):
        launcher_script = SCRIPT_DIR / "Program_Launcher" / "voice_assistant.py"
        try:
            subprocess.Popen([sys.executable, str(launcher_script)])
            self.send_notification("SpeakEasy", "🎯 Listening for app command...", timeout=2000)
        except Exception as e:
            show_gui_error("Launcher Error", f"Failed to start launcher: {e}")

    def send_notification(self, title, message, timeout=2000):
        try:
            subprocess.Popen(["notify-send", title, message, "-t", str(timeout)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def open_settings(self):
        settings_script = SCRIPT_DIR / "settings_gui.py"
        try:
            subprocess.Popen([sys.executable, str(settings_script)])
        except Exception as e:
            show_gui_error("Settings Error", f"Failed to open settings: {e}")

    def quit_app(self):
        subprocess.run(["pkill", "-f", "voice_to_text_dictation.py"])
        self.destroy()


if __name__ == "__main__":
    app = SpeakEasyControlApp()
    app.protocol("WM_DELETE_WINDOW", app.quit_app)
    app.mainloop()
