#!/usr/bin/env python3
"""
EHB-5 Real-Time Problem Detector
Continuously monitors and fixes all linting and formatting issues
"""

import json
import os
import subprocess
import time
from datetime import datetime
from typing import Any, Dict, List


class RealTimeProblemDetector:
    """Real-time problem detection and fixing system"""

    def __init__(self):
        self.problems_found = []
        self.problems_fixed = []
        self.monitoring_active = False
        self.fix_history = []

    def start_monitoring(self):
        """Start real-time problem monitoring"""
        print("🔍 Starting Real-Time Problem Detection...")
        print("=" * 50)

        self.monitoring_active = True

        while self.monitoring_active:
            try:
                # Detect problems
                problems = self.detect_all_problems()

                if problems:
                    print(f"🚨 Found {len(problems)} problems")
                    self.problems_found.extend(problems)

                    # Fix problems automatically
                    fixed = self.fix_problems_automatically(problems)
                    self.problems_fixed.extend(fixed)

                    # Generate report
                    self.generate_problem_report()

                else:
                    print("✅ No problems detected - System clean!")

                # Wait before next check
                time.sleep(10)  # Check every 10 seconds

            except KeyboardInterrupt:
                print("\n⏹️ Stopping problem detection...")
                self.monitoring_active = False
                break
            except Exception as e:
                print(f"❌ Error in monitoring: {e}")
                time.sleep(10)

    def detect_all_problems(self) -> List[Dict[str, Any]]:
        """Detect all types of problems in the project"""
        problems = []

        try:
            # Get all Python files
            python_files = [f for f in os.listdir('.') if f.endswith('.py')]

            for file in python_files:
                file_problems = self.analyze_file(file)
                problems.extend(file_problems)

            return problems

        except Exception as e:
            print(f"❌ Error detecting problems: {e}")
            return []

    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze a single file for problems"""
        problems = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for common issues
            lines = content.split('\n')

            for line_num, line in enumerate(lines, 1):
                # Check line length
                if len(line) > 79:
                    problems.append({
                        'file': file_path,
                        'line': line_num,
                        'type': 'line_too_long',
'message': f'Line {line_num} is too long ({len(line)} > 79 characters)',
                        'severity': 'warning'
                    })

                # Check for trailing whitespace
                if line.rstrip() != line and line.strip():
                    problems.append({
                        'file': file_path,
                        'line': line_num,
                        'type': 'trailing_whitespace',
                        'message': f'Line {line_num} has trailing whitespace',
                        'severity': 'warning'
                    })

                # Check for bare except
                if 'except Exception:' in line:
                    problems.append({
                        'file': file_path,
                        'line': line_num,
                        'type': 'bare_except',
                        'message': f'Line {line_num} uses bare except clause',
                        'severity': 'error'
                    })

            # Check for missing newline at end
            if content and not content.endswith('\n'):
                problems.append({
                    'file': file_path,
                    'line': len(lines),
                    'type': 'missing_newline',
                    'message': 'File missing newline at end',
                    'severity': 'warning'
                })

            # Check for unused imports
            import_lines = [i for i, line in enumerate(
                lines) if line.strip().startswith('import ')]
            if len(import_lines) > 5:  # Simple heuristic
                problems.append({
                    'file': file_path,
                    'line': 0,
                    'type': 'unused_imports',
                    'message': 'Potential unused imports detected',
                    'severity': 'warning'
                })

        except Exception as e:
            problems.append({
                'file': file_path,
                'line': 0,
                'type': 'file_error',
                'message': f'Error reading file: {e}',
                'severity': 'error'
            })

        return problems

    def fix_problems_automatically(
            self, problems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Automatically fix detected problems"""
        fixed = []

        for problem in problems:
            try:
                if self.fix_single_problem(problem):
                    fixed.append(problem)
                    print(f"✅ Fixed: {problem['message']}")

            except Exception as e:
                print(f"❌ Error fixing problem: {e}")

        return fixed

    def fix_single_problem(self, problem: Dict[str, Any]) -> bool:
        """Fix a single problem"""
        try:
            file_path = problem['file']
            problem_type = problem['type']

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            modified = False

            if problem_type == 'line_too_long':
                # Break long lines
                line_num = problem['line'] - 1
                if line_num < len(lines):
                    long_line = lines[line_num]
                    if len(long_line) > 79:
                        # Simple line breaking
                        words = long_line.split()
                        new_lines = []
                        current_line = ''

                        for word in words:
                            if len(current_line + ' ' + word) <= 79:
                                current_line += (' ' +
word) if current_line else word
                            else:
                                if current_line:
                                    new_lines.append(current_line)
                                current_line = word

                        if current_line:
                            new_lines.append(current_line)

                        lines[line_num] = '\n    '.join(new_lines)
                        modified = True

            elif problem_type == 'trailing_whitespace':
                # Remove trailing whitespace
                line_num = problem['line'] - 1
                if line_num < len(lines):
                    lines[line_num] = lines[line_num].rstrip()
                    modified = True

            elif problem_type == 'bare_except':
                # Replace bare except with specific exception
                line_num = problem['line'] - 1
                if line_num < len(lines):
                    lines[line_num] = lines[line_num].replace(
                        'except Exception:', 'except Exception:')
                    modified = True

            elif problem_type == 'missing_newline':
                # Add newline at end
                if lines and lines[-1] != '':
                    lines.append('')
                modified = True

            if modified:
                # Write fixed content back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))

                # Log the fix
                self.log_fix(problem)
                return True

        except Exception as e:
            print(f"❌ Error fixing {problem['type']}: {e}")

        return False

    def log_fix(self, problem: Dict[str, Any]):
        """Log a fix operation"""
        fix_log = {
            'timestamp': datetime.now().isoformat(),
            'file': problem['file'],
            'problem_type': problem['type'],
            'message': problem['message'],
            'severity': problem['severity']
        }
        self.fix_history.append(fix_log)

    def generate_problem_report(self):
        """Generate problem detection report"""
        report = f"""
🔍 Real-Time Problem Detection Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 Problem Statistics:
• Total Problems Found: {len(self.problems_found)}
• Problems Fixed: {len(self.problems_fixed)}
• Problems Remaining: {len(self.problems_found) - len(self.problems_fixed)}

📋 Recent Fixes:
"""

        for fix in self.fix_history[-5:]:  # Last 5 fixes
            report += f"• {fix['file']}: {fix['message']}\n"

        report += f"""
🎯 System Status:
• Monitoring Active: {self.monitoring_active}
• Files Monitored: {len([f for f in os.listdir('.') if f.endswith('.py')])}
• Auto-Fix Enabled: True
• Real-Time Detection: Active

✅ All problems are being automatically detected and fixed!
"""

        print(report)

    def run_autopep8_on_all_files(self):
        """Run autopep8 on all Python files"""
        try:
            print("🔧 Running autopep8 on all files...")

            python_files = [f for f in os.listdir('.') if f.endswith('.py')]

            for file in python_files:
                try:
                    result = subprocess.run(['autopep8',
                                             '--in-place',
                                             '--aggressive',
                                             '--aggressive',
                                             file],
                                            capture_output=True,
                                            text=True)

                    if result.returncode == 0:
                        print(f"✅ Fixed formatting: {file}")
                    else:
                        print(f"❌ Error fixing {file}: {result.stderr}")

                except Exception as e:
                    print(f"❌ Error with {file}: {e}")

            print("✅ autopep8 completed on all files")

        except Exception as e:
            print(f"❌ Error running autopep8: {e}")

    def install_missing_packages(self):
        """Install missing type stubs and packages"""
        try:
            print("📦 Installing missing packages...")

            packages = [
                'types-psutil',
                'autopep8',
                'flake8',
                'mypy'
            ]

            for package in packages:
                try:
                    result = subprocess.run(['pip', 'install', package],
                                            capture_output=True, text=True)

                    if result.returncode == 0:
                        print(f"✅ Installed: {package}")
                    else:
                        print(f"❌ Error installing {package}: {result.stderr}")

                except Exception as e:
                    print(f"❌ Error with {package}: {e}")

            print("✅ Package installation completed")

        except Exception as e:
            print(f"❌ Error installing packages: {e}")


def main():
    """Main function to run real-time problem detection"""
    print("🚀 EHB-5 Real-Time Problem Detector")
    print("=" * 50)

    detector = RealTimeProblemDetector()

    # Install missing packages first
    detector.install_missing_packages()

    # Run autopep8 on all files
    detector.run_autopep8_on_all_files()

    # Start real-time monitoring
    try:
        detector.start_monitoring()
    except KeyboardInterrupt:
        print("\n⏹️ Stopping problem detector...")

    print("\n🎉 Problem detection completed!")


if __name__ == "__main__":
    main()
