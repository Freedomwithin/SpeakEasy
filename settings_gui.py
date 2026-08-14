#!/usr/bin/env python3
"""
SpeakEasy Settings & Command Manager — Premium GUI v2
Dark indigo/blue aesthetic using customtkinter.
"""

import sys
import json
import threading
import subprocess
import shutil
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk

import customtkinter as ctk

# Try to add local venv to path for config_manager
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from config_manager import load_config, save_config, speak
except ImportError:
    def load_config(): return {"voice_commands": {}, "voice_feedback": True, "aggressive_comma_fix": True}
    def save_config(c): pass
    def speak(t, e=True): pass

NIGHT_BG     = "#08080f"
DEEP_INDIGO  = "#0d0d1c"
PANEL_BG     = "#10101f"
CARD_BG      = "#13132a"
INPUT_BG     = "#1a1a2e"
BORDER       = "#1e1e40"
VIVID_INDIGO = "#6366f1"
INDIGO_GLOW  = "#a5b4ff"
SOFT_BLUE    = "#3b82f6"
STEEL        = "#6c6c8c"
DIM_TEXT     = "#4a4a6a"
WHITE        = "#ffffff"
LIGHT_GRAY   = "#c8c8e0"
LIME         = "#10b981"
CRIMSON      = "#ef4444"
AMBER        = "#f59e0b"

CATEGORIES = ["All", "Apps", "Browsers", "Terminals", "Files", "Media", "Dev Tools", "Utilities", "Web", "Custom"]

CATEGORY_COLORS = {
    "Apps":        "#6366f1",
    "Browsers":    "#3b82f6",
    "Terminals":   "#10b981",
    "Files":       "#f59e0b",
    "Media":       "#ec4899",
    "Dev Tools":   "#8b5cf6",
    "Utilities":   "#06b6d4",
    "Web":         "#14b8a6",
    "Custom":      "#a78bfa",
    "All":         "#6c6c8c",
}

