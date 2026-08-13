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
        # ============================================
        # BROWSERS
        # ============================================
        "brave": ["brave-browser"],
        "open brave": ["brave-browser"],
        "firefox": ["firefox"],
        "open firefox": ["firefox"],
        "chrome": ["google-chrome"],
        "open chrome": ["google-chrome"],
        "chromium": ["chromium-browser"],
        "open chromium": ["chromium-browser"],
        
        # ============================================
        # TERMINALS
        # ============================================
        "kitty": ["kitty"],
        "open kitty": ["kitty"],
        "terminal": ["gnome-terminal"],
        "open terminal": ["gnome-terminal"],
        "alacritty": ["alacritty"],
        "open alacritty": ["alacritty"],
        
        # ============================================
        # TEXT EDITORS
        # ============================================
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
        
        # ============================================
        # FILE MANAGERS
        # ============================================
        "nemo": ["nemo"],
        "open nemo": ["nemo"],
        "files": ["nemo"],
        "nautilus": ["nautilus"],
        "open nautilus": ["nautilus"],
        "thunar": ["thunar"],
        "open thunar": ["thunar"],
        
        # ============================================
        # CREATIVE / MEDIA
        # ============================================
        "gimp": ["gimp"],
        "open gimp": ["gimp"],
        "inkscape": ["inkscape"],
        "open inkscape": ["inkscape"],
        "spotify": ["spotify"],
        "open spotify": ["spotify"],
        "vlc": ["vlc"],
        "open vlc": ["vlc"],
        
        # ============================================
        # UTILITIES
        # ============================================
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
        
        # ============================================
        # WEB APPS (via xdg-open)
        # ============================================
        "google": ["xdg-open", "https://www.google.com"],
        "open google": ["xdg-open", "https://www.google.com"],
        "github": ["xdg-open", "https://github.com"],
        "open github": ["xdg-open", "https://github.com"],
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
    }
}