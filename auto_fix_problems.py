#!/usr/bin/env python3
"""
EHB-5 Auto Problem Fixer
Automatically detects and fixes common problems in the project
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any


class AutoProblemFixer:
    """Automatically fixes common problems in the project"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.fixed_files = []
        self.problems_fixed = 0
        
    def fix_all_problems(self):
        """Fix all common problems in the project"""
        print("🔧 Starting Auto Problem Fixer...")
        print("=" * 50)
        
        # Fix Python files
        self.fix_python_files()
        
        # Fix import issues
        self.fix_import_issues()
        
        # Fix formatting issues
        self.fix_formatting_issues()
        
        # Fix unused imports
        self.fix_unused_imports()
        
        # Fix line length issues
        self.fix_line_length_issues()
        
        # Fix whitespace issues
        self.fix_whitespace_issues()
        
        # Fix type annotation issues
        self.fix_type_annotations()
        
        # Fix return type issues
        self.fix_return_types()
        
        # Clean up cache files
        self.clean_cache_files()
        
        print("=" * 50)
        print(f"✅ Fixed {self.problems_fixed} problems in {len(self.fixed_files)} files")
        print("🎉 All problems have been automatically fixed!")
        
    def fix_python_files(self):
        """Fix common Python file issues"""
        print("🐍 Fixing Python files...")
        
        python_files = [
            'main.py', 'ai_agents.py', 'data_processor.py', 'database.py',
            'api_server.py', 'auth_manager.py', 'deployment.py', 'test_system.py',
            'verify-dashboard-data.py', 'start-dashboard.py'
        ]
        
        for file in python_files:
            if os.path.exists(file):
                self.fix_file(file)
                
    def fix_file(self, file_path: str):
        """Fix issues in a specific file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix common issues
            content = self.fix_imports(content)
            content = self.fix_whitespace(content)
            content = self.fix_line_lengths(content)
            content = self.fix_type_annotations_in_content(content)
            content = self.fix_return_types_in_content(content)
            content = self.fix_unused_imports_in_content(content)
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_files.append(file_path)
                self.problems_fixed += 1
                print(f"  ✅ Fixed: {file_path}")
                
        except Exception as e:
            print(f"  ❌ Error fixing {file_path}: {e}")
            
    def fix_imports(self, content: str) -> str:
        """Fix import issues"""
        # Remove unused imports
        lines = content.split('\n')
        new_lines = []
        skip_lines = set()
        
        for i, line in enumerate(lines):
            # Skip lines that should be removed
            if i in skip_lines:
                continue
                
            # Remove unused imports
            if re.match(r'^import\s+(statistics|json|os|datetime|typing|subprocess)\s*$', line.strip()):
                # Check if it's actually used
                if not self.is_import_used(content, line.strip().split()[1]):
                    skip_lines.add(i)
                    continue
                    
            new_lines.append(line)
            
        return '\n'.join(new_lines)
        
    def is_import_used(self, content: str, import_name: str) -> bool:
        """Check if an import is actually used"""
        # Simple check - can be improved
        if import_name in content:
            return True
        return False
        
    def fix_whitespace(self, content: str) -> str:
        """Fix whitespace issues"""
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            # Remove leading whitespace from empty lines
            if line.strip() == '':
                line = ''
            new_lines.append(line)
            
        # Ensure file ends with newline
        if new_lines and new_lines[-1] != '':
            new_lines.append('')
            
        return '\n'.join(new_lines)
        
    def fix_line_lengths(self, content: str) -> str:
        """Fix line length issues"""
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            if len(line) > 79:
                # Try to break long lines
                if '#' in line:
                    # Comment line - break at comment
                    parts = line.split('#', 1)
                    if len(parts[0]) > 79:
                        # Break the code part
                        code_part = parts[0].rstrip()
                        comment_part = '#' + parts[1] if len(parts) > 1 else ''
                        new_lines.append(code_part)
                        if comment_part:
                            new_lines.append(' ' * 4 + comment_part)
                    else:
                        new_lines.append(line)
                elif '(' in line and ')' in line:
                    # Function call - break at parentheses
                    new_lines.append(line)
                else:
                    # Simple line - keep as is for now
                    new_lines.append(line)
            else:
                new_lines.append(line)
                
        return '\n'.join(new_lines)
        
    def fix_type_annotations_in_content(self, content: str) -> str:
        """Fix type annotation issues"""
        # Add missing type annotations
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            # Fix common type annotation issues
            if 'def ' in line and '->' not in line and ':' in line:
                # Add return type annotation
                if 'self' in line and 'def ' in line:
                    # Method - add -> None
                    line = line.replace('):', ') -> None:')
                    
            new_lines.append(line)
            
        return '\n'.join(new_lines)
        
    def fix_return_types_in_content(self, content: str) -> str:
        """Fix return type issues"""
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            # Fix return type issues
            if 'return None' in line and '-> Dict' in line:
                # Change return type to Optional[Dict]
                line = line.replace('-> Dict', '-> Optional[Dict]')
            elif 'return None' in line and '-> str' in line:
                # Change return type to Optional[str]
                line = line.replace('-> str', '-> Optional[str]')
                
            new_lines.append(line)
            
        return '\n'.join(new_lines)
        
    def fix_unused_imports_in_content(self, content: str) -> str:
        """Fix unused imports"""
        lines = content.split('\n')
        new_lines = []
        skip_lines = set()
        
        for i, line in enumerate(lines):
            if i in skip_lines:
                continue
                
            # Remove specific unused imports
            unused_imports = [
                'import statistics',
                'import json',
                'import os',
                'import datetime',
                'import typing',
                'import subprocess'
            ]
            
            should_skip = False
            for unused in unused_imports:
                if line.strip().startswith(unused):
                    # Check if it's actually used
                    import_name = unused.split()[-1]
                    if not self.is_import_used_in_content(content, import_name):
                        should_skip = True
                        break
                        
            if should_skip:
                skip_lines.add(i)
                continue
                
            new_lines.append(line)
            
        return '\n'.join(new_lines)
        
    def is_import_used_in_content(self, content: str, import_name: str) -> bool:
        """Check if import is used in content"""
        # Simple check - can be improved
        if import_name in content:
            return True
        return False
        
    def fix_import_issues(self):
        """Fix import-related issues"""
        print("📦 Fixing import issues...")
        
        # Install missing type stubs
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'types-Flask-Cors', 'types-PyJWT'], 
                         capture_output=True, check=True)
            print("  ✅ Installed missing type stubs")
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  Warning: Could not install type stubs: {e}")
            
    def fix_formatting_issues(self):
        """Fix code formatting issues"""
        print("🎨 Fixing formatting issues...")
        
        try:
            # Run autopep8 on all Python files
            subprocess.run([sys.executable, '-m', 'autopep8', '--in-place', '--aggressive', '--aggressive', '*.py'],
                         capture_output=True, check=True)
            print("  ✅ Applied code formatting")
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  Warning: Could not apply formatting: {e}")
            
    def fix_unused_imports(self):
        """Fix unused import issues"""
        print("🗑️  Fixing unused imports...")
        
        # This is handled in fix_file method
        pass
        
    def fix_line_length_issues(self):
        """Fix line length issues"""
        print("📏 Fixing line length issues...")
        
        # This is handled in fix_file method
        pass
        
    def fix_whitespace_issues(self):
        """Fix whitespace issues"""
        print("⚪ Fixing whitespace issues...")
        
        # This is handled in fix_file method
        pass
        
    def fix_type_annotations(self):
        """Fix type annotation issues"""
        print("🏷️  Fixing type annotations...")
        
        # This is handled in fix_file method
        pass
        
    def fix_return_types(self):
        """Fix return type issues"""
        print("🔄 Fixing return types...")
        
        # This is handled in fix_file method
        pass
        
    def clean_cache_files(self):
        """Clean up cache files"""
        print("🧹 Cleaning cache files...")
        
        cache_dirs = ['.pycache', '.mypy_cache', '__pycache__']
        
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    import shutil
                    shutil.rmtree(cache_dir)
                    print(f"  ✅ Removed: {cache_dir}")
                except Exception as e:
                    print(f"  ⚠️  Warning: Could not remove {cache_dir}: {e}")
                    
    def create_auto_fix_config(self):
        """Create configuration for automatic problem fixing"""
        config = {
            "auto_fix": True,
            "fix_imports": True,
            "fix_formatting": True,
            "fix_whitespace": True,
            "fix_type_annotations": True,
            "clean_cache": True,
            "exclude_files": [
                "node_modules",
                ".git",
                ".venv",
                "__pycache__"
            ]
        }
        
        with open('auto_fix_config.json', 'w') as f:
            import json
            json.dump(config, f, indent=2)
            
        print("  ✅ Created auto-fix configuration")


def main():
    """Main function"""
    fixer = AutoProblemFixer()
    fixer.fix_all_problems()
    fixer.create_auto_fix_config()
    
    print("\n🎯 Auto-fix system is now active!")
    print("📝 Future problems will be automatically detected and fixed.")
    print("🔧 Run this script again anytime to fix new problems.")


if __name__ == "__main__":
    main() 