# Contributing to SpeakEasy

Thank you for your interest in contributing! SpeakEasy is a community-driven project.

## Ways to Contribute

1. **Report bugs** - Open an issue with details
2. **Suggest features** - Share your ideas
3. **Submit PRs** - Code improvements
4. **Improve documentation** - Better guides
5. **Spread the word** - Share with others

## Development Setup

```bash
git clone https://github.com/Freedomwithin/SpeakEasy
cd SpeakEasy
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Code Style

- Follow PEP 8
- Add docstrings for functions
- Keep it lightweight (optimized for low-spec)

## Adding Commands

Edit `Program_Launcher/voice_assistant.py` or use the GUI settings manager.

## Building AppImage

```bash
ARCH=x86_64 appimagetool-x86_64.AppImage AppDir SpeakEasy-x86_64.AppImage
```

## License

MIT License - See LICENSE file.
