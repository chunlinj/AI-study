@echo off
echo ========================================
echo Discord to Kiro Bridge
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM 检查环境变量
if "%DISCORD_BOT_TOKEN%"=="" (
    echo Warning: DISCORD_BOT_TOKEN not set!
    echo Please set it first:
    echo set DISCORD_BOT_TOKEN=your_token_here
    echo.
    pause
)

echo Starting Discord Bot...
start "Discord Bot" cmd /k python discord_to_kiro_bridge.py

timeout /t 2 /nobreak >nul

echo Starting File Watcher...
start "File Watcher" cmd /k python kiro_file_watcher.py

echo.
echo ========================================
echo Bridge started successfully!
echo ========================================
echo.
echo Two windows opened:
echo 1. Discord Bot - Receives messages
echo 2. File Watcher - Monitors and copies to clipboard
echo.
echo Send messages in Discord to interact with Kiro!
echo.
pause
