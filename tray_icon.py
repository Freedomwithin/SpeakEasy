#!/usr/bin/env python3
"""
SpeakEasy System Tray Icon
Shows status (green/red) and provides control menu
"""

import os
import sys
import threading
from pathlib import Path

try:
    import pystray
    from PIL import Image, ImageDraw
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False
    print("⚠️ pystray package not installed. Tray icon disabled.")

# Global state
_tray_icon = None
_tray_thread = None
_current_state = False  # False = stopped, True = active

def create_icon(state=False):
    """Create a colored circle icon (green=active, red=inactive)"""
    size = 64
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw circle
    color = (0, 255, 0) if state else (255, 0, 0)  # Green if active, Red if stopped
    draw.ellipse((8, 8, size-8, size-8), fill=color, outline=(255, 255, 255, 255))
    
    # Draw microphone symbol
    center = size // 2
    draw.rectangle((center-6, center-10, center+6, center+6), fill=(255, 255, 255))
    draw.ellipse((center-8, center-4, center+8, center+12), outline=(255, 255, 255), width=2)
    draw.ellipse((center-2, center-4, center+2, center+4), fill=(255, 255, 255))
    
    return image

def set_tray_state(state):
    """Update the tray icon state (True=active/green, False=stopped/red)"""
    global _current_state, _tray_icon
    _current_state = state
    if _tray_icon and PYSTRAY_AVAILABLE:
        _tray_icon.icon = create_icon(state)
        _tray_icon.update_menu()

def quit_tray():
    """Quit the tray icon"""
    global _tray_icon
    if _tray_icon:
        _tray_icon.stop()
        _tray_icon = None

def _run_tray():
    """Run the tray icon in a separate thread"""
    global _tray_icon
    if not PYSTRAY_AVAILABLE:
        return
    
    icon = pystray.Icon(
        "speakeasy",
        create_icon(False),
        "SpeakEasy",
        menu=pystray.Menu(
            pystray.MenuItem("Start Dictation", lambda: _tray_action("start")),
            pystray.MenuItem("Stop Dictation", lambda: _tray_action("stop")),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", lambda: _tray_action("quit"))
        )
    )
    _tray_icon = icon
    icon.run()

def _tray_action(action):
    """Handle tray menu actions"""
    global _tray_icon
    if action == "quit":
        quit_tray()
        os._exit(0)
    elif action == "start":
        # Start dictation (run the toggle script)
        import subprocess
        script_dir = Path(__file__).parent
        subprocess.Popen([str(script_dir / "voice_to_text_dictation.sh")])
    elif action == "stop":
        # Stop dictation (kill the process)
        import subprocess
        subprocess.Popen(["pkill", "-f", "voice_to_text_dictation.py"])

def start_tray():
    """Start the tray icon in a background thread"""
    global _tray_thread
    if not PYSTRAY_AVAILABLE:
        return
    
    if _tray_thread is None or not _tray_thread.is_alive():
        _tray_thread = threading.Thread(target=_run_tray, daemon=True)
        _tray_thread.start()

# Auto-start tray if script run directly
if __name__ == "__main__":
    start_tray()
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        quit_tray()
