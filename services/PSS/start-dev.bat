@echo off
echo Starting PSS Development Server...
cd pss
if exist package.json (
    echo Found package.json, starting development server...
    npm run dev
) else (
    echo Error: package.json not found in pss directory
    echo Current directory: %CD%
    pause
) 