#!/bin/bash
# Launch SpeakEasy Program Launcher
# Bind this to Super + A in Cinnamon

# Get the directory where this script is located
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"

# Instant notification
notify-send "SpeakEasy" "Listening for app command..." -t 1500

# Run the launcher
python3 voice_assistant.py
