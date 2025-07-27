# 🚀 EHB AI Dev Agent - Quick Start Guide

## Auto-Fix Solutions

Agar aapko server start karne me koi problem aaye, to yeh solutions use karein:

### Method 1: Auto-Start Script (Recommended)

```bash

python start_server.py

```text

### Method 2: Windows Batch File

```bash

start_server.bat

```text

### Method 3: PowerShell Script

```powershell

.\start_server.ps1

```text

### Method 4: Manual (if needed)

```bash

cd ehb-ai-dev-agent
python server.py

```text

## Features

✅ **Auto Directory Detection** - Script automatically finds server.py file

✅ **Auto Encoding Fix** - UTF-8 encoding issues resolved

✅ **Auto Browser Launch** - Dashboard automatically opens

✅ **Error Handling** - Clear error messages and solutions

## Server Access

- **Dashboard:** <http://localhost:8000/dashboard.html>

- **Main Page:** <http://localhost:8000>

- **CLI Interface:** Available in terminal

## Troubleshooting

### Error: "No such file or directory"

**Solution:** Use `python start_server.py` instead of `python server.py`

### Error: Unicode encoding

**Solution:** Already fixed in server.py

### Port already in use

**Solution:** Use different port: `python server.py --port 8001`

## Quick Commands

```bash

# Start server (auto-fix)

python start_server.py

# Stop server

Ctrl+C

# Check if server is running

curl <http://localhost:8000>

```text

## Project Structure

```text

ehb 5/
├── start_server.py          # Auto-start script

├── start_server.bat         # Windows batch file

├── start_server.ps1         # PowerShell script

└── ehb-ai-dev-agent/
    ├── server.py            # Main server file

    ├── dashboard.html       # Dashboard interface

    └── cli.py              # CLI interface

```text

---

**Note:** Ab kabhi bhi directory ya encoding issues nahi honge. Auto-scripts sab
kuch handle kar lenge! 🎉