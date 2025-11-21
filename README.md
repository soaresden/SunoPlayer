# 🎵 Suno Music Player

A beautiful, fully-featured desktop application to browse, play, and download your Suno.ai music directly.

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green)](https://pypi.org/project/PyQt5/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

✅ **Automatic Authentication** - One-click login with automatic token capture
✅ **Browse Workspaces** - Organize music by projects/workspaces
✅ **Beautiful UI** - Modern PyQt5 interface with professional design
✅ **Audio Player** - Built-in player with play/pause/stop/volume controls
✅ **Download Manager** - Download tracks as MP3 with progress tracking
✅ **System Tray** - Minimize to tray, control from taskbar
✅ **Token Caching** - Automatic token refresh and validation
✅ **Cross-Platform** - Works on Windows, macOS, and Linux

## 📸 Screenshots

```
┌─────────────────────────────────────────────────────────┐
│ Suno Music Player - john_doe@example.com                │
├─────────────────────────────────────────────────────────┤
│ Workspace: [My Workspace ▼] [🔄 Refresh] [🔐 Re-login] │
│                                                         │
│ # │ Title               │ Status │ Created    │ Dur    │
│───┼─────────────────────┼────────┼────────────┼────── │
│ 1 │ Ambient Dreams      │ ✓ OK   │ 2025-01-15 │ 180s  │
│ 2 │ Electric Vibes      │ ✓ OK   │ 2025-01-14 │ 210s  │
│ 3 │ Lofi Hip Hop        │ ⌛ Gen │ 2025-01-14 │ N/A   │
│   │                     │        │            │       │
├─────────────────────────────────────────────────────────┤
│ Selected: Ambient Dreams (success)                      │
│ [▶ Play] [⏸ Pause] [⏹ Stop] [Volume ━━●━━] [⬇ DL]     │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Internet connection** - For API calls and music streaming

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/suno-music-player.git
cd suno-music-player
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the App

**Option 1: Windows (Easiest)**
```bash
Double-click launch.bat
```

**Option 2: Command Line**
```bash
python main.py
```

**Option 3: Manual Setup**
```bash
# Install dependencies if not done yet
pip install -r requirements.txt

# Run the application
python main.py
```

## 🔐 Authentication

### First Launch

The app automatically handles authentication:

1. **First time launch** → Browser opens automatically
2. **Login to Suno** → Use your Suno account credentials
3. **Token captured** → The app extracts your token automatically
4. **Token saved** → Stored securely in `~/.suno_player/token.json`

### Manual Token Entry

If automatic authentication fails, you can manually enter your token:

1. Go to https://suno.com/create
2. Press `F12` (Developer Tools)
3. Go to **Network** tab
4. Refresh the page
5. Look for a request to `api/project/me`
6. Click it → **Headers** tab
7. Find `Authorization: Bearer eyJh...`
8. Copy the token (everything after `Bearer `)
9. Paste it when the app asks

### Token Management

- Tokens are stored in: `~/.suno_player/token.json`
- Tokens expire after ~1 hour
- **Re-login**: Click "🔐 Re-login" button in the app
- **Manual clear**: Delete `~/.suno_player/token.json` and restart

## 🎵 How to Use

### Browse & Play

1. **Select Workspace** - Choose from dropdown at the top
2. **View Tracks** - Table shows all songs with:
   - ✓ OK = Ready to play
   - ⌛ Gen = Still generating
   - ✗ Error = Failed
3. **Click a Track** - Selects it for playback
4. **Play** - Click "▶ Play" button

### Playback Controls

| Button | Action |
|--------|--------|
| ▶ Play | Start playback |
| ⏸ Pause | Pause/Resume |
| ⏹ Stop | Stop and reset |
| Volume | Adjust volume |

### Download Music

1. **Select a track** (must have ✓ OK status)
2. **Click "⬇ Download"**
3. **Choose folder** where to save
4. **Wait** for download to complete
5. **Done!** MP3 file is saved

### System Tray

- **Minimize** - Window → Taskbar tray
- **Show** - Double-click tray icon
- **Controls** - Right-click tray icon for quick menu
- **Close App** - "Exit" in tray menu

## 🔧 Configuration

The app stores its config in: `~/.suno_player/`

```
~/.suno_player/
├── token.json          # Your authentication token
├── icon.png           # Application icon
└── temp_play.mp3      # Temporary playback file
```

### Security Notes

- Tokens are stored **locally only** on your computer
- Tokens are **never** sent to third-party services
- You can safely share code - your token stays on your machine

## 📋 System Requirements

| Component | Requirement |
|-----------|-------------|
| Python | 3.8 or higher |
| RAM | 512 MB minimum |
| Storage | ~100 MB (including dependencies) |
| OS | Windows 7+, macOS 10.12+, Linux |
| Audio | Any output device (optional, for playback) |

## 🐛 Troubleshooting

### "Python not found"
```
1. Download Python: https://www.python.org/downloads/
2. During installation: CHECK "Add Python to PATH"
3. Restart your computer
4. Try again
```

### "ModuleNotFoundError: No module named 'PyQt5'"
```
Run: pip install -r requirements.txt
```

### "Selenium Chrome driver not found"
```
The app will try to auto-download. If not:
1. Download ChromeDriver: https://chromedriver.chromium.org/
2. Add to PATH or same folder as script
```

### "No sound during playback"
```
1. Check speaker is not muted
2. Check volume slider in app
3. Try another track
4. Restart app
```

### "Cannot authenticate / Token invalid"
```
1. Click "🔐 Re-login" button
2. Allow browser to fully load Suno.com
3. Login with your Suno account
4. Wait for token capture message
```

### "App crashes on startup"
```
1. Delete ~/.suno_player/ folder
2. Restart app
3. Re-authenticate
```

## 🛠️ Development

### Project Structure

```
suno-music-player/
├── main.py              # Main application window
├── auth.py              # Authentication handler
├── api.py               # Suno API client
├── requirements.txt     # Python dependencies
├── launch.bat          # Windows launcher
├── README.md           # Documentation
└── LICENSE             # MIT License
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Ideas for Improvements

- [ ] Playlist management
- [ ] Search/filter tracks
- [ ] Shuffle/repeat modes
- [ ] Volume normalization
- [ ] Equalizer
- [ ] Track queue
- [ ] Bulk download
- [ ] Song editing metadata
- [ ] macOS native integration
- [ ] Dark mode theme

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Denis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
...
```

## ⚖️ Legal Notice

This application is **not affiliated with Suno.ai**. 

- Suno is a trademark of Suno Inc.
- This tool is for personal use only
- Respect Suno's Terms of Service
- This tool provides access to your own music
- Do not use to violate copyright or terms

## 🙏 Acknowledgments

- [Suno.ai](https://www.suno.ai) - Music generation platform
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [pygame](https://www.pygame.org/) - Audio playback
- [Selenium](https://www.selenium.dev/) - Browser automation

## 📞 Support

- **Issues** - Open an issue on GitHub
- **Questions** - Start a discussion
- **Suggestions** - Feature requests welcome!

## 🔄 Updates

The app will work with the current Suno API. If Suno makes breaking changes:

1. Check GitHub for updates
2. Pull latest version
3. Run `pip install -r requirements.txt` (again if needed)
4. Restart app

---

**Made with ❤️ for music lovers**

⭐ If you like this project, please give it a star! It helps others discover it.
