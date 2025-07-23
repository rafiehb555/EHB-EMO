# Document Title

﻿# ðŸš€ Quick Start Guide - Cursor Global Configuration

## ðŸ“‹ Setup Steps

### 1. Run Setup Script (Choose One)

* *Option A - PowerShell (Recommended):**

```powershell

# Run as Administrator

.\setup-cursor-global.ps1

```

* *Option B - Batch Script:**

```cmd

setup-cursor-global.bat

```

* *Option C - Node.js:**

```bash

node global-package-manager.js

```

### 2. Verify Setup

```powershell

.\verify-setup.ps1

```

### 3. Restart Cursor

Close and reopen Cursor for all settings to take effect.

## ðŸŽ¯ What You Get

### âœ… Global Tools Available Everywhere

- **Node.js**: TypeScript, ESLint, Prettier, Nodemon, Yarn, pnpm
- **Python**: virtualenv, pytest, black, flake8, mypy
- **Package Managers**: npm, yarn, pnpm

### âœ… Extensions Auto-Loaded

- Language support for TypeScript, Python, Java, C++, Go, Rust, PHP, C#
- Development tools: Git, Docker, GitHub
- Code formatting and linting tools

### âœ… Centralized Workspace

- Location: `C:\CursorWorkspace\`
- All tools and packages managed from one place
- Environment variables set globally

## ðŸ“ Directory Structure

```

C:\CursorWorkspace\
â”œâ”€â”€ config\           # Global configuration files
â”œâ”€â”€ packages\         # Global packages and tools
â”œâ”€â”€ extensions\       # Shared extensions
â”œâ”€â”€ projects\         # Your project folders
â””â”€â”€ templates\        # Project templates

```

## ðŸš€ Usage

### Create New Project

```powershell

.\launch-project.ps1 my-new-project

```

### Open Any Folder

1. Open any folder in Cursor
2. All tools are automatically available
3. Run commands like `npm install`, `python script.py`, etc.

### Available Commands

```bash

npm init                    # Initialize new package.json
npm install                 # Install dependencies
npm run dev                 # Start development server
npm run build               # Build project
npm run test                # Run tests
npm run lint                # Run ESLint
npm run format              # Format code with Prettier

```

## ðŸ”§ Environment Variables Set

- `CURSOR_GLOBAL_CONFIG` = `C:\CursorWorkspace\config`
- `GLOBAL_PACKAGES_PATH` = `C:\CursorWorkspace\packages`
- `SHARED_EXTENSIONS_PATH` = `C:\CursorWorkspace\extensions`
- `NODE_ENV` = `development`

## ðŸ› ï¸ Troubleshooting

### If tools aren't available

1. Run `.\verify-setup.ps1` to check status
2. Run setup script again as Administrator
3. Restart Cursor

### If extensions aren't loading

1. Check `SHARED_EXTENSIONS_PATH` environment variable
2. Restart Cursor
3. Reinstall extensions if needed

## ðŸ“ž Support Files

- `cursor-global-config.json` - Main configuration
- `cursor-settings.json` - Cursor editor settings
- `setup-cursor-global.ps1` - PowerShell setup script
- `verify-setup.ps1` - Verification script
- `launch-project.ps1` - Project launcher

- --

* *ðŸŽ‰ After setup, you'll never need to reinstall tools again!**
