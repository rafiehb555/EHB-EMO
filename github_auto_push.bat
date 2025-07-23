@echo off
echo ========================================
echo    EHB-5 Auto Git Push Script
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git and try again
    pause
    exit /b 1
)

echo ✅ Git found
echo.

REM Check if we're in a git repository
git status >nul 2>&1
if errorlevel 1 (
    echo ❌ Not in a git repository
    echo Please run this script from your project directory
    pause
    exit /b 1
)

echo ✅ Git repository found
echo.

echo 🚀 Starting auto-push process...
echo.

REM Run the auto-push script
python auto_git_push.py

echo.
echo ✅ Auto-push script completed
pause
