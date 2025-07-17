# 🍅 Pomodoro Pro

A clean, minimal Pomodoro Timer built with Python and Tkinter. Stay focused, be productive.

## Features

- **Classic Pomodoro Technique**: 25-minute work sessions with short and long breaks
- **System Tray Integration**: Minimize to tray and control from anywhere
- **Desktop Notifications**: Get notified when sessions end
- **Light/Dark Theme**: Switch between themes for comfort
- **Animated Interface**: Smooth animations to keep you engaged
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites
```bash
pip install pillow pystray plyer
```

### Run from Source
```bash
git clone https://github.com/yourusername/pomodoro-pro
cd pomodoro-pro
python pomodoro_timer.py
```

### Build Executable

**Using auto-py-to-exe (Recommended)**
```bash
pip install auto-py-to-exe
auto-py-to-exe
```

Settings in auto-py-to-exe:
- **Script Location**: Select `pomodoro_timer.py`
- **Onefile**: One File
- **Console Window**: Window Based (hide the console)
- **Additional Files**: Add `cats.png` and `cat-cat-snore.gif` (if you have them)

**Or using PyInstaller directly**
```bash
pyinstaller --onefile --windowed --add-data "cats.png;." --add-data "cat-cat-snore.gif;." pomodoro_timer.py
```

## Usage

1. **Set your timers**: Work duration, short break, and long break (in minutes)
2. **Click Start**: Begin your focused work session
3. **Follow the flow**: Work → Short Break → Work → Short Break → Work → Long Break
4. **Stay in the zone**: Every 4th session triggers a longer break

### Default Settings
- Work: 25 minutes
- Short Break: 5 minutes  
- Long Break: 15 minutes

## Controls

- **▶ Start**: Begin the Pomodoro cycle
- **■ Stop**: Pause the current session
- **⟳ Reset**: Reset timer and session count
- **🌗 Toggle Theme**: Switch between light and dark modes

## System Tray

Right-click the tray icon for quick access:
- Start/Stop sessions
- Reset timer
- Quit application

## Optional Assets

Place these files in the same directory for enhanced experience:
- `cats.png` - Logo image (100x120px recommended)
- `cat-cat-snore.gif` - Animated mascot (200x200px recommended)

*App works perfectly without these files - colored fallbacks are provided.*

## Dependencies

- **tkinter** - GUI framework (built-in with Python)
- **Pillow** - Image processing
- **pystray** - System tray integration
- **plyer** - Desktop notifications (optional)
- **winsound** - Audio alerts on Windows (optional)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This is an open source project.

## Acknowledgments

- Built with the [Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique) by Francesco Cirillo
- Icons and emojis for a delightful user experience

---

🧑‍💻 Built By

Harsh Bhimra — Student. DevOps Learner. Python dude. Cat enjoyer.
Give it a ⭐ if this made you 1% more productive.

**Stay focused. Stay productive. 🍅**
