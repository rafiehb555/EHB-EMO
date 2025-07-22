#!/usr/bin/env python3
"""
EHB-5 System Test Suite
Comprehensive testing of all system components
"""

import sys
import os
import json
import time
from datetime import datetime


def test_database():
    """Test database functionality"""
    print("🔍 Testing Database...")
    try:
        from database import db

        # Test database initialization
        db.init_database()
        print("✅ Database initialized successfully")

        # Test user creation
        test_user = db.create_user(
            "testuser",
            "test@example.com",
            "password_hash",
            "user")
        print(
            f"✅ User creation: {'Success' if test_user else 'User already exists'}")

        # Test project creation
        test_project = db.create_project("Test Project", "Test Description", 1)
        print(f"✅ Project creation: {'Success' if test_project else 'Failed'}")

        # Test getting projects
        projects = db.get_all_projects()
        print(f"✅ Get projects: {len(projects)} projects found")

        # Test data file operations
        test_file = db.save_data_file("test.txt", "text", "Test content", 1, 1)
        print(f"✅ File save: {'Success' if test_file else 'Failed'}")

        files = db.get_data_files()
        print(f"✅ Get files: {len(files)} files found")

        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False


def test_data_processor():
    """Test data processing functionality"""
    print("🔍 Testing Data Processor...")
    try:
        from data_processor import DataProcessor

        dp = DataProcessor()

        # Test data analysis
        test_data = "This is test data for EHB-5 project with some numbers: 123, 456, 789"
        result = dp.process_data(test_data, 'analyze')
        print(f"✅ Data analysis: {result.get('status', 'unknown')}")

        # Test data validation
        result = dp.process_data(test_data, 'validate')
        print(f"✅ Data validation: {result.get('status', 'unknown')}")

        # Test data transformation
        result = dp.process_data(test_data, 'transform')
        print(f"✅ Data transformation: {result.get('status', 'unknown')}")

        # Test data summarization
        result = dp.process_data(test_data, 'summarize')
        print(f"✅ Data summarization: {result.get('status', 'unknown')}")

        # Test data extraction
        result = dp.process_data(test_data, 'extract')
        print(f"✅ Data extraction: {result.get('status', 'unknown')}")

        return True

    except Exception as e:
        print(f"❌ Data processor test failed: {e}")
        return False


def test_auth_manager():
    """Test authentication functionality"""
    print("🔍 Testing Authentication Manager...")
    try:
        from auth_manager import AuthManager

        auth = AuthManager()

        # Test password hashing
        password = "testpassword123"
        hash1 = auth.hash_password(password)
        hash2 = auth.hash_password(password)
        print(
            f"✅ Password hashing: {'Consistent' if hash1 == hash2 else 'Inconsistent'}")

        # Test password validation
        valid_password = auth.validate_password("strongpass123")
        invalid_password = auth.validate_password("weak")
        print(
            f"✅ Password validation: {'Working' if valid_password and not invalid_password else 'Failed'}")

        return True

    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False


def test_ai_agents():
    """Test AI agents functionality"""
    print("🔍 Testing AI Agents...")
    try:
        from ai_agents import agent_manager

        # Test agent manager
        agents = agent_manager.get_all_agents()
        print(f"✅ Agent manager: {len(agents)} agents loaded")

        # Test data processor agent
        data_agent = agent_manager.get_agent("dataProcessor")
        if data_agent:
            result = data_agent.analyze_data("Test data for analysis")
            print(f"✅ Data processor agent: {result.get('status', 'unknown')}")

        # Test config manager agent
        config_agent = agent_manager.get_agent("configManager")
        if config_agent:
            result = config_agent.validate_config(
                {"project": "test", "version": "1.0"})
            print(f"✅ Config manager agent: {result.get('is_valid', False)}")

        # Test file organizer agent
        file_agent = agent_manager.get_agent("fileOrganizer")
        if file_agent:
            result = file_agent.scan_files(".")
            print(
                f"✅ File organizer agent: {result.get('total_files', 0)} files scanned")

        # Test code analyzer agent
        code_agent = agent_manager.get_agent("codeAnalyzer")
        if code_agent:
            result = code_agent.analyze_code_quality("main.py")
            print(
                f"✅ Code analyzer agent: {result.get('quality_score', 'unknown')}")

        # Test deployment manager agent
        deploy_agent = agent_manager.get_agent("deploymentManager")
        if deploy_agent:
            result = deploy_agent.check_deployment_readiness()
            print(
                f"✅ Deployment manager agent: {result.get('ready_for_deployment', False)}")

        return True

    except Exception as e:
        print(f"❌ AI agents test failed: {e}")
        return False


def test_api_server():
    """Test API server functionality"""
    print("🔍 Testing API Server...")
    try:
        from api_server import app

        # Test app creation
        print("✅ API server app created successfully")

        # Test routes
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            print(f"✅ Health endpoint: {response.status_code}")

            # Test system status endpoint
            response = client.get('/api/system/status')
            print(f"✅ System status endpoint: {response.status_code}")

        return True

    except Exception as e:
        print(f"❌ API server test failed: {e}")
        return False


def test_main_application():
    """Test main application functionality"""
    print("🔍 Testing Main Application...")
    try:
        from main import EHB5Application

        # Test application creation
        app = EHB5Application()
        print("✅ Main application created successfully")

        # Test system initialization
        app.initialize_system()
        print("✅ System initialization completed")

        return True

    except Exception as e:
        print(f"❌ Main application test failed: {e}")
        return False


def test_file_system():
    """Test file system and configuration"""
    print("🔍 Testing File System...")
    try:
        # Check required files
        required_files = [
            "main.py",
            "api_server.py",
            "database.py",
            "auth_manager.py",
            "data_processor.py",
            "ai_agents.py",
            "config.json",
            "requirements.txt"]

        missing_files = []
        for file in required_files:
            if os.path.exists(file):
                print(f"✅ File exists: {file}")
            else:
                print(f"❌ File missing: {file}")
                missing_files.append(file)

        # Check config.json
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
            print(
                f"✅ Config loaded: {config.get('project', 'Unknown')} v{config.get('version', 'Unknown')}")

        # Check requirements.txt
        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r") as f:
                requirements = f.read()
            print(
                f"✅ Requirements file: {len(requirements.splitlines())} dependencies")

        return len(missing_files) == 0

    except Exception as e:
        print(f"❌ File system test failed: {e}")
        return False


def run_comprehensive_test():
    """Run comprehensive system test"""
    print("=" * 60)
    print("🚀 EHB-5 COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    test_results = {}

    # Run all tests
    tests = [
        ("File System", test_file_system),
        ("Database", test_database),
        ("Data Processor", test_data_processor),
        ("Authentication", test_auth_manager),
        ("AI Agents", test_ai_agents),
        ("API Server", test_api_server),
        ("Main Application", test_main_application)
    ]

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            test_results[test_name] = result
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status}: {test_name}")
        except Exception as e:
            print(f"❌ ERROR: {test_name} - {e}")
            test_results[test_name] = False

    # Generate test report
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)

    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")

    print(f"\n📈 Overall Result: {passed_tests}/{total_tests} tests passed")
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"📊 Success Rate: {success_rate:.1f}%")

    if success_rate >= 90:
        print("🎉 EXCELLENT: System is ready for production!")
    elif success_rate >= 70:
        print("✅ GOOD: System is mostly functional")
    elif success_rate >= 50:
        print("⚠️  FAIR: System needs some improvements")
    else:
        print("❌ POOR: System needs significant work")

    print(
        f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    return success_rate >= 70


if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
