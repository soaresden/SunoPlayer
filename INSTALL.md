# Installation Guide

Complete installation instructions for all platforms.

## Windows

### Option 1: Automatic (Easiest) ⭐

1. **Download** `launch.bat` 
2. **Double-click** it
3. **Done!** App launches automatically

### Option 2: Python Command Line

1. **Install Python 3.8+**
   - https://www.python.org/downloads/
   - ✓ Check "Add Python to PATH"
   - ✓ Click "Install Now"

2. **Download** this project (as ZIP)
   - Click green "Code" button → "Download ZIP"
   - Extract to a folder

3. **Open Command Prompt** in the folder
   ```bash
   cd path\to\suno-music-player
   pip install -r requirements.txt
   python main.py
   ```

### Option 3: via pip (Soon)

```bash
pip install suno-music-player
suno-player
```

---

## macOS

### Option 1: Command Line (Recommended)

1. **Install Python** (if not already)
   ```bash
   # Using Homebrew
   brew install python3
   
   # Or download: https://www.python.org/downloads/
   ```

2. **Clone or download** this project
   ```bash
   git clone https://github.com/yourusername/suno-music-player.git
   cd suno-music-player
   ```

3. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   python3 main.py
   ```

### Option 2: Create an App Bundle

```bash
# Create executable
pyinstaller --onefile --windowed --name "Suno Music Player" main.py

# App will be in: dist/Suno Music Player.app
```

### Option 3: via pip

```bash
pip3 install suno-music-player
suno-player
```

---

## Linux (Ubuntu/Debian)

### Prerequisites

```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk python3-dev
```

### Installation

1. **Clone the project**
   ```bash
   git clone https://github.com/yourusername/suno-music-player.git
   cd suno-music-player
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run**
   ```bash
   python3 main.py
   ```

### Create Desktop Shortcut

```bash
# Create .desktop file
cat > ~/.local/share/applications/suno-player.desktop << EOF
[Desktop Entry]
Type=Application
Name=Suno Music Player
Comment=Play your Suno music
Exec=/path/to/suno-music-player/venv/bin/python /path/to/suno-music-player/main.py
Icon=audio
Categories=Audio;
EOF

# Make executable
chmod +x ~/.local/share/applications/suno-player.desktop

# Add to menu (some DEs)
update-desktop-database ~/.local/share/applications
```

---

## Troubleshooting Installation

### "Command 'python' not found"

**Windows:**
- Download Python: https://www.python.org/downloads/
- During install: CHECK "Add Python to PATH"
- Restart Command Prompt

**macOS/Linux:**
```bash
# Use python3 instead
python3 --version
```

### "ModuleNotFoundError: No module named 'PyQt5'"

```bash
pip install -r requirements.txt

# Or manually:
pip install PyQt5==5.15.9
```

### "Permission denied" (macOS/Linux)

```bash
sudo chown -R $(whoami) ~/.suno_player
```

### "No module named 'selenium'"

```bash
pip install selenium
```

### "ChromeDriver not found"

The app tries to auto-download. If it fails:

```bash
# Download ChromeDriver
# https://chromedriver.chromium.org/

# Option 1: Add to PATH
export PATH=$PATH:./chromedriver

# Option 2: Same folder as script
cp chromedriver ./chromedriver
```

### Port already in use

Usually not an issue. If it is:

```bash
# Kill process using port 8000
# Windows
netstat -ano | findstr 8000
taskkill /PID <pid> /F

# macOS/Linux  
lsof -i :8000
kill -9 <pid>
```

---

## Advanced Installation

### Development Setup

```bash
git clone https://github.com/yourusername/suno-music-player.git
cd suno-music-player

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install with dev tools
pip install -r requirements.txt
pip install pylint black pytest

# Run
python main.py
```

### Docker Installation

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t suno-player .
docker run -it -e DISPLAY=$DISPLAY suno-player
```

---

## Updating

### If Already Installed

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run
python main.py
```

---

## Verification

After installation, verify everything works:

```bash
python main.py
```

You should see:
- ✓ Window appears
- ✓ "Enter token" dialog (first time)
- ✓ No error messages in console

---

## System Requirements

| Item | Requirement |
|------|-------------|
| **Python** | 3.8 or higher |
| **RAM** | 512 MB minimum |
| **Disk** | ~100 MB (+ dependencies) |
| **OS** | Windows 7+, macOS 10.12+, Ubuntu 18.04+ |
| **Audio** | Any output (speakers/headphones) |
| **Internet** | Required for API calls |

---

## Getting Help

- **Installation Issues** → GitHub Issues
- **Python Help** → https://www.python.org/
- **PyQt5 Help** → https://www.riverbankcomputing.com/
- **Suno API** → https://www.suno.ai

---

**✓ All set! Enjoy your music!** 🎵