def auto_category(phrase: str, cmd: list) -> str:
    binary = cmd[0] if cmd else ""
    browsers = ["brave-browser", "firefox", "google-chrome", "chromium-browser", "xdg-open"]
    terminals = ["gnome-terminal", "kitty", "alacritty", "xterm", "tilix"]
    files = ["nemo", "nautilus", "thunar", "dolphin"]
    media = ["spotify", "vlc", "mpv", "rhythmbox", "clementine"]
    dev = ["code", "subl", "vim", "nvim", "pycharm-community", "idea", "gedit"]
    utils = ["gnome-calculator", "gnome-disk-utility", "gnome-system-monitor", "gtk-launch"]
    if binary in browsers: return "Browsers"
    if binary in terminals: return "Terminals"
    if binary in files: return "Files"
    if binary in media: return "Media"
    if binary in dev: return "Dev Tools"
    if binary in utils: return "Utilities"
    if "http" in " ".join(cmd): return "Web"
    return "Custom"


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SpeakEasyGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SpeakEasy — Command Center")
        self.geometry("1120x780")
        self.minsize(900, 640)
        self.configure(fg_color=NIGHT_BG)
        self.resizable(True, True)

        self.config_data = load_config()
        self.commands_raw = dict(self.config_data.get("voice_commands", {}))
        self.category_map = {}
        self._build_category_map()
        self.filter_category = "All"
        self.search_term = ""
        self.selected_phrase = None
        self.undo_stack = []

        self._build_ui()
        self._refresh_list()

        self.bind("<Control-s>", lambda e: self._save_config())
        self.bind("<Control-q>", lambda e: self.destroy())
        self.bind("<Control-z>", lambda e: self._undo())
        self.bind("<Control-n>", lambda e: self._focus_new_entry())
        self.bind("<Escape>", lambda e: self._clear_selection())

    def _build_category_map(self):
        for phrase, cmd in self.commands_raw.items():
            if phrase not in self.category_map:
                self.category_map[phrase] = auto_category(phrase, cmd)

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color=DEEP_INDIGO, corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_lbl = ctk.CTkLabel(
            header, text="🎙  SpeakEasy  —  Command Center",
            font=ctk.CTkFont("Arial", 24, "bold"),
            text_color=VIVID_INDIGO
        )
        title_lbl.pack(side="left", padx=24, pady=18)

        sub_lbl = ctk.CTkLabel(
            header, text="Voice Command Manager  ·  v2.0",
            font=ctk.CTkFont("Arial", 13),
            text_color=STEEL
        )
        sub_lbl.pack(side="left", padx=0, pady=22)

        hint_lbl = ctk.CTkLabel(
            header, text="Ctrl+S  Save    Ctrl+Z  Undo    Ctrl+N  New    Ctrl+Q  Quit",
            font=ctk.CTkFont("Arial", 11),
            text_color=DIM_TEXT
        )
        hint_lbl.pack(side="right", padx=20)

        body = ctk.CTkFrame(self, fg_color=NIGHT_BG, corner_radius=0)
        body.pack(fill="both", expand=True, padx=0, pady=0)

        sidebar = ctk.CTkFrame(body, fg_color=DEEP_INDIGO, corner_radius=0, width=190)
        sidebar.pack(side="left", fill="y", padx=0)
        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar, text="CATEGORIES",
            font=ctk.CTkFont("Arial", 11, "bold"),
            text_color=STEEL
        ).pack(anchor="w", padx=16, pady=(18, 8))

        self.cat_buttons = {}
        for cat in CATEGORIES:
            color = CATEGORY_COLORS.get(cat, STEEL)
            btn = ctk.CTkButton(
                sidebar,
                text=cat,
                font=ctk.CTkFont("Arial", 13),
                fg_color="transparent",
                hover_color=INPUT_BG,
                text_color=LIGHT_GRAY,
                anchor="w",
                corner_radius=8,
                height=38,
                command=lambda c=cat: self._filter_category(c)
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.cat_buttons[cat] = btn

        ctk.CTkFrame(sidebar, fg_color=BORDER, height=1).pack(fill="x", padx=10, pady=16)

        ctk.CTkLabel(sidebar, text="SETTINGS", font=ctk.CTkFont("Arial", 11, "bold"), text_color=STEEL).pack(anchor="w", padx=16, pady=(0, 8))

        self.voice_fb_var = ctk.BooleanVar(value=self.config_data.get("voice_feedback", True))
        ctk.CTkSwitch(
            sidebar, text="Voice Feedback",
            font=ctk.CTkFont("Arial", 12),
            variable=self.voice_fb_var,
            text_color=LIGHT_GRAY,
            button_color=VIVID_INDIGO,
            progress_color=VIVID_INDIGO,
            fg_color=INPUT_BG,
        ).pack(anchor="w", padx=14, pady=5)

        self.comma_fix_var = ctk.BooleanVar(value=self.config_data.get("aggressive_comma_fix", True))
        ctk.CTkSwitch(
            sidebar, text="Comma Fix",
            font=ctk.CTkFont("Arial", 12),
            variable=self.comma_fix_var,
            text_color=LIGHT_GRAY,
            button_color=VIVID_INDIGO,
            progress_color=VIVID_INDIGO,
            fg_color=INPUT_BG,
        ).pack(anchor="w", padx=14, pady=5)

        self.tray_var = ctk.BooleanVar(value=self.config_data.get("tray_enabled", True))
        ctk.CTkSwitch(
            sidebar, text="Tray Icon",
            font=ctk.CTkFont("Arial", 12),
            variable=self.tray_var,
            text_color=LIGHT_GRAY,
            button_color=VIVID_INDIGO,
            progress_color=VIVID_INDIGO,
            fg_color=INPUT_BG,
        ).pack(anchor="w", padx=14, pady=5)

        main = ctk.CTkFrame(body, fg_color=NIGHT_BG, corner_radius=0)
        main.pack(side="left", fill="both", expand=True, padx=0)

        search_row = ctk.CTkFrame(main, fg_color=PANEL_BG, corner_radius=0, height=56)
        search_row.pack(fill="x")
        search_row.pack_propagate(False)

        search_icon = ctk.CTkLabel(search_row, text="⌕", font=ctk.CTkFont("Arial", 20), text_color=STEEL)
        search_icon.pack(side="left", padx=(16, 6), pady=10)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._on_search())
        search_entry = ctk.CTkEntry(
            search_row,
            textvariable=self.search_var,
            placeholder_text="Search commands...",
            font=ctk.CTkFont("Arial", 14),
            fg_color=INPUT_BG,
            border_color=BORDER,
            text_color=WHITE,
            height=38,
            corner_radius=8,
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=9)

        ctk.CTkButton(
            search_row, text="⬆  Export",
            font=ctk.CTkFont("Arial", 12, "bold"),
            fg_color=INPUT_BG, hover_color=BORDER,
            text_color=INDIGO_GLOW, border_color=BORDER, border_width=1,
            corner_radius=8, height=38, width=100,
            command=self._export_commands
        ).pack(side="right", padx=(0, 10), pady=9)

        ctk.CTkButton(
            search_row, text="⬇  Import",
            font=ctk.CTkFont("Arial", 12, "bold"),
            fg_color=INPUT_BG, hover_color=BORDER,
            text_color=INDIGO_GLOW, border_color=BORDER, border_width=1,
            corner_radius=8, height=38, width=100,
            command=self._import_commands
        ).pack(side="right", padx=(0, 6), pady=9)

        col_header = ctk.CTkFrame(main, fg_color=CARD_BG, corner_radius=0, height=40)
        col_header.pack(fill="x")
        col_header.pack_propagate(False)

        ctk.CTkLabel(col_header, text="VOICE PHRASE", font=ctk.CTkFont("Arial", 11, "bold"),
                     text_color=STEEL).pack(side="left", padx=(18, 0), pady=10)
        ctk.CTkLabel(col_header, text="COMMAND", font=ctk.CTkFont("Arial", 11, "bold"),
                     text_color=STEEL).place(x=340, y=10)
        ctk.CTkLabel(col_header, text="CATEGORY", font=ctk.CTkFont("Arial", 11, "bold"),
                     text_color=STEEL).place(x=580, y=10)
        ctk.CTkLabel(col_header, text="ACTIONS", font=ctk.CTkFont("Arial", 11, "bold"),
                     text_color=STEEL).place(x=760, y=10)

        self.list_frame = ctk.CTkScrollableFrame(
            main, fg_color=PANEL_BG, corner_radius=0,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=VIVID_INDIGO,
        )
        self.list_frame.pack(fill="both", expand=True)

        editor = ctk.CTkFrame(main, fg_color=DEEP_INDIGO, corner_radius=0, height=150)
        editor.pack(fill="x")
        editor.pack_propagate(False)

        self.editor_title = ctk.CTkLabel(
            editor, text="✦  ADD NEW COMMAND",
            font=ctk.CTkFont("Arial", 12, "bold"),
            text_color=VIVID_INDIGO
        )
        self.editor_title.pack(anchor="w", padx=18, pady=(14, 6))

        fields_row = ctk.CTkFrame(editor, fg_color="transparent")
        fields_row.pack(fill="x", padx=18, pady=0)

        ctk.CTkLabel(fields_row, text="Phrase", font=ctk.CTkFont("Arial", 12), text_color=STEEL).grid(row=0, column=0, sticky="w", pady=2)
        self.phrase_entry = ctk.CTkEntry(
            fields_row, placeholder_text="e.g. open brave",
            font=ctk.CTkFont("Arial", 13),
            fg_color=INPUT_BG, border_color=BORDER, text_color=WHITE,
            height=38, corner_radius=8, width=220
        )
        self.phrase_entry.grid(row=1, column=0, padx=(0, 12))

        ctk.CTkLabel(fields_row, text="Command", font=ctk.CTkFont("Arial", 12), text_color=STEEL).grid(row=0, column=1, sticky="w", pady=2)
        self.cmd_entry = ctk.CTkEntry(
            fields_row, placeholder_text="e.g. brave-browser",
            font=ctk.CTkFont("Arial", 13),
            fg_color=INPUT_BG, border_color=BORDER, text_color=WHITE,
            height=38, corner_radius=8, width=220
        )
        self.cmd_entry.grid(row=1, column=1, padx=(0, 12))

        ctk.CTkLabel(fields_row, text="Category", font=ctk.CTkFont("Arial", 12), text_color=STEEL).grid(row=0, column=2, sticky="w", pady=2)
        self.cat_var = ctk.StringVar(value="Custom")
        self.cat_menu = ctk.CTkOptionMenu(
            fields_row, values=CATEGORIES[1:],
            variable=self.cat_var,
            fg_color=INPUT_BG, button_color=VIVID_INDIGO,
            button_hover_color=SOFT_BLUE,
            dropdown_fg_color=CARD_BG, dropdown_text_color=WHITE,
            dropdown_hover_color=INPUT_BG,
            text_color=WHITE, font=ctk.CTkFont("Arial", 13),
            height=38, corner_radius=8, width=140
        )
        self.cat_menu.grid(row=1, column=2, padx=(0, 12))

        btn_col = ctk.CTkFrame(fields_row, fg_color="transparent")
        btn_col.grid(row=0, column=3, rowspan=2, padx=(12, 0), sticky="s")

        self.add_btn = ctk.CTkButton(
            btn_col, text="＋  Add / Update",
            font=ctk.CTkFont("Arial", 13, "bold"),
            fg_color=VIVID_INDIGO, hover_color=SOFT_BLUE,
            text_color=WHITE, corner_radius=8,
            height=38, width=150,
            command=self._add_command
        )
        self.add_btn.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_col, text="✕  Clear",
            font=ctk.CTkFont("Arial", 13),
            fg_color=INPUT_BG, hover_color=BORDER,
            text_color=LIGHT_GRAY, border_color=BORDER, border_width=1,
            corner_radius=8, height=38, width=100,
            command=self._clear_selection
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_col, text="💾  Save Config",
            font=ctk.CTkFont("Arial", 13, "bold"),
            fg_color=LIME, hover_color="#059669",
            text_color="#000000", corner_radius=8,
            height=38, width=150,
            command=self._save_config
        ).pack(side="left")

        self.status_bar = ctk.CTkFrame(self, fg_color=DEEP_INDIGO, corner_radius=0, height=32)
        self.status_bar.pack(fill="x", side="bottom")
        self.status_bar.pack_propagate(False)
        self.status_lbl = ctk.CTkLabel(
            self.status_bar, text="Ready.",
            font=ctk.CTkFont("Arial", 11), text_color=STEEL
        )
        self.status_lbl.pack(side="left", padx=16)
        self.count_lbl = ctk.CTkLabel(
            self.status_bar, text="",
            font=ctk.CTkFont("Arial", 11), text_color=STEEL
        )
        self.count_lbl.pack(side="right", padx=16)

    def _refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        visible = []
        for phrase, cmd in self.commands_raw.items():
            cat = self.category_map.get(phrase, "Custom")
            cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
            if self.filter_category != "All" and cat != self.filter_category:
                continue
            if self.search_term and self.search_term not in phrase.lower() and self.search_term not in cmd_str.lower():
                continue
            visible.append((phrase, cmd, cmd_str, cat))

        for i, (phrase, cmd, cmd_str, cat) in enumerate(visible):
            row_color = CARD_BG if i % 2 == 0 else PANEL_BG
            is_selected = phrase == self.selected_phrase
            if is_selected:
                row_color = "#1c1c3d"

            row = ctk.CTkFrame(self.list_frame, fg_color=row_color, corner_radius=6, height=48)
            row.pack(fill="x", padx=8, pady=3)
            row.pack_propagate(False)
            row.bind("<Button-1>", lambda e, p=phrase, c=cmd, cs=cmd_str, ca=cat: self._select_row(p, c, cs, ca))

            ph_lbl = ctk.CTkLabel(row, text=phrase, font=ctk.CTkFont("Arial", 13),
                                   text_color=WHITE if not is_selected else INDIGO_GLOW,
                                   anchor="w", width=300)
            ph_lbl.place(x=14, y=12)
            ph_lbl.bind("<Button-1>", lambda e, p=phrase, c=cmd, cs=cmd_str, ca=cat: self._select_row(p, c, cs, ca))

            cmd_lbl = ctk.CTkLabel(row, text=cmd_str, font=ctk.CTkFont("Arial", 12),
                                    text_color=LIGHT_GRAY, anchor="w", width=230)
            cmd_lbl.place(x=324, y=13)
            cmd_lbl.bind("<Button-1>", lambda e, p=phrase, c=cmd, cs=cmd_str, ca=cat: self._select_row(p, c, cs, ca))

            cat_color = CATEGORY_COLORS.get(cat, STEEL)
            cat_badge = ctk.CTkLabel(
                row, text=f"  {cat}  ",
                font=ctk.CTkFont("Arial", 11, "bold"),
                text_color=cat_color,
                fg_color=INPUT_BG,
                corner_radius=6,
                width=100
            )
            cat_badge.place(x=564, y=11)

            test_btn = ctk.CTkButton(
                row, text="▶", width=34, height=30,
                font=ctk.CTkFont("Arial", 12),
                fg_color=INPUT_BG, hover_color=LIME,
                text_color=LIME, border_color=BORDER, border_width=1,
                corner_radius=6,
                command=lambda c=cmd: self._test_command(c)
            )
            test_btn.place(x=740, y=9)

            del_btn = ctk.CTkButton(
                row, text="✕", width=34, height=30,
                font=ctk.CTkFont("Arial", 12),
                fg_color=INPUT_BG, hover_color=CRIMSON,
                text_color=CRIMSON, border_color=BORDER, border_width=1,
                corner_radius=6,
                command=lambda p=phrase: self._delete_command(p)
            )
            del_btn.place(x=785, y=9)

        total = len(self.commands_raw)
        shown = len(visible)
        self.count_lbl.configure(text=f"{shown} of {total} commands")
        self._update_cat_buttons()

    def _select_row(self, phrase, cmd, cmd_str, cat):
        self.selected_phrase = phrase
        self.phrase_entry.delete(0, "end")
        self.phrase_entry.insert(0, phrase)
        self.cmd_entry.delete(0, "end")
        self.cmd_entry.insert(0, cmd_str)
        self.cat_var.set(cat)
        self.editor_title.configure(text=f"✦  EDITING: {phrase.upper()}")
        self._refresh_list()

    def _clear_selection(self, *args):
        self.selected_phrase = None
        self.phrase_entry.delete(0, "end")
        self.cmd_entry.delete(0, "end")
        self.cat_var.set("Custom")
        self.editor_title.configure(text="✦  ADD NEW COMMAND")
        self._refresh_list()

    def _filter_category(self, cat):
        self.filter_category = cat
        self._refresh_list()

    def _on_search(self):
        self.search_term = self.search_var.get().lower()
        self._refresh_list()

    def _update_cat_buttons(self):
        for cat, btn in self.cat_buttons.items():
            if cat == self.filter_category:
                btn.configure(fg_color=INPUT_BG, text_color=INDIGO_GLOW)
            else:
                btn.configure(fg_color="transparent", text_color=LIGHT_GRAY)

    def _focus_new_entry(self):
        self._clear_selection()
        self.phrase_entry.focus()

    def _add_command(self):
        phrase = self.phrase_entry.get().strip().lower()
        cmd_str = self.cmd_entry.get().strip()
        cat = self.cat_var.get()

        if not phrase or not cmd_str:
            self._set_status("⚠  Phrase and Command are both required.", AMBER)
            return

        self.undo_stack.append(dict(self.commands_raw))
        if len(self.undo_stack) > 30:
            self.undo_stack.pop(0)

        self.commands_raw[phrase] = cmd_str.split()
        self.category_map[phrase] = cat
        self._clear_selection()
        self._set_status(f"✓  Command '{phrase}' added / updated.", LIME)

    def _delete_command(self, phrase):
        self.undo_stack.append(dict(self.commands_raw))
        self.commands_raw.pop(phrase, None)
        self.category_map.pop(phrase, None)
        if self.selected_phrase == phrase:
            self.selected_phrase = None
        self._refresh_list()
        self._set_status(f"✕  Command '{phrase}' deleted.", CRIMSON)

    def _undo(self, *args):
        if not self.undo_stack:
            self._set_status("Nothing to undo.", STEEL)
            return
        self.commands_raw = self.undo_stack.pop()
        self._refresh_list()
        self._set_status("↩  Undo applied.", AMBER)

    def _test_command(self, cmd):
        binary = cmd[0] if cmd else ""
        if binary and not shutil.which(binary) and binary != "gtk-launch" and not Path(binary).exists():
            self._set_status(f"✕  Binary '{binary}' not found on PATH.", CRIMSON)
            return
        try:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._set_status(f"▶  Launched: {' '.join(cmd)}", LIME)
        except Exception as ex:
            self._set_status(f"✕  Launch failed: {ex}", CRIMSON)

    def _save_config(self, *args):
        self.config_data["voice_commands"] = self.commands_raw
        self.config_data["voice_feedback"] = self.voice_fb_var.get()
        self.config_data["aggressive_comma_fix"] = self.comma_fix_var.get()
        self.config_data["tray_enabled"] = self.tray_var.get()
        save_config(self.config_data)
        speak("Configuration saved", self.config_data.get("voice_feedback", True))
        self._set_status("💾  Configuration saved to ~/.config/speakeasy/config.json", LIME)

    def _export_commands(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Export SpeakEasy Commands"
        )
        if not path:
            return
        export = {"voice_commands": self.commands_raw, "categories": self.category_map}
        with open(path, "w") as f:
            json.dump(export, f, indent=2)
        self._set_status(f"⬆  Exported to {path}", LIME)

    def _import_commands(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Import SpeakEasy Commands"
        )
        if not path:
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
            imported_cmds = data.get("voice_commands", data)
            imported_cats = data.get("categories", {})
            self.undo_stack.append(dict(self.commands_raw))
            self.commands_raw.update(imported_cmds)
            self.category_map.update(imported_cats)
            self._refresh_list()
            self._set_status(f"⬇  Imported {len(imported_cmds)} commands from {Path(path).name}", LIME)
        except Exception as ex:
            self._set_status(f"✕  Import failed: {ex}", CRIMSON)

    def _set_status(self, msg, color=STEEL):
        self.status_lbl.configure(text=msg, text_color=color)
        self.after(5000, lambda: self.status_lbl.configure(text="Ready.", text_color=STEEL))


def main():
    app = SpeakEasyGUI()
    app.mainloop()


if __name__ == "__main__":
    main()