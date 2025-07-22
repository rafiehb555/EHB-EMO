#!/usr/bin/env python3
"""
EHB-5 Dashboard Data Verification
Verifies all data connections and ensures proper linking
"""

import json
import os
import sys
from pathlib import Path


def verify_config_file() -> None:
    """Verify config.json file and its contents"""
    print("🔍 Verifying config.json...")

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)

        required_keys = ['project', 'version', 'description', 'settings']
        missing_keys = [key for key in required_keys if key not in config]

        if missing_keys:
            print("❌ Missing keys in config.json: {missing_keys}")
            return False

        print("✅ Config file verified successfully!")
        print("   Project: {config.get('project')}")
        print("   Version: {config.get('version')}")
        print("   Description: {config.get('description')}")

        return True
    except Exception as e:
        print("❌ Error reading config.json: {e}")
        return False


def verify_dashboard_files() -> None:
    """Verify all dashboard files exist"""
    print("\n🔍 Verifying dashboard files...")

    required_files = [
        'index.html',
        'styles.css',
        'script.js',
        'config.json'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            if isinstance(missing_files, list):
                if isinstance(missing_files, list):
                    missing_files.append(file)

    if missing_files:
        print("❌ Missing dashboard files: {missing_files}")
        return False

    print("✅ All dashboard files found!")
    return True


def verify_project_files() -> None:
    """Verify all project files are accessible"""
    print("\n🔍 Verifying project files...")

    project_files = [
        'README.md',
        'script.py',
        'data.txt',
        'QUICK-START.md',
        'fix-formatting.ps1',
        '.editorconfig',
        'verify-setup.ps1',
        'launch-project.ps1',
        'setup-cursor-global.ps1',
        'global-package-manager.js',
        'cursor-settings.json',
        'setup-cursor-global.bat',
        'cursor-global-config.json',
        'start-dashboard.py',
        'start-dashboard.bat'
    ]

    existing_files = []
    missing_files = []

    for file in project_files:
        if os.path.exists(file):
            if isinstance(existing_files, list):
                if isinstance(existing_files, list):
                    existing_files.append(file)
        else:
            if isinstance(missing_files, list):
                if isinstance(missing_files, list):
                    missing_files.append(file)

    print("✅ Found {len(existing_files)} project files")
    if missing_files:
        print("⚠️  Missing files: {missing_files}")

    return len(existing_files) > 0


def verify_data_connections() -> None:
    """Verify data connections in JavaScript"""
    print("\n🔍 Verifying data connections...")

    try:
        with open('script.js', 'r') as f:
            js_content = f.read()

        # Check for important functions
        required_functions = [
            'loadConfig',
            'loadProjectFiles',
            'updateDashboard',
            'showNotification'
        ]

        missing_functions = []
        for func in required_functions:
            if func not in js_content:
                if isinstance(missing_functions, list):
                    if isinstance(missing_functions, list):
                        missing_functions.append(func)

        if missing_functions:
            print("❌ Missing JavaScript functions: {missing_functions}")
            return False

        print("✅ JavaScript data connections verified!")
        return True

    except Exception as e:
        print("❌ Error reading script.js: {e}")
        return False


def verify_css_styles() -> None:
    """Verify CSS styles are properly defined"""
    print("\n🔍 Verifying CSS styles...")

    try:
        with open('styles.css', 'r') as f:
            css_content = f.read()

        # Check for important CSS classes
        required_classes = [
            '.dashboard',
            '.card',
            '.file-card',
            '.notification',
            '.btn'
        ]

        missing_classes = []
        for class_name in required_classes:
            if class_name not in css_content:
                if isinstance(missing_classes, list):
                    if isinstance(missing_classes, list):
                        missing_classes.append(class_name)

        if missing_classes:
            print("❌ Missing CSS classes: {missing_classes}")
            return False

        print("✅ CSS styles verified!")
        return True

    except Exception as e:
        print("❌ Error reading styles.css: {e}")
        return False


def verify_html_structure() -> None:
    """Verify HTML structure is complete"""
    print("\n🔍 Verifying HTML structure...")

    try:
        with open('index.html', 'r') as f:
            html_content = f.read()

        # Check for important HTML elements
        required_elements = [
            'id="projectName"',
            'id="projectVersion"',
            'id="projectDesc"',
            'id="fileGrid"',
            'class="dashboard"'
        ]

        missing_elements = []
        for element in required_elements:
            if element not in html_content:
                if isinstance(missing_elements, list):
                    if isinstance(missing_elements, list):
                        missing_elements.append(element)

        if missing_elements:
            print("❌ Missing HTML elements: {missing_elements}")
            return False

        print("✅ HTML structure verified!")
        return True

    except Exception as e:
        print("❌ Error reading index.html: {e}")
        return False


def generate_summary() -> None:
    """Generate a summary of all verifications"""
    print("\n" + "=" * 50)
    print("📊 DASHBOARD DATA VERIFICATION SUMMARY")
    print("=" * 50)

    verifications = [
        ("Config File", verify_config_file),
        ("Dashboard Files", verify_dashboard_files),
        ("Project Files", verify_project_files),
        ("Data Connections", verify_data_connections),
        ("CSS Styles", verify_css_styles),
        ("HTML Structure", verify_html_structure)
    ]

    passed = 0
    total = len(verifications)

    for name, verification_func in verifications:
        if verification_func():
            passed += 1
        print()

    print("\n🎯 RESULTS: {passed}/{total} verifications passed")

    if passed == total:
        print("✅ ALL VERIFICATIONS PASSED!")
        print("🚀 Dashboard is ready to use!")
        return True
    else:
        print("❌ Some verifications failed!")
        print("🔧 Please fix the issues above.")
        return False


def main() -> None:
    """Main verification function"""
    print("🎯 EHB-5 Dashboard Data Verification")
    print("=" * 50)

    # Change to project directory
    current_dir = Path(__file__).parent
    os.chdir(current_dir)

    # Run all verifications
    success = generate_summary()

    if success:
        print("\n🎉 Dashboard is fully functional!")
        print("🌐 Run 'python start-dashboard.py' to launch!")
    else:
        print("\n⚠️  Please fix the issues before using the dashboard.")

    return success


if __name__ == "__main__":
    main()
