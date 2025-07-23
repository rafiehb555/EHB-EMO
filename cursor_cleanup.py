import json
import os
import shutil
from pathlib import Path
from typing import Dict, List

#!/usr/bin/env python3
"""
Cursor Environment Cleanup - Remove VS Code conflicts and optimize for Cursor
"""



class CursorCleanup:
    """Clean up VS Code conflicts and optimize for Cursor"""

    def __init__(self):
        self.project_root = Path(".")
        self.vscode_folders = []
        self.cursor_configs = []

    def find_vscode_artifacts(self):
        """Find all VS Code related files and folders"""
        print("🔍 Finding VS Code artifacts...")

        # VS Code folders to remove
        vscode_patterns = [
            ".vscode",
            ".vs",
            "*.code-workspace",
            ".vscodeignore",
            "launch.json",
            "tasks.json",
            "settings.json"
        ]

        # Find VS Code folders
        for pattern in vscode_patterns:
            if pattern.startswith("."):
                # Directory patterns
                for item in self.project_root.glob(f"**/{pattern}"):
                    if item.is_dir():
                        self.vscode_folders.append(item)
                        print(f"📁 Found VS Code folder: {item}")
            else:
                # File patterns
                for item in self.project_root.glob(f"**/{pattern}"):
                    if item.is_file():
                        self.vscode_folders.append(item)
                        print(f"📄 Found VS Code file: {item}")

        return len(self.vscode_folders)

    def create_cursor_config(self):
        """Create Cursor-specific configuration"""
        print("⚙️ Creating Cursor configuration...")

        # Create .cursorrules file
        cursor_rules = """# Cursor Rules for EHB-5 Project

## Code Style
- Use 4 spaces for Python indentation
- Use 2 spaces for CSS/HTML indentation
- Use single quotes for strings in JavaScript
- Use double quotes for strings in Python
- Always add trailing commas in objects/arrays

## File Organization
- Keep related files together
- Use descriptive file names
- Group imports at the top
- Add proper docstrings to functions

## Error Handling
- Use try-catch blocks appropriately
- Log errors with context
- Handle edge cases gracefully

## Performance
- Optimize imports
- Use efficient data structures
- Cache expensive operations
- Minimize DOM queries

## Security
- Validate all inputs
- Sanitize user data
- Use HTTPS in production
- Implement proper authentication

## Testing
- Write unit tests for functions
- Test edge cases
- Mock external dependencies
- Maintain good test coverage
"""

        with open(".cursorrules", "w", encoding="utf-8") as f:
            f.write(cursor_rules)

        print("✅ Created .cursorrules")

        # Create cursor-specific settings
        cursor_settings = {
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.fixAll.eslint": True,
                "source.organizeImports": True
            },
            "files.autoSave": "afterDelay",
            "files.autoSaveDelay": 1000,
            "editor.tabSize": 4,
            "editor.insertSpaces": True,
            "editor.rulers": [80, 120],
            "editor.wordWrap": "bounded",
            "editor.minimap.enabled": False,
            "workbench.colorTheme": "Default Dark+",
            "workbench.iconTheme": "vs-seti",
            "python.defaultInterpreterPath": "python",
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "python.formatting.provider": "black",
            "javascript.preferences.importModuleSpecifier": "relative",
            "typescript.preferences.importModuleSpecifier": "relative"
        }

        with open("cursor-settings.json", "w", encoding="utf-8") as f:
            json.dump(cursor_settings, f, indent=2)

        print("✅ Created cursor-settings.json")

    def remove_vscode_artifacts(self):
        """Remove VS Code artifacts"""
        print("🗑️ Removing VS Code artifacts...")

        removed_count = 0
        for item in self.vscode_folders:
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                print(f"✅ Removed: {item}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {item}: {e}")

        return removed_count

    def create_cursor_ignore(self):
        """Create .cursorignore file"""
        print("📝 Creating .cursorignore...")

        cursor_ignore = """# Cursor Ignore File

# VS Code artifacts
.vscode/
.vs/
*.code-workspace
.vscodeignore

# Node modules
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3

# Cache
.cache/
.mypy_cache/
.pytest_cache/

# Temporary files
*.tmp
*.temp
"""

        with open(".cursorignore", "w", encoding="utf-8") as f:
            f.write(cursor_ignore)

        print("✅ Created .cursorignore")

    def optimize_for_cursor(self):
        """Optimize project for Cursor development"""
        print("🚀 Optimizing for Cursor...")

        # Create cursor-specific scripts
        scripts = {
            "start-cursor.bat": """@echo off
echo 🚀 Starting EHB-5 with Cursor...
echo.
echo 📁 Opening project in Cursor...
cursor .
echo.
echo ✅ Project opened in Cursor!
pause""",

            "cursor-dev.bat": """@echo off
echo 🔧 Starting Cursor Development Environment...
echo.
echo 📦 Installing dependencies...
npm install
echo.
echo 🐍 Setting up Python environment...
python -m venv .venv
call .venv\\Scripts\\activate
pip install -r requirements.txt
echo.
echo 🚀 Starting development server...
python main.py
echo.
echo ✅ Development environment ready!
pause""",

            "cursor-clean.bat": """@echo off
echo 🧹 Cleaning Cursor Environment...
echo.
echo 🗑️ Removing cache files...
if exist __pycache__ rmdir /s /q __pycache__
if exist .mypy_cache rmdir /s /q .mypy_cache
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist node_modules rmdir /s /q node_modules
echo.
echo ✅ Environment cleaned!
pause"""
        }

        for filename, content in scripts.items():
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Created {filename}")

    def create_cursor_workspace(self):
        """Create Cursor workspace configuration"""
        print("⚙️ Creating Cursor workspace...")

        workspace_config = {
            "folders": [
                {
                    "name": "EHB-5 Project",
                    "path": "."
                }
            ],
            "settings": {
                "editor.formatOnSave": True,
                "editor.codeActionsOnSave": {
                    "source.fixAll.eslint": True,
                    "source.organizeImports": True
                },
                "files.autoSave": "afterDelay",
                "files.autoSaveDelay": 1000,
                "editor.tabSize": 4,
                "editor.insertSpaces": True,
                "editor.rulers": [80, 120],
                "editor.wordWrap": "bounded",
                "editor.minimap.enabled": False,
                "workbench.colorTheme": "Default Dark+",
                "workbench.iconTheme": "vs-seti",
                "python.defaultInterpreterPath": "python",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "python.formatting.provider": "black",
                "javascript.preferences.importModuleSpecifier": "relative",
                "typescript.preferences.importModuleSpecifier": "relative",
                "files.exclude": {
                    "**/__pycache__": True,
                    "**/.mypy_cache": True,
                    "**/.pytest_cache": True,
                    "**/node_modules": True,
                    "**/.venv": True,
                    "**/*.pyc": True,
                    "**/*.log": True
                }
            },
            "extensions": {
                "recommendations": [
                    "ms-python.python",
                    "ms-python.black-formatter",
                    "ms-python.pylint",
                    "ms-vscode.vscode-eslint",
                    "esbenp.prettier-vscode",
                    "bradlc.vscode-tailwindcss",
                    "ms-vscode.vscode-json",
                    "ms-vscode.vscode-css-peek",
                    "ms-vscode.vscode-html-css-support"
                ]
            }
        }

        with open("ehb-5.code-workspace", "w", encoding="utf-8") as f:
            json.dump(workspace_config, f, indent=2)

        print("✅ Created ehb-5.code-workspace")

    def run_cleanup(self):
        """Run complete Cursor cleanup"""
        print("🧹 Starting Cursor Environment Cleanup...")
        print("=" * 60)

        # Find VS Code artifacts
        artifact_count = self.find_vscode_artifacts()
        print(f"📊 Found {artifact_count} VS Code artifacts")

        # Remove VS Code artifacts
        removed_count = self.remove_vscode_artifacts()
        print(f"🗑️ Removed {removed_count} VS Code artifacts")

        # Create Cursor configuration
        self.create_cursor_config()
        self.create_cursor_ignore()
        self.optimize_for_cursor()
        self.create_cursor_workspace()

        print("=" * 60)
        print("🎉 Cursor Environment Cleanup Complete!")
        print("=" * 60)
        print("✅ Removed VS Code conflicts")
        print("✅ Created Cursor-specific configuration")
        print("✅ Optimized for Cursor development")
        print("✅ Created development scripts")
        print("=" * 60)
        print("🚀 Next Steps:")
        print("1. Open project in Cursor: cursor .")
        print("2. Use start-cursor.bat for quick start")
        print("3. Use cursor-dev.bat for development")
        print("4. Use cursor-clean.bat for cleanup")
        print("=" * 60)


def main():
    """Main function"""
    cleanup = CursorCleanup()
    cleanup.run_cleanup()


if __name__ == "__main__":
    main()
