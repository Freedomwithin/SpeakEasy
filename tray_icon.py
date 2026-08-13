import os
import sys
import threading
import subprocess
from PIL import Image, ImageDraw

TRAY_ICON = None
TRAY_THREAD = None
IS_ACTIVE = False

def create_icon_image(active=False):
    """Generates a dynamic 64x64 PIL image indicator (Green = Active, Red = Stopped)."""
    image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    color = (16, 185, 129, 255) if active else (239, 68, 68, 255)
    draw.ellipse((8, 8, 56, 56), fill=color)
    draw.ellipse((20, 20, 44, 44), fill=(255, 255, 255, 220))
    return image

def toggle_dictation_service(item=None):
    """Toggles dictation on or off from the system tray menu."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dictation_script = os.path.join(script_dir, "voice_to_text_dictation.py")

    # Check if dictation process is running
    p = subprocess.run(["pgrep", "-f", "voice_to_text_dictation.py"], capture_output=True)
    if p.returncode == 0:
        # Running -> Stop it
        subprocess.run(["pkill", "-f", "voice_to_text_dictation.py"])
    else:
        # Not running -> Start it
        subprocess.Popen([sys.executable, dictation_script])

def open_settings_gui(item=None):
    """Opens the Settings Manager GUI."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    settings_script = os.path.join(script_dir, "settings_gui.py")
    subprocess.Popen([sys.executable, settings_script])

def open_control_gui(item=None):
    """Opens the Control Center GUI."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    control_script = os.path.join(script_dir, "control_gui.py")
    subprocess.Popen([sys.executable, control_script])

def quit_application(icon, item):
    """Stops any running dictation and exits the system tray icon."""
    subprocess.run(["pkill", "-f", "voice_to_text_dictation.py"])
    if TRAY_ICON:
        TRAY_ICON.stop()

def init_tray():
    """Initializes pystray system tray icon with full interactive menu."""
    global TRAY_ICON
    try:
        import pystray
        from pystray import MenuItem as item, Menu

        menu = Menu(
            item("🎙️ Control Center", open_control_gui),
            item("⚡ Toggle Dictation", toggle_dictation_service),
            item("⚙️ Settings Manager", open_settings_gui),
            Menu.separator(),
            item("✕ Quit SpeakEasy", quit_application)
        )

        TRAY_ICON = pystray.Icon("SpeakEasy", create_icon_image(IS_ACTIVE), "SpeakEasy Voice Tools", menu)
        TRAY_ICON.run()
    except Exception as e:
        print(f"⚠️ Tray icon unavailable: {e}")

def set_tray_state(active=True):
    """Updates tray icon state (Green = Active, Red = Idle). Starts tray thread if needed."""
    global IS_ACTIVE, TRAY_ICON, TRAY_THREAD
    IS_ACTIVE = active

    if TRAY_ICON and hasattr(TRAY_ICON, 'icon'):
        TRAY_ICON.icon = create_icon_image(active)

    if TRAY_THREAD is None or not TRAY_THREAD.is_alive():
        TRAY_THREAD = threading.Thread(target=init_tray, daemon=True)
        TRAY_THREAD.start()

if __name__ == "__main__":
    init_tray()
