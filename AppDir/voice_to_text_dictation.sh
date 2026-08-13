#!/bin/bash
# Toggle SpeakEasy Dictation
# Bind this to Super + V in Cinnamon

# Get the directory where this script is located
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"

# Check if dictation is running (look for the correct script name)
if pgrep -f "python3.*voice_to_text_dictation.py" > /dev/null; then
    # Stop it
    pkill -f "python3.*voice_to_text_dictation.py"
    notify-send "SpeakEasy" "🛑 Dictation Disabled" -t 1500
else
    # Start it
    python3 voice_to_text_dictation.py > /dev/null 2>&1 &
    notify-send "SpeakEasy" "🎤 Dictation Active (Super+V to stop)" -t 2000
fi
