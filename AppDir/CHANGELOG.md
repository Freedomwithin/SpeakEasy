# Changelog

All notable changes to SpeakEasy will be documented in this file.

## [1.2.0] - 2026-08-13

### Added
- **GUI Categories** - Commands organized into: Apps, Browsers, Terminals, Files, Media, Dev Tools, Utilities, Web, Custom
- **Settings Toggles** - Voice Feedback, Comma Fix, Tray Icon in GUI
- **Screenshot** - SpeakEasy_Settings.png added to README
- **Better GUI Layout** - Clean, professional interface with category tabs

### Changed
- `settings_gui.py` - Complete redesign with categories and improved UX
- README - Added screenshot and updated GUI features section

## [1.1.0] - 2026-08-13

### Added
- **System Tray Icon** - Visual status indicator (green/red) with context menu
- **GUI Settings Manager** - Add, edit, and delete voice commands without touching code
- **Voice Feedback** - Audio confirmations using espeak/spd-say
- **GUI Error Dialogs** - User-friendly error popups using zenity
- **JSON Configuration** - Centralized config at `~/.config/speakeasy/config.json`
- **Config Manager** - Load and save settings programmatically
- **Tray State Control** - Dynamic status updates

### Changed
- `voice_assistant.py` - Integrated config_manager, tray, voice feedback, error dialogs
- `voice_to_text_dictation.py` - Integrated config, tray, voice feedback, error dialogs
- `install.sh` - Checks for espeak, zenity, pystray, Pillow
- `requirements.txt` - Added pystray, Pillow dependencies
- README - Updated with new features and documentation

### Fixed
- Module import paths for config_manager in Program_Launcher

## [1.0.0] - 2026-08-13

### Added
- Initial release
- Dictation engine with punctuation commands and auto-capitalization
- Program launcher with voice-activated application launch
- Hotkey toggles (Super+V for dictation, Super+A for launcher)
- Vosk model integration
- Clean Phrase Dump architecture
- MIT license
- Installation script
- Documentation

### Features
- Spoken punctuation: period, comma, question mark, exclamation point, new line, new paragraph, open/close paren, semi-colon, colon, hyphen, dash
- Automatic capitalization of sentences and "I"
- Toggleable fix for "comma" misheard as "come on"
- Fast Start pattern for launcher
- Cross-phrase capitalization
- Support for .desktop files via gtk-launch
- Dynamic Google search via "google <query>"