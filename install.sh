#!/bin/bash
# SpeakEasy Installer
# Sets up the virtual environment and makes scripts executable

set -e

echo "========================================="
echo "  SpeakEasy - Voice Tools Installer"
echo "========================================="
echo ""

# Get the directory where this script is located
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Parse optional flags
WITH_TRAY=false
WITH_GUI=false

for arg in "$@"; do
    case $arg in
        --with-tray)
            WITH_TRAY=true
            shift
            ;;
        --with-gui)
            WITH_GUI=true
            shift
            ;;
        --all)
            WITH_TRAY=true
            WITH_GUI=true
            shift
            ;;
    esac
done

# Check Python version
echo "Checking Python version..."
python3 --version

# Check system dependencies (espeak, zenity)
echo ""
echo "Checking system feedback tools..."
if command -v espeak &> /dev/null; then
    echo "  [✓] espeak found (voice feedback enabled)"
else
    echo "  [!] espeak missing (optional for spoken feedback: 'sudo apt install espeak')"
fi

if command -v zenity &> /dev/null; then
    echo "  [✓] zenity found (GUI error dialogs enabled)"
else
    echo "  [!] zenity missing (optional for GUI dialogs: 'sudo apt install zenity')"
fi

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping."
else
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate and install dependencies
echo ""
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Check if model exists
echo ""
echo "Checking Vosk model..."
if [ -d "vosk-model-small-en-us-0.15" ]; then
    echo "Model found."
else
    echo "WARNING: Vosk model not found!"
    echo "Please download it from: https://alphacephei.com/vosk/models/"
    echo "Extract it to: $DIR/vosk-model-small-en-us-0.15/"
fi

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x voice_to_text_dictation.sh
chmod +x Program_Launcher/start_voice_assistant.sh
chmod +x settings_gui.py

echo ""
echo "========================================="
echo "  Installation Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Set up hotkeys in your Desktop Environment:"
echo "   Super+V -> $DIR/voice_to_text_dictation.sh"
echo "   Super+A -> $DIR/Program_Launcher/start_voice_assistant.sh"
echo ""
echo "2. Launch Settings GUI manager:"
echo "   ./venv/bin/python3 $DIR/settings_gui.py"
echo ""
echo "3. Edit configuration anytime at:"
echo "   ~/.config/speakeasy/config.json"
echo ""
