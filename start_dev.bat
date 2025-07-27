@echo off
echo Starting EHB AI Dev Environment...
echo.

echo Starting Backend Server...
cd backend
start "Backend Server" cmd /k "npm run dev"

echo Starting Frontend Server...
cd ../frontend
start "Frontend Server" cmd /k "npm run dev"

echo.
echo EHB AI Dev Environment is starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
pause
