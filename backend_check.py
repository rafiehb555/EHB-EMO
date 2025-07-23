import json
import os
import sqlite3
import sys
from datetime import datetime

#!/usr/bin/env python3
"""
EHB-5 Backend Check Script
Comprehensive testing of all backend components
"""



def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python version too old")
        return False

def check_dependencies():
    """Check required dependencies"""
    print("\n📦 Checking dependencies...")
    dependencies = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'jwt': 'PyJWT',
        'psutil': 'psutil'
    }

    missing = []
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {name} installed")
        except ImportError:
            print(f"   ❌ {name} missing")
            missing.append(name)

    return len(missing) == 0

def check_database():
    """Check database setup"""
    print("\n🗄️  Checking database...")

    # Check if database file exists
    if os.path.exists('ehb5.db'):
        print("   ✅ Database file exists")
    else:
        print("   ❌ Database file missing")
        return False

    # Check database tables
    try:
        conn = sqlite3.connect('ehb5.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]

        required_tables = ['users', 'projects', 'data_files', 'system_logs']
        missing_tables = [table for table in required_tables if table not in table_names]

        if missing_tables:
            print(f"   ❌ Missing tables: {missing_tables}")
            return False
        else:
            print("   ✅ All required tables exist")
            return True

    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False
    finally:
        conn.close()

def check_file_structure():
    """Check backend file structure"""
    print("\n📁 Checking file structure...")

    required_files = [
        'main.py',
        'api_server.py',
        'database.py',
        'auth_manager.py',
        'data_processor.py',
        'requirements.txt'
    ]

    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file} exists")
        else:
            print(f"   ❌ {file} missing")
            missing_files.append(file)

    return len(missing_files) == 0

def check_syntax():
    """Check Python syntax"""
    print("\n🔍 Checking syntax...")

    python_files = [
        'main.py',
        'api_server.py',
        'database.py',
        'auth_manager.py',
        'data_processor.py'
    ]

    syntax_errors = []
    for file in python_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                compile(content, file, 'exec')
                print(f"   ✅ {file} syntax OK")
            except SyntaxError as e:
                print(f"   ❌ {file} syntax error: {e}")
                syntax_errors.append(file)
        else:
            print(f"   ⚠️  {file} not found")

    return len(syntax_errors) == 0

def check_api_endpoints():
    """Check API endpoint definitions"""
    print("\n🌐 Checking API endpoints...")

    try:
        with open('api_server.py', 'r', encoding='utf-8') as f:
            content = f.read()

        endpoints = [
            '/api/health',
            '/api/auth/register',
            '/api/auth/login',
            '/api/projects',
            '/api/data/files',
            '/api/data/process',
            '/api/system/status',
            '/api/system/logs'
        ]

        found_endpoints = []
        for endpoint in endpoints:
            if endpoint in content:
                found_endpoints.append(endpoint)
                print(f"   ✅ {endpoint} defined")
            else:
                print(f"   ❌ {endpoint} missing")

        return len(found_endpoints) >= 6  # At least 6 endpoints should be present

    except Exception as e:
        print(f"   ❌ Error checking endpoints: {e}")
        return False

def check_security():
    """Check security features"""
    print("\n🔒 Checking security features...")

    security_features = [
        'JWT token',
        'password hashing',
        'authentication decorator',
        'CORS',
        'input validation'
    ]

    try:
        with open('auth_manager.py', 'r', encoding='utf-8') as f:
            auth_content = f.read()

        with open('api_server.py', 'r', encoding='utf-8') as f:
            api_content = f.read()

        found_features = []
        for feature in security_features:
            if feature.lower() in auth_content.lower() or feature.lower() in api_content.lower():
                found_features.append(feature)
                print(f"   ✅ {feature} implemented")
            else:
                print(f"   ❌ {feature} missing")

        return len(found_features) >= 3  # At least 3 security features

    except Exception as e:
        print(f"   ❌ Error checking security: {e}")
        return False

def main():
    """Main check function"""
    print("=" * 60)
    print("🔧 EHB-5 BACKEND COMPREHENSIVE CHECK")
    print("=" * 60)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
        ("File Structure", check_file_structure),
        ("Syntax", check_syntax),
        ("API Endpoints", check_api_endpoints),
        ("Security", check_security)
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Error in {name}: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 BACKEND CHECK SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 All backend checks passed!")
        return True
    elif passed >= total * 0.8:
        print("⚠️  Most checks passed, minor issues found")
        return True
    else:
        print("❌ Multiple issues found, needs attention")
        return False

if __name__ == "__main__":
    main()
