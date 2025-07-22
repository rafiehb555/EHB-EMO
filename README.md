# EHB-5 Repository - Global Cursor Configuration

This repository contains a comprehensive setup for centralized Cursor configuration that allows you to use all tools, extensions, and packages globally across all projects.

## 🚀 Quick Setup

### Option 1: Automatic Setup (Recommended)
```bash
# Run the batch script
setup-cursor-global.bat

# Or run the Node.js script
node global-package-manager.js
```

### Option 2: Manual Setup
1. Copy `cursor-global-config.json` to `C:\CursorWorkspace\config\`
2. Copy `cursor-settings.json` to your Cursor settings
3. Run the setup scripts

## 📁 Directory Structure

```
C:\CursorWorkspace\
├── config\           # Global configuration files
├── packages\         # Global packages and tools
├── extensions\       # Shared extensions
├── projects\         # Your project folders
└── templates\        # Project templates
```

## 🔧 Features

### ✅ Global Tools & Packages
- **Node.js**: TypeScript, ESLint, Prettier, Nodemon, etc.
- **Python**: Virtualenv, Pytest, Black, Flake8, MyPy
- **Package Managers**: npm, yarn, pnpm

### ✅ Extensions
- Language support for TypeScript, Python, Java, C++, Go, Rust, PHP, C#
- Development tools: Git, Docker, GitHub
- Code formatting: Prettier, ESLint
- Themes and icons

### ✅ Environment Variables
- `CURSOR_GLOBAL_CONFIG`: Points to global config directory
- `GLOBAL_PACKAGES_PATH`: Points to global packages
- `SHARED_EXTENSIONS_PATH`: Points to shared extensions

## 🎯 Benefits

1. **No Reinstallation**: All tools available in any new project
2. **Centralized Management**: One place to manage all tools
3. **Consistent Environment**: Same setup across all projects
4. **Time Saving**: No need to install tools for each project

## 📋 Usage

### Creating New Projects
```bash
# Navigate to your project folder
cd C:\CursorWorkspace\projects\my-new-project

# All tools are already available!
npm init
npm install
npm run dev
```

### Global Commands
All commands run from the centralized workspace:
- `npm` commands use global packages
- `python` commands use global interpreters
- Extensions are shared across all projects

## 🔄 Maintenance

### Adding New Tools
1. Edit `cursor-global-config.json`
2. Add to the appropriate section
3. Run setup script to install

### Updating Tools
```bash
# Update global packages
npm update -g

# Update Python packages
pip install --upgrade package-name
```

## 📝 Configuration Files

- `cursor-global-config.json`: Main configuration file
- `cursor-settings.json`: Cursor editor settings
- `setup-cursor-global.bat`: Windows setup script
- `global-package-manager.js`: Node.js setup script

## 🛠️ Troubleshooting

### If tools aren't available:
1. Check environment variables are set
2. Restart Cursor
3. Verify paths in configuration files

### If extensions aren't loading:
1. Check `SHARED_EXTENSIONS_PATH` environment variable
2. Restart Cursor
3. Reinstall extensions if needed

## 📞 Support

For issues or questions about the global configuration setup, please check the configuration files or run the setup scripts again.

---

**Note**: This setup creates a centralized workspace at `C:\CursorWorkspace\` where all tools, packages, and extensions are managed globally. 