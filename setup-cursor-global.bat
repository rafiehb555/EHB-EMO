@echo off
echo Setting up Cursor Global Configuration...
echo.

REM Create main workspace directory
if not exist "C:\CursorWorkspace" (
    mkdir "C:\CursorWorkspace"
    echo Created C:\CursorWorkspace
)

REM Create subdirectories
if not exist "C:\CursorWorkspace\config" mkdir "C:\CursorWorkspace\config"
if not exist "C:\CursorWorkspace\packages" mkdir "C:\CursorWorkspace\packages"
if not exist "C:\CursorWorkspace\extensions" mkdir "C:\CursorWorkspace\extensions"
if not exist "C:\CursorWorkspace\projects" mkdir "C:\CursorWorkspace\projects"

echo Created directory structure in C:\CursorWorkspace

REM Set environment variables
setx CURSOR_GLOBAL_CONFIG "C:\CursorWorkspace\config"
setx GLOBAL_PACKAGES_PATH "C:\CursorWorkspace\packages"
setx SHARED_EXTENSIONS_PATH "C:\CursorWorkspace\extensions"

echo Set environment variables

REM Install global Node.js packages
echo Installing global Node.js packages...
npm install -g typescript eslint prettier nodemon concurrently cross-env dotenv

REM Install global Python packages
echo Installing global Python packages...
pip install virtualenv pytest black flake8 mypy

echo.
echo Cursor Global Configuration setup complete!
echo.
echo Next steps:
echo 1. Copy cursor-global-config.json to C:\CursorWorkspace\config\
echo 2. Restart Cursor
echo 3. Open any project folder - all tools will be available automatically
pause 