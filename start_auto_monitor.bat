@echo off
echo ========================================
echo    EHB-5 Auto Monitor Started
echo ========================================
echo.
echo 🔍 Monitoring for changes...
echo 📁 Repository: %CD%
echo ⏰ Checking every 30 seconds
echo.
echo Press Ctrl+C to stop monitoring
echo.

REM Start the auto-monitor
python auto_git_push.py --monitor --interval 30

echo.
echo 🛑 Auto-monitor stopped
pause
