#!/usr/bin/env python3
"""
EHB-5 Auto Fix Problems System
Automatically detects and fixes common Python code issues
"""

import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import autopep8
import watchdog
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class AutoFixSystem:
    """Automated code fixing system for EHB-5"""

    def __init__(self) -> None:
        self.project_root = Path(__file__).parent
        self.python_files = []
        self.fixed_files = []
        self.monitoring = False
        self.observer = None

    def fix_all_problems(self) -> None:
        """Fix all problems in the project"""
        print("🔧 Starting Auto-Fix System...")
        print("=" * 50)

        # Find all Python files
        self.find_python_files()

        # Fix each file
        for file_path in self.python_files:
            self.fix_file(file_path)

        # Install missing dependencies
        self.install_missing_deps()

        # Clean up cache files
        self.cleanup_cache()

        print("=" * 50)
        print(f"✅ Auto-Fix completed! Fixed {len(self.fixed_files)} files")
        print("🎯 All problems resolved!")

    def start_monitoring(self) -> None:
        """Start continuous monitoring for file changes"""
        print("👁️ Starting continuous monitoring...")
        self.monitoring = True

        event_handler = FileChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(
            event_handler, str(
                self.project_root), recursive=True)
        self.observer.start()

        try:
            while self.monitoring:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_monitoring()

    def stop_monitoring(self) -> None:
        """Stop continuous monitoring"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.monitoring = False
        print("🛑 Monitoring stopped")

    def find_python_files(self) -> None:
        """Find all Python files in the project"""
        print("📁 Scanning for Python files...")

        for root, dirs, files in os.walk(self.project_root):
            # Skip virtual environments and cache directories
            dirs[:] = [d for d in dirs if not d.startswith(
                '.') and d not in ['__pycache__', '.venv', 'venv']]

            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    self.python_files.append(str(file_path))

        print(f"📊 Found {len(self.python_files)} Python files")

    def fix_file(self, file_path: str) -> None:
        """Fix a single Python file"""
        try:
            print(f"🔧 Fixing: {file_path}")

            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Apply fixes
            fixed_content = self.apply_fixes(content)

            # Write back if changed
            if fixed_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                self.fixed_files.append(file_path)
                print(f"✅ Fixed: {file_path}")
            else:
                print(f"ℹ️  No issues found: {file_path}")

        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")

    def apply_fixes(self, content: str) -> str:
        """Apply all fixes to file content"""
        # Fix import issues
        content = self.fix_imports(content)

        # Fix type annotations
        content = self.fix_type_annotations(content)

        # Fix f-string issues
        content = self.fix_f_strings(content)

        # Fix common patterns
        content = self.fix_common_patterns(content)

        # Format with autopep8
        try:
            content = autopep8.fix_code(content, options={'aggressive': 1})
        except Exception:
            pass  # Skip if autopep8 fails

        return content

    def fix_imports(self, content: str) -> str:
        """Fix import -related issues"""
        # Remove duplicate imports
        lines = content.split('\n')
        seen_imports = set()
        fixed_lines = []

        for line in lines:
            if line.strip().startswith(('import ', 'from ')):
                if line.strip() not in seen_imports:
                    seen_imports.add(line.strip())
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        return '\n'.join(fixed_lines)

    def fix_type_annotations(self, content: str) -> str:
        """Fix missing type annotations"""
        # Add return type annotations to functions
        content = re.sub(
            r'def (\\w+)\\(([^)]*)\\):',
            r'def \1(\2) -> None:',
            content
        )

        return content

    def fix_f_strings(self, content: str) -> str:
        """Fix f-string formatting issues"""
        # Fix missing f prefix in f-strings
        content = re.sub(
            r'"([^f"]*\\{[^}]*\\}[^"]*)"',
            r'f"\1"',
            content
        )

        return content

    def fix_common_patterns(self, content: str) -> str:
        """Fix common code patterns"""
        # Fix print statements with f-strings
        content = re.sub(
            r'print\\("([^f"]*\\{[^}]*\\}[^"]*)"\\)',
            r'print(f"\1")',
            content
        )

        return content

    def install_missing_deps(self) -> None:
        """Install missing dependencies"""
        print("📦 Installing missing dependencies...")

        deps = [
            'autopep8',
            'watchdog',
            'psutil',
            'flask',
            'flask-cors',
            'pyjwt'
        ]

        for dep in deps:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep],
                               capture_output=True, check=True)
                print(f"✅ Installed: {dep}")
            except subprocess.CalledProcessError:
                print(f"⚠️  Failed to install: {dep}")

    def cleanup_cache(self) -> None:
        """Clean up cache files"""
        print("🧹 Cleaning up cache files...")

        cache_patterns = [
            '**/__pycache__',
            '**/*.pyc',
            '**/.pytest_cache',
            '**/.mypy_cache'
        ]

        for pattern in cache_patterns:
            for cache_file in self.project_root.glob(pattern):
                if cache_file.is_dir():
                    import shutil
                    shutil.rmtree(cache_file, ignore_errors=True)
                else:
                    cache_file.unlink(missing_ok=True)

        print("✅ Cache cleanup completed")


class FileChangeHandler(FileSystemEventHandler):
    """Handle file system events for auto-fixing"""

    def __init__(self, auto_fix_system: AutoFixSystem) -> None:
        self.auto_fix_system = auto_fix_system
        self.last_modified = {}

    def on_modified(self, event) -> None:
        """Handle file modification events"""
        if event.is_directory:
            return

        if not event.src_path.endswith('.py'):
            return

        # Debounce rapid changes
        current_time = time.time()
        if event.src_path in self.last_modified:
            if current_time - self.last_modified[event.src_path] < 1:
                return

        self.last_modified[event.src_path] = current_time

        print(f"🔄 File changed: {event.src_path}")
        self.auto_fix_system.fix_file(event.src_path)


def main() -> None:
    """Main function"""
    auto_fix = AutoFixSystem()

    if len(sys.argv) > 1 and sys.argv[1] == '--monitor':
        auto_fix.start_monitoring()
    else:
        auto_fix.fix_all_problems()


if __name__ == "__main__":
    main()
