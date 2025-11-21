@echo off
REM Suno Music Player Launcher
REM Automatically handles Python setup and dependencies

cls
echo.
echo =====================================
echo    SUNO MUSIC PLAYER
echo =====================================
echo.

cd /d "%~dp0"

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python 3.8+ not found!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    echo Try running this manually:
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo Launching Suno Music Player...
echo.

REM Launch the app
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo.
    pause
    exit /b 1
)

exit /b 0
