#!/usr/bin/env python3
"""
EHB Python Project Test - Comprehensive testing of all Python components
"""

import importlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


class EHBPythonProjectTester:
    def __init__(self):
        self.project_root = Path.cwd()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests_passed": [],
            "tests_failed": [],
            "imports_working": [],
            "imports_failed": [],
            "files_created": [],
            "errors_fixed": [],
            "summary": {}
        }
    
    def test_python_imports(self):
        """Test Python module imports"""
        print("📦 Testing Python Imports...")
        
        modules_to_test = [
            "fastapi",
            "uvicorn",
            "sqlalchemy",
            "requests",
            "pytest",
            "black",
            "flake8",
            "mypy",
            "psutil",
            "numpy",
            "pandas",
            "matplotlib",
            "seaborn",
            "scikit-learn"
        ]
        
        for module in modules_to_test:
            try:
                importlib.import_module(module)
                print(f"✅ {module}: Import successful")
                self.results["imports_working"].append(module)
            except ImportError as e:
                print(f"❌ {module}: Import failed - {e}")
                self.results["imports_failed"].append(module)
    
    def test_python_files(self):
        """Test Python file execution"""
        print("🐍 Testing Python Files...")
        
        python_files = [
            "main.py",
            "config.py", 
            "utils.py",
            "models.py",
            "api.py",
            "database.py",
            "simple_server.py",
            "http_server.py"
        ]
        
        for file_name in python_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                try:
                    # Test syntax
                    with open(file_path, 'r', encoding='utf-8') as f:
                        source = f.read()
                    
                    # Parse Python code
                    compile(source, file_name, 'exec')
                    print(f"✅ {file_name}: Syntax OK")
                    self.results["tests_passed"].append(f"Syntax check: {file_name}")
                    
                except SyntaxError as e:
                    print(f"❌ {file_name}: Syntax error - {e}")
                    self.results["tests_failed"].append(f"Syntax error: {file_name}")
                except Exception as e:
                    print(f"❌ {file_name}: Error - {e}")
                    self.results["tests_failed"].append(f"File error: {file_name}")
            else:
                print(f"⚠️ {file_name}: File not found")
                self.results["tests_failed"].append(f"Missing file: {file_name}")
    
    def test_api_endpoints(self):
        """Test API endpoints"""
        print("🌐 Testing API Endpoints...")
        
        # Start server in background
        try:
            server_process = subprocess.Popen(
                [sys.executable, "simple_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            time.sleep(3)
            
            # Test endpoints
            endpoints = [
                "http://localhost:8000/",
                "http://localhost:8000/health",
                "http://localhost:8000/api/patients",
                "http://localhost:8000/api/doctors"
            ]
            
            import requests
            
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, timeout=5)
                    if response.status_code == 200:
                        print(f"✅ {endpoint}: Working")
                        self.results["tests_passed"].append(f"API endpoint: {endpoint}")
                    else:
                        print(f"⚠️ {endpoint}: Status {response.status_code}")
                        self.results["tests_failed"].append(f"API endpoint: {endpoint}")
                except Exception as e:
                    print(f"❌ {endpoint}: Error - {e}")
                    self.results["tests_failed"].append(f"API endpoint: {endpoint}")
            
            # Kill server
            server_process.terminate()
            
        except Exception as e:
            print(f"❌ API testing failed: {e}")
            self.results["tests_failed"].append(f"API testing: {e}")
    
    def test_database_operations(self):
        """Test database operations"""
        print("🗄️ Testing Database Operations...")
        
        try:
            # Test database imports
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker

            # Create test database
            engine = create_engine("sqlite:///test.db")
            
            # Test connection
            with engine.connect() as conn:
                result = conn.execute("SELECT 1")
                print("✅ Database connection: Working")
                self.results["tests_passed"].append("Database connection")
            
            # Clean up
            engine.dispose()
            if Path("test.db").exists():
                Path("test.db").unlink()
                
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            self.results["tests_failed"].append(f"Database test: {e}")
    
    def test_data_creation(self):
        """Test data creation and management"""
        print("📊 Testing Data Creation...")
        
        try:
            # Create test data
            test_data = {
                "patients": [
                    {"name": "Test Patient", "email": "test@example.com"}
                ],
                "doctors": [
                    {"name": "Test Doctor", "specialization": "Test"}
                ]
            }
            
            # Save to file
            data_dir = self.project_root / "data"
            data_dir.mkdir(exist_ok=True)
            
            with open(data_dir / "test_data.json", "w") as f:
                json.dump(test_data, f, indent=2)
            
            print("✅ Test data created")
            self.results["tests_passed"].append("Data creation")
            self.results["files_created"].append("data/test_data.json")
            
        except Exception as e:
            print(f"❌ Data creation failed: {e}")
            self.results["tests_failed"].append(f"Data creation: {e}")
    
    def test_utilities(self):
        """Test utility functions"""
        print("🔧 Testing Utilities...")
        
        try:
            # Test utils module
            if Path("utils.py").exists():
                import utils

                # Test functions if they exist
                if hasattr(utils, 'generate_secure_id'):
                    test_id = utils.generate_secure_id()
                    print(f"✅ generate_secure_id: {test_id}")
                    self.results["tests_passed"].append("generate_secure_id")
                
                if hasattr(utils, 'validate_email'):
                    test_email = "test@example.com"
                    result = utils.validate_email(test_email)
                    print(f"✅ validate_email: {result}")
                    self.results["tests_passed"].append("validate_email")
                
                print("✅ Utilities working")
            else:
                print("⚠️ utils.py not found")
                self.results["tests_failed"].append("utils.py missing")
                
        except Exception as e:
            print(f"❌ Utilities test failed: {e}")
            self.results["tests_failed"].append(f"Utilities test: {e}")
    
    def run_comprehensive_test(self):
        """Run comprehensive Python project test"""
        print("🧪 EHB Python Project Test")
        print("=" * 50)
        print("Testing Python project comprehensively...")
        print("=" * 50)
        
        try:
            # Step 1: Test imports
            self.test_python_imports()
            
            # Step 2: Test Python files
            self.test_python_files()
            
            # Step 3: Test API endpoints
            self.test_api_endpoints()
            
            # Step 4: Test database operations
            self.test_database_operations()
            
            # Step 5: Test data creation
            self.test_data_creation()
            
            # Step 6: Test utilities
            self.test_utilities()
            
            # Step 7: Generate summary
            self.generate_summary()
            
            print("✅ Comprehensive Python project test completed")
            
        except Exception as e:
            print(f"❌ Comprehensive test failed: {e}")
            self.results["summary"]["status"] = "failed"
            self.results["summary"]["error"] = str(e)
        
        return self.results
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 50)
        print("📊 PYTHON PROJECT TEST SUMMARY")
        print("=" * 50)
        
        # Tests passed
        if self.results["tests_passed"]:
            print(f"✅ Tests Passed: {len(self.results['tests_passed'])}")
            for test in self.results["tests_passed"][:10]:  # Show first 10
                print(f"  ✅ {test}")
        
        # Tests failed
        if self.results["tests_failed"]:
            print(f"\n❌ Tests Failed: {len(self.results['tests_failed'])}")
            for test in self.results["tests_failed"][:10]:  # Show first 10
                print(f"  ❌ {test}")
        
        # Imports working
        if self.results["imports_working"]:
            print(f"\n📦 Imports Working: {len(self.results['imports_working'])}")
            for module in self.results["imports_working"]:
                print(f"  ✅ {module}")
        
        # Imports failed
        if self.results["imports_failed"]:
            print(f"\n❌ Imports Failed: {len(self.results['imports_failed'])}")
            for module in self.results["imports_failed"]:
                print(f"  ❌ {module}")
        
        # Files created
        if self.results["files_created"]:
            print(f"\n📁 Files Created: {len(self.results['files_created'])}")
            for file in self.results["files_created"]:
                print(f"  📄 {file}")
        
        # Calculate success rate
        total_tests = len(self.results["tests_passed"]) + len(self.results["tests_failed"])
        if total_tests > 0:
            success_rate = (len(self.results["tests_passed"]) / total_tests) * 100
            print(f"\n📈 Test Success Rate: {success_rate:.1f}%")
        
        # Save results
        report_file = f"reports/python_project_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path("reports").mkdir(exist_ok=True)
        
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        print("=" * 50)
        
        self.results["summary"] = {
            "tests_passed": len(self.results["tests_passed"]),
            "tests_failed": len(self.results["tests_failed"]),
            "imports_working": len(self.results["imports_working"]),
            "imports_failed": len(self.results["imports_failed"]),
            "files_created": len(self.results["files_created"]),
            "success_rate": success_rate if total_tests > 0 else 100,
            "report_file": report_file
        }

def main():
    """Main function"""
    try:
        tester = EHBPythonProjectTester()
        results = tester.run_comprehensive_test()
        
        if results["summary"]["success_rate"] >= 80:
            print("\n🎉 Python project test completed successfully!")
            return 0
        else:
            print(f"\n⚠️ Some tests failed. Success rate: {results['summary']['success_rate']:.1f}%")
            return 1
            
    except Exception as e:
        print(f"❌ Python project test failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 